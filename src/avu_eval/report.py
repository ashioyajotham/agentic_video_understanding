from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Callable
import csv
import json
import statistics


def _usable(values):
    return [value for value in values if value is not None]


def _mean(values):
    values = _usable(values)
    return statistics.fmean(values) if values else None


def _median(values):
    values = _usable(values)
    return statistics.median(values) if values else None


def _stdev(values):
    values = _usable(values)
    return statistics.stdev(values) if len(values) > 1 else 0.0 if values else None


def _pct_change(old, new):
    return None if old in (None, 0) or new is None else (new / old - 1) * 100


def _fmt(value, digits=3):
    return "—" if value is None else f"{value:.{digits}f}"


def _fmt_change(value):
    return "—" if value is None else f"{value:+.1f}%"


def _model_label(model: str) -> str:
    return model.rsplit("/", 1)[-1]


def _provider_latency(row):
    return row.get("metadata", {}).get("provider_latency_seconds", row.get("latency_seconds"))


def _total_tokens(row):
    return row.get("metadata", {}).get("total_tokens")


def _thought_tokens(row):
    return row.get("metadata", {}).get("thought_tokens")


def _completed(row):
    return row.get("attempt_status", "completed") == "completed"


def _strict(row):
    return float(row.get("strict_correct", row["correct"]))


METRICS: list[tuple[str, Callable[[dict[str, Any]], Any]]] = [
    ("semantic_score", lambda row: row.get("score")),
    ("strict_score", _strict),
    ("input_tokens", lambda row: row.get("input_tokens")),
    ("total_tokens", _total_tokens),
    ("thought_tokens", _thought_tokens),
    ("provider_latency_seconds", _provider_latency),
    ("wall_latency_seconds", lambda row: row.get("latency_seconds")),
]


def _read_rows(input_path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in input_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    seen = set()
    for row in rows:
        key = (row["model"], row["task_id"], row["processing"], row["repetition"])
        if key in seen:
            raise ValueError(f"Duplicate observation key: {key!r}")
        seen.add(key)
    return rows


def _write_csv(path: Path, rows: list[dict[str, Any]], fallback_fields: list[str]) -> None:
    fields = list(rows[0]) if rows else fallback_fields
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _aggregate(items: list[dict[str, Any]]) -> dict[str, Any]:
    provider = [_provider_latency(row) for row in items]
    provider_mean = _mean(provider)
    provider_sd = _stdev(provider)
    return {
        "n": len(items),
        "completion_rate": _mean([_completed(row) for row in items]),
        "semantic_accuracy": _mean([row.get("score") for row in items]),
        "exact_accuracy": _mean([row.get("correct") for row in items]),
        "strict_accuracy": _mean([_strict(row) for row in items]),
        "mean_input_tokens": _mean([row.get("input_tokens") for row in items]),
        "mean_total_tokens": _mean([_total_tokens(row) for row in items]),
        "mean_thought_tokens": _mean([_thought_tokens(row) for row in items]),
        "mean_provider_latency_seconds": provider_mean,
        "median_provider_latency_seconds": _median(provider),
        "stdev_provider_latency_seconds": provider_sd,
        "provider_latency_cv": None if provider_mean in (None, 0) or provider_sd is None else provider_sd / provider_mean,
        "max_provider_latency_seconds": max(_usable(provider), default=None),
        "mean_wall_latency_seconds": _mean([row.get("latency_seconds") for row in items]),
        "errors": sum(bool(row.get("error")) for row in items),
    }


def _paired_means(pairs, getter):
    values = [(getter(left), getter(right)) for left, right in pairs]
    values = [(left, right) for left, right in values if left is not None and right is not None]
    return _mean([left for left, _ in values]), _mean([right for _, right in values]), len(values)


def build(input_path: Path, output_prefix: Path) -> None:
    rows = _read_rows(input_path)
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["model"], row["family"], row["processing"])].append(row)

    summary = [
        {"model": model, "family": family, "processing": processing, **_aggregate(items)}
        for (model, family, processing), items in sorted(grouped.items())
    ]
    # Append extensions instead of replacing them: model-version prefixes such as
    # ``gemini-3.7`` contain a dot but do not already have a file extension.
    _write_csv(Path(f"{output_prefix}.csv"), summary, ["model", "family", "processing"])

    lines = [
        "# Evaluation report", "", f"Attempts: {len(rows)}", f"Models: {len({row['model'] for row in rows})}", "",
        "## Model × family × mode summary", "",
        "| Model | Family | Mode | n | Completion | Semantic | Exact | Strict | Input tokens | Total tokens | Provider mean (s) | Provider median (s) | Provider CV | Provider max (s) | Errors |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in summary:
        lines.append(
            f"| {_model_label(item['model'])} | {item['family']} | {item['processing']} | {item['n']} | "
            f"{_fmt(item['completion_rate'])} | {_fmt(item['semantic_accuracy'])} | {_fmt(item['exact_accuracy'])} | "
            f"{_fmt(item['strict_accuracy'])} | {_fmt(item['mean_input_tokens'])} | {_fmt(item['mean_total_tokens'])} | "
            f"{_fmt(item['mean_provider_latency_seconds'])} | {_fmt(item['median_provider_latency_seconds'])} | "
            f"{_fmt(item['provider_latency_cv'])} | {_fmt(item['max_provider_latency_seconds'])} | {item['errors']} |"
        )

    # Include model in the key so records from different model versions cannot collide.
    index = {(r["model"], r["task_id"], r["repetition"], r["processing"]): r for r in rows}
    models = sorted({r["model"] for r in rows})
    lines.extend(["", "## Static versus agentic within each model"])
    for model in models:
        pairs = []
        keys = sorted({(r["task_id"], r["repetition"]) for r in rows if r["model"] == model})
        for task_id, repetition in keys:
            static = index.get((model, task_id, repetition, "static"))
            agentic = index.get((model, task_id, repetition, "agentic"))
            if static and agentic and _completed(static) and _completed(agentic):
                pairs.append((static, agentic))
        lines += ["", f"### {_model_label(model)}", "", f"Completed pairs: {len(pairs)}", "", "| Metric | Static mean | Agentic mean | Agentic change |", "|---|---:|---:|---:|"]
        for metric, getter in METRICS:
            sm, am, _ = _paired_means(pairs, getter)
            lines.append(f"| {metric} | {_fmt(sm)} | {_fmt(am)} | {_fmt_change(_pct_change(sm, am))} |")

    comparison_rows = []
    if len(models) >= 2:
        baseline = models[0]
        for candidate in models[1:]:
            for processing in sorted({r["processing"] for r in rows}):
                for task_id in sorted({r["task_id"] for r in rows}):
                    pairs = []
                    reps = sorted({r["repetition"] for r in rows if r["task_id"] == task_id and r["processing"] == processing})
                    for repetition in reps:
                        left = index.get((baseline, task_id, repetition, processing))
                        right = index.get((candidate, task_id, repetition, processing))
                        if left and right and _completed(left) and _completed(right):
                            pairs.append((left, right))
                    if not pairs:
                        continue
                    out = {"model_a": baseline, "model_b": candidate, "task_id": task_id, "processing": processing, "n_pairs": len(pairs)}
                    for metric, getter in METRICS:
                        left, right, _ = _paired_means(pairs, getter)
                        out[f"model_a_{metric}"] = left
                        out[f"model_b_{metric}"] = right
                        out[f"model_b_change_{metric}_pct"] = _pct_change(left, right)
                    out["quality_regression"] = out["model_b_semantic_score"] < out["model_a_semantic_score"]
                    comparison_rows.append(out)

        lines += ["", "## Model-to-model paired comparison", "", f"Baseline: {_model_label(baseline)}", "",
                  "| Candidate | Task | Mode | n | Semantic A | Semantic B | Input change | Total change | Thought change | Provider change | Wall change | Quality regression |",
                  "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for item in comparison_rows:
            lines.append(
                f"| {_model_label(item['model_b'])} | {item['task_id']} | {item['processing']} | {item['n_pairs']} | "
                f"{_fmt(item['model_a_semantic_score'])} | {_fmt(item['model_b_semantic_score'])} | "
                f"{_fmt_change(item['model_b_change_input_tokens_pct'])} | {_fmt_change(item['model_b_change_total_tokens_pct'])} | "
                f"{_fmt_change(item['model_b_change_thought_tokens_pct'])} | {_fmt_change(item['model_b_change_provider_latency_seconds_pct'])} | "
                f"{_fmt_change(item['model_b_change_wall_latency_seconds_pct'])} | {'YES' if item['quality_regression'] else 'no'} |"
            )

    _write_csv(output_prefix.parent / f"{output_prefix.name}-model-comparison.csv", comparison_rows,
               ["model_a", "model_b", "task_id", "processing", "n_pairs"])
    Path(f"{output_prefix}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

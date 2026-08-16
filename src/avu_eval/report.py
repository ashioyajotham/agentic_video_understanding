from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import json
import statistics


def _mean(values):
    usable = [v for v in values if v is not None]
    return statistics.fmean(usable) if usable else None


def build(input_path: Path, output_prefix: Path) -> None:
    rows = [json.loads(line) for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    groups = defaultdict(list)
    for row in rows:
        groups[(row["family"], row["processing"])].append(row)
    summary = []
    for (family, processing), items in sorted(groups.items()):
        summary.append({
            "family": family,
            "processing": processing,
            "n": len(items),
            "accuracy": _mean([x["score"] for x in items]),
            "strict_accuracy": _mean([x.get("strict_correct", x["correct"]) for x in items]),
            "completion_rate": _mean([x.get("attempt_status", "completed") == "completed" for x in items]),
            "mean_input_tokens": _mean([x.get("input_tokens") for x in items]),
            "mean_total_tokens": _mean([x.get("metadata", {}).get("total_tokens") for x in items]),
            "mean_output_tokens": _mean([x.get("output_tokens") for x in items]),
            "mean_latency_seconds": _mean([x.get("latency_seconds") for x in items]),
            "median_latency_seconds": statistics.median([x["latency_seconds"] for x in items]),
            "errors": sum(bool(x.get("error")) for x in items),
        })
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = output_prefix.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0].keys()) if summary else ["family"])
        writer.writeheader(); writer.writerows(summary)
    lines = ["# Evaluation report", "", f"Attempts: {len(rows)}", "", "| Family | Mode | n | Completion | Semantic | Strict | Input tokens | Total tokens | Median latency (s) | Errors |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for x in summary:
        fmt = lambda v: "—" if v is None else f"{v:.3f}"
        lines.append(f"| {x['family']} | {x['processing']} | {x['n']} | {fmt(x['completion_rate'])} | {fmt(x['accuracy'])} | {fmt(x['strict_accuracy'])} | {fmt(x['mean_input_tokens'])} | {fmt(x['mean_total_tokens'])} | {fmt(x['median_latency_seconds'])} | {x['errors']} |")

    indexed = {(x["task_id"], x["repetition"], x["processing"]): x for x in rows}
    pairs = []
    for (task_id, repetition, mode), static in indexed.items():
        if mode != "static":
            continue
        agentic = indexed.get((task_id, repetition, "agentic"))
        if not agentic or static.get("attempt_status", "completed") != "completed" or agentic.get("attempt_status", "completed") != "completed":
            continue
        pairs.append((static, agentic))
    lines.extend(["", "## Completed paired comparison", "", f"Pairs: {len(pairs)}", ""])
    lines.append("| Metric | Static mean | Agentic mean | Agentic change |")
    lines.append("|---|---:|---:|---:|")
    for label, getter in [
        ("Semantic score", lambda x: x["score"]),
        ("Strict score", lambda x: float(x.get("strict_correct", x["correct"]))),
        ("Input tokens", lambda x: x.get("input_tokens")),
        ("Total tokens", lambda x: x.get("metadata", {}).get("total_tokens")),
        ("Inference latency (s)", lambda x: x.get("metadata", {}).get("provider_latency_seconds", x.get("latency_seconds"))),
    ]:
        values = [(getter(s), getter(a)) for s, a in pairs]
        values = [(s, a) for s, a in values if s is not None and a is not None]
        sm = _mean([s for s, _ in values]); am = _mean([a for _, a in values])
        change = None if sm in (None, 0) else (am / sm - 1) * 100
        lines.append(f"| {label} | {fmt(sm)} | {fmt(am)} | {'—' if change is None else f'{change:+.1f}%'} |")
    output_prefix.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")

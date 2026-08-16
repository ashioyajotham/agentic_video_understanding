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
            "mean_input_tokens": _mean([x.get("input_tokens") for x in items]),
            "mean_output_tokens": _mean([x.get("output_tokens") for x in items]),
            "mean_latency_seconds": _mean([x.get("latency_seconds") for x in items]),
            "errors": sum(bool(x.get("error")) for x in items),
        })
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = output_prefix.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0].keys()) if summary else ["family"])
        writer.writeheader(); writer.writerows(summary)
    lines = ["# Evaluation report", "", f"Runs: {len(rows)}", "", "| Family | Mode | n | Accuracy | Input tokens | Latency (s) | Errors |", "|---|---:|---:|---:|---:|---:|---:|"]
    for x in summary:
        fmt = lambda v: "—" if v is None else f"{v:.3f}"
        lines.append(f"| {x['family']} | {x['processing']} | {x['n']} | {fmt(x['accuracy'])} | {fmt(x['mean_input_tokens'])} | {fmt(x['mean_latency_seconds'])} | {x['errors']} |")
    output_prefix.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")


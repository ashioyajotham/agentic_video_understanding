#!/usr/bin/env python3
"""Score exact event order from JSONL responses."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


def parse_order(text: str) -> list[str] | None:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            return None
        try:
            value = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    order = value.get("order") if isinstance(value, dict) else None
    if not isinstance(order, list) or not all(isinstance(item, str) for item in order):
        return None
    return [item.strip().lower() for item in order]


def score(results: Path, ground_truth_dir: Path) -> dict:
    truth = {
        path.stem: json.loads(path.read_text(encoding="utf-8"))["expected_order"]
        for path in ground_truth_dir.glob("*.json")
    }
    rows = []
    by_variant: dict[str, list[bool]] = defaultdict(list)
    completed = 0

    for line_number, line in enumerate(results.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        variant = record["variant_id"]
        if variant not in truth:
            raise ValueError(f"line {line_number}: no ground truth for {variant}")
        predicted = parse_order(record.get("response_text", ""))
        exact = record.get("status") == "completed" and predicted == truth[variant]
        completed += int(record.get("status") == "completed")
        by_variant[variant].append(exact)
        rows.append({
            "variant_id": variant,
            "mode": record.get("mode"),
            "attempt": record.get("attempt"),
            "expected": truth[variant],
            "predicted": predicted,
            "exact": exact,
            "status": record.get("status"),
        })

    total = len(rows)
    exact_total = sum(row["exact"] for row in rows)
    return {
        "attempts": total,
        "completed": completed,
        "exact": exact_total,
        "exact_rate": exact_total / total if total else None,
        "per_variant": {
            variant: {
                "attempts": len(values),
                "exact": sum(values),
                "exact_rate": sum(values) / len(values),
            }
            for variant, values in sorted(by_variant.items())
        },
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--ground-truth-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary = score(args.results, args.ground_truth_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: summary[key] for key in ("attempts", "completed", "exact", "exact_rate")}, indent=2))


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Score needle-in-a-haystack results on both Color sequence and Micro-ID accuracy."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

COLOR_MAP = {"purple": "magenta", "violet": "magenta", "pink": "magenta"}


def parse_order(text: str) -> list[dict] | None:
    # If wrapped inside TextContent string representation:
    m = re.search(r"text='(.*?)'(?:,\s*annotations=|\s*\))", text, re.DOTALL)
    if m:
        try:
            text = m.group(1).encode("utf-8").decode("unicode_escape")
        except Exception:
            text = m.group(1)

    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        val = json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            return None
        try:
            val = json.loads(match.group(0))
        except Exception:
            return None

    order = val.get("order") if isinstance(val, dict) else None
    if not isinstance(order, list):
        return None

    parsed = []
    for item in order:
        if isinstance(item, dict):
            c = str(item.get("color", "")).strip().lower()
            c = COLOR_MAP.get(c, c)
            d = str(item.get("id", "")).strip()
            parsed.append({"color": c, "id": d})
        elif isinstance(item, str):
            c = item.strip().lower()
            parsed.append({"color": COLOR_MAP.get(c, c), "id": ""})
    return parsed


def score_needle(results_path: Path, truth_dir: Path) -> dict:
    truth = {}
    for p in truth_dir.glob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        truth[data["variant_id"]] = data

    rows = []
    color_exact_count = 0
    id_exact_count = 0
    full_exact_count = 0

    for line in results_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        vid = rec["variant_id"]
        if vid not in truth:
            continue
        gt = truth[vid]
        gt_colors = gt["expected_colors"]
        gt_ids = gt["expected_ids"]

        pred = parse_order(rec.get("response_text", ""))
        pred_colors = [p["color"] for p in pred] if pred else []
        pred_ids = [p["id"] for p in pred] if pred else []

        color_exact = (pred_colors == gt_colors)
        id_exact = (pred_ids == gt_ids)
        full_exact = (color_exact and id_exact)

        if color_exact:
            color_exact_count += 1
        if id_exact:
            id_exact_count += 1
        if full_exact:
            full_exact_count += 1

        rows.append({
            "variant_id": vid,
            "mode": rec.get("mode"),
            "expected_colors": gt_colors,
            "predicted_colors": pred_colors,
            "expected_ids": gt_ids,
            "predicted_ids": pred_ids,
            "color_exact": color_exact,
            "id_exact": id_exact,
            "full_exact": full_exact,
            "status": rec.get("status"),
        })

    total = len(rows)
    return {
        "total_attempts": total,
        "color_exact": color_exact_count,
        "color_exact_rate": color_exact_count / total if total else 0.0,
        "id_exact": id_exact_count,
        "id_exact_rate": id_exact_count / total if total else 0.0,
        "full_exact": full_exact_count,
        "full_exact_rate": full_exact_count / total if total else 0.0,
        "rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--truth-dir", type=Path, default=Path("generated_needle/ground_truth"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = score_needle(args.results, args.truth_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in summary if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from avu_eval.report import build


def observation(model, task, mode, repetition, score, latency, tokens):
    return {
        "task_id": task,
        "family": "test_family",
        "processing": mode,
        "repetition": repetition,
        "model": model,
        "score": score,
        "correct": score == 1.0,
        "strict_correct": score == 1.0,
        "input_tokens": tokens,
        "output_tokens": 1,
        "latency_seconds": latency + 0.5,
        "attempt_status": "completed",
        "error": None,
        "metadata": {
            "total_tokens": tokens + 10,
            "thought_tokens": 9,
            "provider_latency_seconds": latency,
        },
    }


class ModelComparisonReportTest(unittest.TestCase):
    def test_models_do_not_collide_and_versioned_filename_is_preserved(self):
        rows = []
        for model, static_score, latency in [("models/model-3.6", 0.6, 10), ("models/model-3.7", 0.0, 5)]:
            rows.append(observation(model, "rapid", "static", 1, static_score, latency, 100))
            rows.append(observation(model, "rapid", "agentic", 1, 1.0, latency + 2, 200))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.jsonl"
            source.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
            prefix = root / "gemini-3.6-vs-3.7"
            build(source, prefix)

            self.assertTrue((root / "gemini-3.6-vs-3.7.md").exists())
            self.assertTrue((root / "gemini-3.6-vs-3.7.csv").exists())
            with (root / "gemini-3.6-vs-3.7-model-comparison.csv").open(newline="", encoding="utf-8") as handle:
                comparison = list(csv.DictReader(handle))
            self.assertEqual(len(comparison), 2)
            regression = [row for row in comparison if row["processing"] == "static"][0]
            self.assertEqual(regression["quality_regression"], "True")

            report = (root / "gemini-3.6-vs-3.7.md").read_text(encoding="utf-8")
            self.assertEqual(report.count("Completed pairs: 1"), 2)


if __name__ == "__main__":
    unittest.main()

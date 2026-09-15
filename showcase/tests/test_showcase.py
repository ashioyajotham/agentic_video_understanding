from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


generator = load("generator", "rapid_crossing/generate_variants.py")
scorer = load("scorer", "rapid_crossing/score_results.py")


class ShowcaseTests(unittest.TestCase):
    def test_plan_is_deterministic(self):
        spec = json.loads((ROOT / "rapid_crossing/variants.json").read_text())
        variant = spec["variants"][0]
        self.assertEqual(
            generator.build_plan(variant, spec["video"]),
            generator.build_plan(variant, spec["video"]),
        )

    def test_registered_variants_change_order(self):
        spec = json.loads((ROOT / "rapid_crossing/variants.json").read_text())
        orders = {
            tuple(generator.build_plan(variant, spec["video"])["expected_order"])
            for variant in spec["variants"]
        }
        self.assertGreaterEqual(len(orders), 4)

    def test_parse_order_accepts_json_and_fences(self):
        expected = ["red", "blue"]
        self.assertEqual(scorer.parse_order('{"order":["red","blue"]}'), expected)
        self.assertEqual(scorer.parse_order('```json\n{"order":["red","blue"]}\n```'), expected)

    def test_scoring_uses_per_clip_ground_truth(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            truth = root / "truth"
            truth.mkdir()
            (truth / "v1.json").write_text(json.dumps({"expected_order": ["green", "red"]}))
            results = root / "results.jsonl"
            results.write_text(json.dumps({
                "variant_id": "v1",
                "mode": "agentic",
                "attempt": 1,
                "status": "completed",
                "response_text": '{"order":["green","red"]}',
            }) + "\n")
            summary = scorer.score(results, truth)
            self.assertEqual(summary["exact"], 1)
            self.assertEqual(summary["exact_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()

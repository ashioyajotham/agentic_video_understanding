from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from avu_eval.schema import load_tasks
from avu_eval.showcase import export_showcase, verify_showcase


REPOSITORY = Path(__file__).resolve().parents[1]
SUITE = REPOSITORY / "data/tasks/phase4_tracking_ablation.jsonl"


class ShowcaseExportTests(unittest.TestCase):
    def test_ocr_control_is_a_matched_ablation(self):
        by_id = {task.id: task for task in load_tasks(SUITE)}
        unlabeled = by_id["phase4_control_unlabeled"]
        labeled = by_id["phase4_ocr_positive_control"]
        self.assertEqual(unlabeled.expected, labeled.expected)
        left = {key: value for key, value in unlabeled.generator.items() if key != "show_labels"}
        right = {key: value for key, value in labeled.generator.items() if key != "show_labels"}
        self.assertEqual(left, right)
        self.assertFalse(unlabeled.generator["show_labels"])
        self.assertTrue(labeled.generator["show_labels"])

    def test_export_and_verification_preserve_exact_bytes_and_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tasks = load_tasks(SUITE)
            for task in tasks:
                video = root / task.video
                video.parent.mkdir(parents=True, exist_ok=True)
                video.write_bytes(f"canonical:{task.video}".encode())
            output = root / "showcase/generated_canonical_phase4"
            manifest = export_showcase(root=root, suite_path=SUITE, output_dir=output, generate=False)
            self.assertEqual(manifest["task_count"], 8)
            self.assertEqual(manifest["claim_status"], "stimuli_only_no_model_results")
            self.assertTrue(all(item["provenance"]["exact_canonical_render"] for item in manifest["tasks"]))
            self.assertEqual(verify_showcase(root=root, suite_path=SUITE, input_dir=output), {"tasks": 8, "videos": 8})

            first = output / manifest["tasks"][0]["clip"]
            first.write_bytes(first.read_bytes() + b"tampered")
            with self.assertRaisesRegex(ValueError, "Clip hash mismatch"):
                verify_showcase(root=root, suite_path=SUITE, input_dir=output)

    def test_showcase_registry_separates_demo_from_claim_evidence(self):
        import yaml

        registry = yaml.safe_load((REPOSITORY / "showcase/manifest.yaml").read_text(encoding="utf-8"))
        self.assertFalse(registry["showcase"]["demo_suite"]["claim_evidence"])
        self.assertTrue(registry["showcase"]["canonical_benchmark"]["exact_render_required"])
        self.assertEqual(
            registry["showcase"]["canonical_benchmark"]["suite"],
            "data/tasks/phase4_tracking_ablation.jsonl",
        )


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path

from avu_eval.runner import completed_keys, matrix
from avu_eval.schema import Task


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.task = Task("t", "f", "v.mp4", "q", "exact", "a")

    def test_counterbalanced_order(self):
        jobs = list(matrix([self.task], {
            "processing_modes": ["static", "agentic"], "repetitions": 2,
            "order_strategy": "counterbalanced",
        }))
        self.assertEqual([x[1] for x in jobs], ["static", "agentic", "agentic", "static"])

    def test_resume_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "run.jsonl"
            path.write_text('{"task_id":"t","processing":"static","repetition":1}\n')
            self.assertEqual(completed_keys(path), {("t", "static", 1)})


if __name__ == "__main__":
    unittest.main()

import unittest

from avu_eval.grading import grade, grade_format


class GradingTests(unittest.TestCase):
    def test_number(self):
        self.assertEqual(grade("number", 4, "4"), 1.0)
        self.assertEqual(grade("number", 4, "There were three."), 0.0)

    def test_ordered_list(self):
        self.assertEqual(grade("ordered_list", ["red", "blue"], '["red", "blue"]'), 1.0)
        self.assertEqual(grade("ordered_list", ["red", "blue"], '["blue", "red"]'), 0.0)

    def test_negative_exact(self):
        self.assertEqual(grade("exact", "no", "No."), 1.0)

    def test_strict_format(self):
        self.assertEqual(grade_format("number", "4"), 1.0)
        self.assertEqual(grade_format("number", "The answer is 4"), 0.0)
        self.assertEqual(grade_format("ordered_list", '["red", "blue"]'), 1.0)
        self.assertEqual(grade_format("ordered_list", '```json\n["red", "blue"]\n```'), 0.0)


if __name__ == "__main__":
    unittest.main()

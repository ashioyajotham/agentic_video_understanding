import unittest

from avu_eval.grading import grade


class GradingTests(unittest.TestCase):
    def test_number(self):
        self.assertEqual(grade("number", 4, "4"), 1.0)
        self.assertEqual(grade("number", 4, "There were three."), 0.0)

    def test_ordered_list(self):
        self.assertEqual(grade("ordered_list", ["red", "blue"], '["red", "blue"]'), 1.0)
        self.assertEqual(grade("ordered_list", ["red", "blue"], '["blue", "red"]'), 0.0)

    def test_negative_exact(self):
        self.assertEqual(grade("exact", "no", "No."), 1.0)


if __name__ == "__main__":
    unittest.main()

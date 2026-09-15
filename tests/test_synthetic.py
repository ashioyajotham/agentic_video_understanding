import unittest

from avu_eval.schema import Task
from avu_eval.synthetic import _rapid_x, validate_generator_spec


def rapid_task(generator, expected=None):
    expected = expected if expected is not None else [
        event["color"]
        for event in sorted(generator["events"], key=lambda event: event["time"])
        if event.get("crosses", True)
    ]
    return Task("rapid", "fine_motion", "rapid.mp4", "q", "ordered_list", expected, generator)


class RapidGeneratorTests(unittest.TestCase):
    def test_rejects_subframe_ordering(self):
        task = rapid_task({
            "type": "rapid_order", "fps": 30, "minimum_gap_frames": 2,
            "events": [
                {"time": 1.0, "color": "red"},
                {"time": 1.03, "color": "blue"},
            ],
        })
        with self.assertRaisesRegex(ValueError, "only 0.90 frames apart"):
            validate_generator_spec(task)

    def test_decoys_are_excluded_from_ground_truth(self):
        task = rapid_task({
            "type": "rapid_order", "fps": 30, "object_radius": 12,
            "events": [
                {"time": 1.0, "color": "red"},
                {"time": 1.1, "color": "yellow", "crosses": False, "closest_offset": 16},
                {"time": 1.2, "color": "blue", "direction": "rtl"},
            ],
        })
        validate_generator_spec(task)

    def test_decoy_never_crosses_gate(self):
        event = {
            "time": 1.0, "color": "yellow", "crosses": False,
            "direction": "ltr", "closest_offset": 16,
        }
        self.assertLess(_rapid_x(0.9, event, 320, 400), 320)
        self.assertLess(_rapid_x(1.0, event, 320, 400), 320)
        self.assertLess(_rapid_x(1.1, event, 320, 400), 320)

    def test_rejects_incorrect_expected_order(self):
        task = rapid_task({
            "type": "rapid_order", "fps": 30,
            "events": [
                {"time": 1.0, "color": "red"},
                {"time": 1.1, "color": "blue"},
            ],
        }, expected=["blue", "red"])
        with self.assertRaisesRegex(ValueError, "does not match rendered crossings"):
            validate_generator_spec(task)


if __name__ == "__main__":
    unittest.main()

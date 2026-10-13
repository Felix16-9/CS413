"""Required test cases from the Part I handout, plus schedule sanity checks."""

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from delivery import Delivery, load_deliveries
from task_a import count_maximum_deliveries, select_maximum_deliveries
from task_b import assign_minimum_drivers, minimum_drivers
from task_c import count_minimum_rejections, minimum_rejections
from task_d import (
    BETTER_SCHEDULE,
    COUNTEREXAMPLE,
    greedy_schedule,
    schedule_value,
)


def _deliveries(intervals):
    return [Delivery(f"D{index}", start, finish) for index, (start, finish) in enumerate(intervals, start=1)]


def _assert_compatible(test, deliveries):
    for left_index, left in enumerate(deliveries):
        for right in deliveries[left_index + 1 :]:
            test.assertFalse(
                left.overlaps(right),
                f"{left.id} ({left.start},{left.finish}) overlaps {right.id} ({right.start},{right.finish})",
            )


class TaskATests(unittest.TestCase):
    CASES = (
        ("01_no_deliveries.txt", [], 0),
        ("02_single.txt", [(1, 3)], 1),
        ("03_chain.txt", [(1, 3), (3, 5), (5, 7)], 3),
        ("04_nested_overlap.txt", [(1, 5), (2, 6), (3, 7)], 1),
        ("05_one_conflict.txt", [(5, 7), (1, 3), (3, 5), (2, 4)], 3),
        ("06_shared_finish.txt", [(1, 4), (2, 4), (4, 6)], 2),
    )

    def test_required_counts_and_compatibility(self):
        directory = ROOT / "data" / "required" / "task_a"
        for filename, intervals, expected in self.CASES:
            with self.subTest(filename=filename):
                from_file = load_deliveries(str(directory / filename))
                built = _deliveries(intervals)
                for deliveries in (from_file, built):
                    selected = select_maximum_deliveries(deliveries)
                    self.assertEqual(count_maximum_deliveries(deliveries), expected)
                    self.assertEqual(len(selected), expected)
                    _assert_compatible(self, selected)

    def test_endpoint_touching_is_compatible(self):
        deliveries = _deliveries([(1, 3), (3, 5)])
        selected = select_maximum_deliveries(deliveries)
        self.assertEqual(len(selected), 2)


class TaskBTests(unittest.TestCase):
    CASES = (
        ("01_no_deliveries.txt", [], 0),
        ("02_single.txt", [(1, 3)], 1),
        ("03_chain.txt", [(1, 3), (3, 5), (5, 7)], 1),
        ("04_all_overlap.txt", [(1, 5), (2, 6), (3, 7)], 3),
        ("05_two_drivers.txt", [(1, 4), (2, 5), (4, 7), (5, 8)], 2),
        ("06_unsorted.txt", [(5, 8), (1, 4), (2, 5), (4, 6), (6, 9)], 2),
    )

    def test_required_counts_and_no_overlap(self):
        directory = ROOT / "data" / "required" / "task_b"
        for filename, intervals, expected in self.CASES:
            with self.subTest(filename=filename):
                from_file = load_deliveries(str(directory / filename))
                built = _deliveries(intervals)
                for deliveries in (from_file, built):
                    schedules = assign_minimum_drivers(deliveries)
                    self.assertEqual(minimum_drivers(deliveries), expected)
                    self.assertEqual(len(schedules), expected)
                    assigned = [delivery.id for jobs in schedules for delivery in jobs]
                    self.assertCountEqual(assigned, [delivery.id for delivery in deliveries])
                    for jobs in schedules:
                        _assert_compatible(self, jobs)


class TaskCTests(unittest.TestCase):
    CASES = (
        ("01_no_deliveries.txt", [], 0),
        ("02_single.txt", [(1, 3)], 0),
        ("03_chain.txt", [(1, 3), (3, 5), (5, 7)], 0),
        ("04_all_overlap.txt", [(1, 5), (2, 6), (3, 7)], 2),
        ("05_one_conflict.txt", [(5, 7), (1, 3), (3, 5), (2, 4)], 1),
        ("06_one_extra.txt", [(1, 2), (2, 3), (3, 4), (1, 3)], 1),
    )

    def test_required_counts(self):
        directory = ROOT / "data" / "required" / "task_c"
        for filename, intervals, expected in self.CASES:
            with self.subTest(filename=filename):
                from_file = load_deliveries(str(directory / filename))
                built = _deliveries(intervals)
                for deliveries in (from_file, built):
                    kept, rejected = minimum_rejections(deliveries)
                    self.assertEqual(count_minimum_rejections(deliveries), expected)
                    self.assertEqual(len(rejected), expected)
                    self.assertEqual(len(kept) + len(rejected), len(deliveries))
                    _assert_compatible(self, kept)
                    self.assertEqual(len(rejected), len(deliveries) - len(kept))


class TaskDTests(unittest.TestCase):
    def test_greedy_is_not_optimal(self):
        greedy = greedy_schedule(COUNTEREXAMPLE)
        self.assertEqual(greedy, {"A": 0, "B": 1, "C": 2})
        greedy_value = schedule_value(COUNTEREXAMPLE, greedy)
        better_value = schedule_value(COUNTEREXAMPLE, BETTER_SCHEDULE)
        self.assertEqual(greedy_value, Fraction(17, 2))
        self.assertEqual(better_value, Fraction(28, 3))
        self.assertGreater(better_value, greedy_value)


class SampleFileTests(unittest.TestCase):
    def test_handout_sample(self):
        deliveries = load_deliveries(str(ROOT / "data" / "sample_deliveries.txt"))
        self.assertEqual(len(deliveries), 7)
        self.assertEqual(count_maximum_deliveries(deliveries), 3)
        self.assertEqual(minimum_drivers(deliveries), 3)
        self.assertEqual(count_minimum_rejections(deliveries), 4)
        _assert_compatible(self, select_maximum_deliveries(deliveries))
        for jobs in assign_minimum_drivers(deliveries):
            _assert_compatible(self, jobs)


if __name__ == "__main__":
    unittest.main()

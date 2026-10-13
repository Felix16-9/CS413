"""Read a delivery file and answer the Part I scheduling questions.

Examples, from this directory:

    python3 run.py data/sample_deliveries.txt
    python3 run.py --task a data/sample_deliveries.txt
    python3 run.py --required
"""

import argparse
import sys
from pathlib import Path

from delivery import load_deliveries
from task_a import select_maximum_deliveries
from task_b import assign_minimum_drivers
from task_c import minimum_rejections


def format_task_a(deliveries) -> str:
    selected = select_maximum_deliveries(deliveries)
    lines = ["Selected deliveries:"]
    if not selected:
        lines.append("(none)")
    else:
        for delivery in selected:
            lines.append(f"{delivery.id} {delivery.start} {delivery.finish}")
    lines.append(f"Total deliveries completed: {len(selected)}")
    return "\n".join(lines)


def format_task_b(deliveries) -> str:
    schedules = assign_minimum_drivers(deliveries)
    lines = []
    for index, jobs in enumerate(schedules, start=1):
        ids = " ".join(delivery.id for delivery in jobs)
        lines.append(f"Driver {index}: {ids}")
    lines.append(f"Minimum drivers required: {len(schedules)}")
    return "\n".join(lines)


def format_task_c(deliveries) -> str:
    _kept, rejected = minimum_rejections(deliveries)
    lines = [f"Minimum deliveries rejected: {len(rejected)}"]
    lines.append("Rejected deliveries:")
    if not rejected:
        lines.append("(none)")
    else:
        for delivery in rejected:
            lines.append(f"{delivery.id} {delivery.start} {delivery.finish}")
    return "\n".join(lines)


FORMATTERS = {
    "a": format_task_a,
    "b": format_task_b,
    "c": format_task_c,
}


def report(deliveries, task: str) -> str:
    if task == "all":
        sections = [
            "Task A: maximum deliveries for one driver",
            format_task_a(deliveries),
            "",
            "Task B: minimum number of drivers",
            format_task_b(deliveries),
            "",
            "Task C: minimum deliveries to reject",
            format_task_c(deliveries),
        ]
        return "\n".join(sections)
    return FORMATTERS[task](deliveries)


def run_required_cases(root: Path) -> int:
    """Print the program output for every required test-case file."""
    case_root = root / "data" / "required"
    exit_code = 0
    for task_name in ("task_a", "task_b", "task_c"):
        task = task_name[-1]
        directory = case_root / task_name
        files = sorted(directory.glob("*.txt"))
        if not files:
            print(f"No files in {directory}", file=sys.stderr)
            exit_code = 1
            continue
        print(f"===== {task_name} =====")
        for path in files:
            deliveries = load_deliveries(str(path))
            print(f"--- {path.name} ---")
            print(report(deliveries, task))
            print()
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pioneer Delivery Part I: greedy scheduling."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="delivery request file (id, start time, finish time)",
    )
    parser.add_argument(
        "--task",
        choices=("a", "b", "c", "all"),
        default="all",
        help="which question to answer (default: all)",
    )
    parser.add_argument(
        "--required",
        action="store_true",
        help="run every required test-case file under data/required/",
    )
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent
    if args.required:
        return run_required_cases(root)
    if not args.file:
        parser.error("give a delivery file, or pass --required")
    deliveries = load_deliveries(args.file)
    print(report(deliveries, args.task))
    return 0


if __name__ == "__main__":
    sys.exit(main())

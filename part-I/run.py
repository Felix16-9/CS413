"""Read deliveries and answer the Part I scheduling questions.

Examples, from this directory:

    python3 run.py
    python3 run.py data/sample_deliveries.txt
    python3 run.py --task a data/sample_deliveries.txt
    python3 run.py --required
"""

import argparse
import sys
from pathlib import Path

from delivery import _next_id, _pieces, load_deliveries, parse_delivery_line, parse_deliveries
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


def prompt_deliveries(input_func=input, output=print) -> list:
    """Ask for deliveries until a blank line, 'done', or 'q'.

    A bad line is reported and ignored so the user can keep typing.
    """
    output("Enter deliveries, one per line. Any of these are fine:")
    output("  D1 1 3")
    output("  1 3")
    output("  (1, 3)")
    output("  D2 4-7")
    output("Blank line, done, or q when you are finished.")
    deliveries = []
    seen = set()
    while True:
        try:
            raw = input_func("> ")
        except EOFError:
            output("")
            break
        text = raw.strip()
        if text == "" or text.lower() in {"done", "q", "quit"}:
            break
        added = False
        for piece in _pieces(raw):
            try:
                delivery = parse_delivery_line(piece, _next_id(seen))
            except ValueError as exc:
                output(str(exc))
                continue
            if delivery is None:
                continue
            if delivery.id in seen:
                output(f"{delivery.id} is already used. Type a different id.")
                continue
            seen.add(delivery.id)
            deliveries.append(delivery)
            added = True
        if added:
            output(f"  kept {len(deliveries)} so far")
    return deliveries


def read_deliveries(file_path, input_func=input, output=print) -> list:
    """Load a file, stdin, or an interactive prompt."""
    if file_path:
        return load_deliveries(file_path)
    if not sys.stdin.isatty():
        return parse_deliveries(sys.stdin)
    return prompt_deliveries(input_func=input_func, output=output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pioneer Delivery Part I: greedy scheduling."
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="delivery file. Leave this off to type deliveries yourself.",
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
    try:
        deliveries = read_deliveries(args.file)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(report(deliveries, args.task))
    return 0


if __name__ == "__main__":
    sys.exit(main())

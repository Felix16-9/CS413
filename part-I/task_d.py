"""Task D: a counterexample to scheduling by decreasing profit.

The proposed greedy strategy G considers deliveries in order of decreasing
profit and places each one in the earliest free time slot at or after its
ready time. Each delivery occupies one integer time slot. The value of
delivery j on schedule S is

    V_j(S) = P_j / (1 + D_j(S)),    D_j(S) = T_j(S) - R_j

and V(S) is the sum of those values.

This module builds a three-delivery counterexample, runs strategy G, and
compares it with a better schedule.
"""

from fractions import Fraction


# (id, ready time R_j, profit P_j). Profits are pairwise distinct.
COUNTEREXAMPLE = (
    ("A", 0, 5),
    ("B", 0, 4),
    ("C", 1, 3),
)

# A schedule that beats greedy strategy G on COUNTEREXAMPLE.
BETTER_SCHEDULE = {"A": 0, "C": 1, "B": 2}


def delivery_value(profit: int, ready: int, slot: int) -> Fraction:
    """Return P / (1 + delay) for one delivery assigned to an integer slot."""
    if slot < ready:
        raise ValueError(f"slot {slot} is earlier than ready time {ready}")
    delay = slot - ready
    return Fraction(profit, 1 + delay)


def schedule_value(jobs, assignment) -> Fraction:
    """Return V(S) for an assignment of job id -> time slot."""
    by_id = {job_id: (ready, profit) for job_id, ready, profit in jobs}
    if set(assignment) != set(by_id):
        raise ValueError("assignment must include every delivery exactly once")
    slots = list(assignment.values())
    if len(slots) != len(set(slots)):
        raise ValueError("two deliveries were given the same time slot")
    total = Fraction(0)
    for job_id, slot in assignment.items():
        ready, profit = by_id[job_id]
        total += delivery_value(profit, ready, slot)
    return total


def greedy_schedule(jobs) -> dict:
    """Run strategy G: decreasing profit, then the earliest free feasible slot."""
    ordered = sorted(jobs, key=lambda job: -job[2])
    used = set()
    assignment = {}
    for job_id, ready, _profit in ordered:
        slot = ready
        while slot in used:
            slot += 1
        used.add(slot)
        assignment[job_id] = slot
    return assignment


def describe_schedule(jobs, assignment) -> list:
    """Return one human-readable line per delivery, in scheduled-slot order."""
    by_id = {job_id: (ready, profit) for job_id, ready, profit in jobs}
    lines = []
    for job_id, slot in sorted(assignment.items(), key=lambda item: item[1]):
        ready, profit = by_id[job_id]
        delay = slot - ready
        value = delivery_value(profit, ready, slot)
        lines.append(
            f"{job_id}: R={ready}, P={profit}, slot={slot}, delay={delay}, value={value}"
        )
    return lines


def main() -> None:
    greedy = greedy_schedule(COUNTEREXAMPLE)
    greedy_value = schedule_value(COUNTEREXAMPLE, greedy)
    better_value = schedule_value(COUNTEREXAMPLE, BETTER_SCHEDULE)
    print("Greedy strategy G")
    for line in describe_schedule(COUNTEREXAMPLE, greedy):
        print(f"  {line}")
    print(f"V(G) = {greedy_value}")
    print()
    print("Better schedule S")
    for line in describe_schedule(COUNTEREXAMPLE, BETTER_SCHEDULE):
        print(f"  {line}")
    print(f"V(S) = {better_value}")
    print()
    print(f"V(S) > V(G): {better_value > greedy_value}")


if __name__ == "__main__":
    main()

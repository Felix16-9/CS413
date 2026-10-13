"""Task C: fewest deliveries to reject so one driver can do the rest."""

from task_a import select_maximum_deliveries


def minimum_rejections(deliveries: list) -> tuple:
    """Return (kept, rejected) for a minimum set of rejections.

    Keeping a largest compatible subset (Task A) and rejecting everyone else
    minimizes the number rejected. If that subset has size k, exactly n - k
    deliveries are rejected.

    Running time is O(n log n), the same as Task A. Listing the rejected
    deliveries is an additional O(n) pass.
    """
    kept = select_maximum_deliveries(deliveries)
    kept_objects = {id(delivery) for delivery in kept}
    rejected = [delivery for delivery in deliveries if id(delivery) not in kept_objects]
    return kept, rejected


def count_minimum_rejections(deliveries: list) -> int:
    """Return how many deliveries must be rejected."""
    _kept, rejected = minimum_rejections(deliveries)
    return len(rejected)

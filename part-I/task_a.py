"""Task A: largest set of deliveries one driver can finish."""


def select_maximum_deliveries(deliveries: list) -> list:
    """Select a maximum set of mutually compatible deliveries.

    Greedy choice: among the deliveries that do not overlap the ones already
    chosen, take the one that finishes earliest.

    Running time is O(n log n): sorting by finish time dominates a single
    left-to-right scan.
    """
    ordered = sorted(deliveries, key=lambda delivery: (delivery.finish, delivery.start, delivery.id))
    selected = []
    available_at = None
    for delivery in ordered:
        if available_at is not None and delivery.start < available_at:
            continue
        selected.append(delivery)
        available_at = delivery.finish
    return selected


def count_maximum_deliveries(deliveries: list) -> int:
    """Return how many deliveries one driver can complete."""
    return len(select_maximum_deliveries(deliveries))

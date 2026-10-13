"""Task B: fewest drivers that can accept every delivery."""

import heapq


def assign_minimum_drivers(deliveries: list) -> list:
    """Assign every delivery to a driver, using as few drivers as possible.

    Deliveries are processed in increasing order of start time. A min-heap
    stores one entry per driver:

        (free_time, driver_index)

    free_time is the finish time of that driver's most recent delivery, which
    is the earliest time that driver can accept another request.

    For each delivery, if the driver who becomes free soonest is free at or
    before the delivery's start, that driver takes the delivery. Otherwise
    every current driver is still busy, so a new driver is added.

    Running time is O(n log n): the sort is O(n log n) and each of the n
    deliveries performs a constant number of O(log n) heap operations.
    """
    ordered = sorted(deliveries, key=lambda delivery: (delivery.start, delivery.finish, delivery.id))
    free_heap = []
    schedules = []
    for delivery in ordered:
        if free_heap and free_heap[0][0] <= delivery.start:
            _free_time, driver_index = heapq.heappop(free_heap)
        else:
            driver_index = len(schedules)
            schedules.append([])
        schedules[driver_index].append(delivery)
        heapq.heappush(free_heap, (delivery.finish, driver_index))
    return schedules


def minimum_drivers(deliveries: list) -> int:
    """Return the minimum number of drivers needed to accept every delivery."""
    return len(assign_minimum_drivers(deliveries))

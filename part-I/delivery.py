"""Delivery requests and the input-file format."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Delivery:
    """One delivery request.

    Times are integers. A driver who finishes at time t may start another
    delivery at time t, so intervals that only touch at an endpoint are compatible.
    """

    id: str
    start: int
    finish: int

    def __post_init__(self) -> None:
        if not isinstance(self.start, int) or not isinstance(self.finish, int):
            raise ValueError(f"{self.id}: start and finish must be integers")
        if self.start >= self.finish:
            raise ValueError(
                f"{self.id}: start time {self.start} must be < finish time {self.finish}"
            )

    def overlaps(self, other: "Delivery") -> bool:
        """Return True when the two deliveries cannot share a driver."""
        return self.start < other.finish and other.start < self.finish


def load_deliveries(path: str) -> list:
    """Read delivery requests from a text file.

    Each data line has three whitespace-separated fields:

        <id> <start_time> <finish_time>

    Blank lines and lines whose first non-whitespace character is '#' are ignored.
    """
    deliveries = []
    seen = set()
    with open(path, encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError(
                    f"{path}:{line_number}: expected '<id> <start> <finish>', "
                    f"got {raw.rstrip()!r}"
                )
            delivery_id, start_text, finish_text = parts
            try:
                start = int(start_text)
                finish = int(finish_text)
            except ValueError as exc:
                raise ValueError(
                    f"{path}:{line_number}: start and finish must be integers"
                ) from exc
            if delivery_id in seen:
                raise ValueError(f"{path}:{line_number}: duplicate id {delivery_id}")
            seen.add(delivery_id)
            deliveries.append(Delivery(delivery_id, start, finish))
    return deliveries

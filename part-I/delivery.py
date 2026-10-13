"""Delivery requests and the input format."""

import re
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


_INT = re.compile(r"^-?\d+$")
_RANGE = re.compile(r"^(-?\d+)-(-?\d+)$")


def _next_id(seen: set) -> str:
    number = 1
    while f"D{number}" in seen:
        number += 1
    return f"D{number}"


def parse_delivery_line(raw: str, default_id: str):
    """Turn one delivery into a Delivery, or return None for a blank/comment line.

    Accepted forms include:
        D1 1 3
        1 3
        (1, 3)
        D1, 1, 3
        D1 1-3
        1-3
    If the id is left off, default_id is used.
    """
    text = raw.strip()
    if not text or text.startswith("#"):
        return None

    parts = text.replace("(", " ").replace(")", " ").replace(",", " ").replace(":", " ").split()
    if not parts:
        return None

    delivery_id = None
    start = None
    finish = None

    if len(parts) == 1:
        match = _RANGE.fullmatch(parts[0])
        if match:
            delivery_id = default_id
            start, finish = int(match.group(1)), int(match.group(2))
    elif len(parts) == 2:
        match = _RANGE.fullmatch(parts[1])
        if match:
            delivery_id = parts[0]
            start, finish = int(match.group(1)), int(match.group(2))
        elif _INT.fullmatch(parts[0]) and _INT.fullmatch(parts[1]):
            delivery_id = default_id
            start, finish = int(parts[0]), int(parts[1])
    elif len(parts) == 3 and _INT.fullmatch(parts[1]) and _INT.fullmatch(parts[2]):
        delivery_id = parts[0]
        start, finish = int(parts[1]), int(parts[2])

    if delivery_id is None:
        raise ValueError(
            f"could not read a delivery from {text!r}. "
            "Try 'D1 1 3', '1 3', '(1, 3)', or 'D1 1-3'."
        )
    try:
        return Delivery(delivery_id, start, finish)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc


def _pieces(raw: str) -> list:
    """Split a line that has more than one delivery, separated by ; or |."""
    return [piece for piece in re.split(r"[;|]", raw) if piece.strip()]


def parse_deliveries(lines) -> list:
    """Parse an iterable of text lines. Raise ValueError on a bad line."""
    deliveries = []
    seen = set()
    for line_number, raw in enumerate(lines, start=1):
        if not str(raw).strip() or str(raw).strip().startswith("#"):
            continue
        for piece in _pieces(str(raw)):
            try:
                delivery = parse_delivery_line(piece, _next_id(seen))
            except ValueError as exc:
                raise ValueError(f"line {line_number}: {exc}") from exc
            if delivery is None:
                continue
            if delivery.id in seen:
                raise ValueError(f"line {line_number}: duplicate id {delivery.id}")
            seen.add(delivery.id)
            deliveries.append(delivery)
    return deliveries


def load_deliveries(path: str) -> list:
    """Read delivery requests from a text file.

    Each data line is one delivery, or several separated by ';' or '|'.
    Blank lines and lines whose first non-whitespace character is '#' are ignored.
    """
    with open(path, encoding="utf-8") as handle:
        try:
            return parse_deliveries(handle)
        except ValueError as exc:
            raise ValueError(f"{path}: {exc}") from exc

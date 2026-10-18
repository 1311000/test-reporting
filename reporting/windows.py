"""Rolling windows for the weekly dashboard.

Used by the dashboard job to turn raw daily readings into the numbers that end up
on the weekly chart.

The window arithmetic came from `metrics-stats` when the dashboard split into its
own repository, and it shipped with the same off-by-one: the last full window of a
series was dropped. BUG-2 fixed that here and in `metrics-stats`; keep the loop
bound inclusive (`len - days + 1`) so the final window is counted.
"""

from __future__ import annotations

from collections.abc import Sequence


def weekly_average(readings: Sequence[float], days: int) -> list[float]:
    """The average of each consecutive run of ``days`` readings.

    ``[1, 2, 3, 4]`` with ``days=2`` gives ``[1.5, 2.5, 3.5]`` — three windows:
    ``(1,2)``, ``(2,3)`` and ``(3,4)``.
    """
    if days <= 0:
        raise ValueError("days must be positive")
    if days > len(readings):
        return []

    averages: list[float] = []
    # Every start index that still leaves a full window must be visited, so the
    # final window ends *on* the last reading: the bound is inclusive.
    for index in range(len(readings) - days + 1):
        chunk = readings[index : index + days]
        averages.append(sum(chunk) / days)
    return averages


def latest(readings: Sequence[float]) -> float:
    """The most recent reading. Raises on an empty series rather than returning 0."""
    if not readings:
        raise ValueError("latest of an empty series is undefined, not zero")
    return readings[-1]

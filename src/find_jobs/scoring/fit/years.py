"""Shared years-of-experience helpers for fit scoring.

These helpers keep the gap-based years logic consistent across fit modules.
"""

from __future__ import annotations


def score_years_gap(
    years_required: float,
    candidate_years: float,
    gap_bands: tuple[tuple[float, float], ...],
) -> float:
    """Map the years gap to a score using ordered gap bands."""

    if years_required >= 7.0:
        return 0.0

    years_gap = years_required - candidate_years
    for max_gap, score in gap_bands:
        if years_gap <= max_gap:
            return score

    return gap_bands[-1][1]

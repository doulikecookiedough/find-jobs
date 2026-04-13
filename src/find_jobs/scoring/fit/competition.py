"""Competition-fit scoring helpers.

These functions estimate whether a role looks realistic to pursue before adding
stack or domain detail.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.fit.years import score_years_gap


def score_competition_realism(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score whether the role looks realistically competitive to pursue.

    This penalizes seniority and experience stretches even when the work itself
    otherwise looks relevant.
    """
    if job.seniority in {"staff", "principal"}:
        return 0.0
    if job.role_type in profile.avoid_roles:
        return 0.0

    if job.years_experience_required is None:
        return _score_unknown_years_competition(job)

    return score_years_gap(
        job.years_experience_required,
        profile.years_experience,
        (
            (0.0, 1.0),
            (1.0, 0.8),
            (2.0, 0.55),
            (float("inf"), 0.25),
        ),
    )


def _score_unknown_years_competition(job: ParsedJob) -> float:
    """Score competition realism when the job omits an explicit years requirement."""

    if job.seniority == "senior":
        return 0.25
    if job.role_type == "data":
        return 0.3
    if job.role_type == "business-systems":
        return 0.25
    return 0.45

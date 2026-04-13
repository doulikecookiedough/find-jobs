"""Competition-fit scoring helpers.

These functions estimate whether a role looks realistic to pursue before adding
stack or domain detail.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


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
        return _score_competition_without_years(job)

    years_gap = job.years_experience_required - profile.years_experience
    score = 0.25
    if job.years_experience_required >= 7.0:
        score = 0.0
    elif years_gap <= 0:
        score = 1.0
    elif years_gap <= 1.0:
        score = 0.8
    elif years_gap <= 2.0:
        score = 0.55

    return score


def _score_competition_without_years(job: ParsedJob) -> float:
    """Score competition realism when the posting omits explicit years."""

    if job.seniority == "senior":
        return 0.25
    if job.role_type == "data":
        return 0.3
    if job.role_type == "business-systems":
        return 0.25
    return 0.45

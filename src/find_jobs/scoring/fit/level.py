"""Level-fit scoring helpers.

These functions score whether the role's seniority and years requirements are
plausible relative to the candidate profile.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


def score_level_match(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how closely the job level matches the candidate's experience.

    Level mismatch is treated as a strong constraint because it affects both fit
    and the likelihood of getting screened in.
    """
    if job.seniority in {"staff", "principal"}:
        return 0.0

    if job.years_experience_required is None:
        if job.seniority == "senior":
            return 0.35
        if job.seniority == "mid":
            return 0.85
        if job.seniority == "junior":
            return 1.0
        return 0.5

    years_gap = job.years_experience_required - profile.years_experience

    if job.years_experience_required >= 7.0:
        return 0.0
    if years_gap <= 0:
        return 1.0
    if years_gap <= 1.0:
        return 0.85
    if years_gap <= 2.0:
        return 0.65
    if years_gap <= 3.0:
        return 0.35
    return 0.0

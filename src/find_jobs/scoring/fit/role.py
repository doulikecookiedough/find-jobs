"""Role-fit scoring helpers.

These functions score whether the inferred role lane matches the candidate's
preferred or avoided tracks.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


def score_role_type_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how the inferred role type aligns with preferred and avoided tracks.

    Avoided roles get hard penalties while adjacent roles stay neutral rather
    than strongly positive.
    """
    if not job.role_type:
        return 0.5

    if job.role_type in profile.avoid_roles:
        return 0.0
    if job.role_type in profile.preferred_roles:
        return 1.0
    if job.role_type == "data":
        return 0.25
    if job.role_type == "business-systems":
        return 0.15
    return 0.5

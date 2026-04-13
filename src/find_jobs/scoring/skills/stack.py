"""Skills-stack scoring helpers.

These functions score broad technical overlap using the candidate's wider known
technology set rather than only preferred technologies.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.shared import candidate_known_technologies


def score_skills_stack_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score stack overlap using the candidate's broader known technologies.

    This is intentionally wider than fit stack alignment so transferable but
    credible experience still counts.
    """
    if not job.technologies:
        return 0.5

    known_technologies = candidate_known_technologies(profile)
    if not known_technologies:
        return 0.0

    matched_known = len(set(job.technologies).intersection(known_technologies)) / len(set(job.technologies))
    return min(1.0, matched_known)

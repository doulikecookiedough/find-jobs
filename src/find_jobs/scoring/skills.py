"""Skills scoring helpers for technical overlap.

These functions focus on stack evidence rather than broader role fit or
screening realism.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob, ScoreBreakdown
from find_jobs.scoring.shared import candidate_known_technologies


def score_skills_alignment(
    job: ParsedJob,
    profile: CandidateProfile,
    breakdown: ScoreBreakdown,
) -> int:
    """Estimate technical overlap independent of years and seniority fit.

    This combines broad known-stack evidence with the softer domain and strength
    signals already computed for fit.
    """
    weighted_score = (
        score_skills_stack_alignment(job, profile) * 0.60
        + breakdown.strength_alignment * 0.25
        + breakdown.domain_alignment * 0.15
    )
    return round(weighted_score * 100)


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

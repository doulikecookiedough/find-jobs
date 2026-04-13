"""Aggregate skills scoring helpers.

These functions combine stack evidence with the existing fit breakdown to
produce a standalone technical-alignment score.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob, ScoreBreakdown
from find_jobs.scoring.skills.stack import score_skills_stack_alignment


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

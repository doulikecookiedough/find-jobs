"""Fit-stack scoring helpers.

These functions measure direct resonance between the job stack and the
candidate's preferred technologies.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


def score_stack_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score direct overlap between the job stack and preferred technologies.

    This stays narrow so fit reflects explicit stack resonance, not broad resume
    coverage.
    """
    if not job.technologies:
        return 0.5

    preferred_technologies = set(profile.preferred_technologies)
    if not preferred_technologies:
        return 0.0

    matched_technologies = preferred_technologies.intersection(job.technologies)
    return len(matched_technologies) / len(set(job.technologies))

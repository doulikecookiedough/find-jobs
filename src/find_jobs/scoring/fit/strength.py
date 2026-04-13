"""Strength-fit scoring helpers.

These functions map the raw job text onto named candidate strengths using
reviewable regex patterns.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.fit.patterns import STRENGTH_PATTERNS


def score_strength_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score whether the raw job text matches the candidate's strongest themes.

    This acts as a qualitative signal when the job language mirrors known
    strengths such as backend systems or integrations.
    """
    if not profile.strengths:
        return 0.0

    matched_strengths = 0
    for strength in set(profile.strengths):
        pattern = STRENGTH_PATTERNS.get(strength)
        if pattern and pattern.search(job.raw_text):
            matched_strengths += 1

    if matched_strengths == 0:
        return 0.5
    if matched_strengths == 1:
        return 0.7
    if matched_strengths == 2:
        return 0.85
    return 1.0

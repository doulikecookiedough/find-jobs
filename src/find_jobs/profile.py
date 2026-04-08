"""Candidate profile helpers."""

from __future__ import annotations

from find_jobs.models import CandidateProfile


def build_default_candidate_profile() -> CandidateProfile:
    """Return the default candidate profile used for local scoring."""
    return CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend", "platform"],
        preferred_domains=[
            "backend",
            "distributed-systems",
            "event-driven",
            "apis",
            "integrations",
            "observability",
        ],
        preferred_technologies=["python", "java", "aws", "postgresql", "kubernetes"],
        avoid_domains=["mobile", "frontend", "networking"],
        avoid_roles=["frontend", "mobile"],
    )

"""Domain-fit scoring helpers.

These functions compare extracted domain signals against preferred and avoided
areas from the candidate profile.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


def score_domain_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how well the job's domain signals match preferred and avoided areas.

    Preferred domains add confidence while avoided domains suppress the score.
    """
    if not job.domain_signals:
        return 0.5

    job_domains = set(job.domain_signals)
    preferred_domains = set(profile.preferred_domains)
    avoid_domains = set(profile.avoid_domains)

    positive_matches = len(job_domains.intersection(preferred_domains))
    negative_matches = len(job_domains.intersection(avoid_domains))

    if positive_matches == 0 and negative_matches == 0:
        return 0.5
    if negative_matches:
        return max(0.0, (positive_matches - negative_matches) / len(job_domains))
    return positive_matches / len(job_domains)

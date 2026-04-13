"""Domain-fit scoring helpers.

These functions compare extracted domain signals against preferred and avoided
areas from the candidate profile.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.shared import candidate_known_technologies


SPECIALIZED_DOMAINS = {
    "ai-ml",
    "computer-vision",
    "video-processing",
    "model-inference",
}
SPECIALIZED_TECHNOLOGIES = {
    "pytorch",
    "tensorflow",
    "keras",
    "cuda",
    "opencv",
    "ffmpeg",
    "gstreamer",
}


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
    specialized_domains = job_domains.intersection(SPECIALIZED_DOMAINS)

    if positive_matches == 0 and negative_matches == 0:
        base_score = 0.5
    elif negative_matches:
        base_score = max(0.0, (positive_matches - negative_matches) / len(job_domains))
    else:
        base_score = positive_matches / len(job_domains)

    if specialized_domains and not _has_specialized_domain_proof(profile, specialized_domains):
        return min(base_score, 0.35)

    return base_score


def _has_specialized_domain_proof(profile: CandidateProfile, specialized_domains: set[str]) -> bool:
    """Check whether the profile contains credible evidence for specialized domains.

    Specialized domain language should not score as a strong match unless the
    profile shows related domains, strengths, or tools.
    """
    profile_domains = set(profile.preferred_domains)
    if specialized_domains.intersection(profile_domains):
        return True

    profile_strengths = set(profile.strengths)
    if specialized_domains.intersection(profile_strengths):
        return True

    known_technologies = candidate_known_technologies(profile)
    if known_technologies.intersection(SPECIALIZED_TECHNOLOGIES):
        return True

    return False

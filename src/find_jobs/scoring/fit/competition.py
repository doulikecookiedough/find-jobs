"""Competition-fit scoring helpers.

These functions estimate whether a role looks realistic to pursue before adding
stack or domain detail.
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


def score_competition_realism(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score whether the role looks realistically competitive to pursue.

    This penalizes seniority and experience stretches even when the work itself
    otherwise looks relevant.
    """
    if job.seniority in {"staff", "principal"}:
        return 0.0
    if job.role_type in profile.avoid_roles:
        return 0.0

    if job.years_experience_required is None:
        if job.seniority == "senior":
            return 0.25
        if job.role_type == "data":
            return 0.3
        if job.role_type == "business-systems":
            return 0.25
        return 0.45

    years_gap = job.years_experience_required - profile.years_experience

    if job.years_experience_required >= 7.0:
        return 0.0
    if years_gap <= 0:
        base_score = 1.0
    elif years_gap <= 1.0:
        base_score = 0.8
    elif years_gap <= 2.0:
        base_score = 0.55
    else:
        base_score = 0.25

    if _has_unproven_specialized_domain(job, profile):
        return min(base_score, 0.35)

    return base_score


def _has_unproven_specialized_domain(job: ParsedJob, profile: CandidateProfile) -> bool:
    """Check whether a specialized role lacks matching domain proof in the profile.

    Competition realism should drop when the job asks for AI or video-inference
    specialization but the profile does not show relevant domains, strengths, or tools.
    """
    specialized_domains = set(job.domain_signals).intersection(SPECIALIZED_DOMAINS)
    if not specialized_domains:
        return False

    profile_domains = set(profile.preferred_domains)
    if specialized_domains.intersection(profile_domains):
        return False

    profile_strengths = set(profile.strengths)
    if specialized_domains.intersection(profile_strengths):
        return False

    known_technologies = candidate_known_technologies(profile)
    if known_technologies.intersection(SPECIALIZED_TECHNOLOGIES):
        return False

    return True

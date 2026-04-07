"""Scoring logic built on comparison results."""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob


def score_level_match(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how well the job level matches the candidate's experience."""
    if job.seniority in {"staff", "principal"}:
        return 0.0

    if job.years_experience_required is None:
        if job.seniority == "senior":
            return 0.35
        if job.seniority == "mid":
            return 0.85
        if job.seniority == "junior":
            return 1.0
        return 0.5

    years_gap = job.years_experience_required - profile.years_experience

    if job.years_experience_required >= 7.0:
        return 0.0
    if years_gap <= 0:
        return 1.0
    if years_gap <= 1.0:
        return 0.85
    if years_gap <= 2.0:
        return 0.65
    if years_gap <= 3.0:
        return 0.35
    return 0.0


def score_stack_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score technology overlap between a job and the candidate profile."""
    if not job.technologies:
        return 0.5

    preferred_technologies = set(profile.preferred_technologies)
    if not preferred_technologies:
        return 0.0

    matched_technologies = preferred_technologies.intersection(job.technologies)
    return len(matched_technologies) / len(set(job.technologies))


def score_domain_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how well a job's domain signals align with the candidate profile."""
    if not job.domain_signals:
        return 0.5

    job_domains = set(job.domain_signals)
    preferred_domains = set(profile.preferred_domains)
    avoid_domains = set(profile.avoid_domains)

    positive_matches = len(job_domains.intersection(preferred_domains))
    negative_matches = len(job_domains.intersection(avoid_domains))

    if positive_matches == 0 and negative_matches == 0:
        return 0.5

    raw_score = (positive_matches - negative_matches) / len(job_domains)
    return max(0.0, min(1.0, 0.5 + raw_score))


def score_role_type_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how well a job's role type aligns with the candidate profile."""
    if not job.role_type:
        return 0.5

    if job.role_type in profile.avoid_roles:
        return 0.0
    if job.role_type in profile.preferred_roles:
        return 1.0
    return 0.5

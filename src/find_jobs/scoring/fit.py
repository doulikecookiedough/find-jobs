"""Fit scoring helpers for overall job alignment.

These functions score how well the role matches the candidate on level, domain,
role type, strengths, and application realism.
"""

from __future__ import annotations

import re

from find_jobs.models import CandidateProfile, ParsedJob


STRENGTH_PATTERNS = {
    "backend": re.compile(r"\bbackend(?: systems?| services?| infrastructure)?\b", re.IGNORECASE),
    "full-stack": re.compile(r"\bfull[ -]?stack\b|\bfront-end to back-end\b|\bacross the stack\b", re.IGNORECASE),
    "product-engineering": re.compile(
        r"\bproduct decisions?\b|\bcustomer value\b|\bproduct development\b|\bproduct-oriented\b",
        re.IGNORECASE,
    ),
    "data-platforms": re.compile(r"\bdata platforms?\b|\bdata pipelines?\b|\bdata lake\b", re.IGNORECASE),
    "distributed-systems": re.compile(r"\bdistributed systems?\b|\bsystems? that scale\b|\bscalable\b", re.IGNORECASE),
    "data-integrity": re.compile(r"\bdata integrity\b|\bconsistency\b|\bcorrectness\b", re.IGNORECASE),
    "concurrency": re.compile(r"\bconcurr(?:ent|ency)\b|\basynchronous\b|\basync\b", re.IGNORECASE),
    "schema-migrations": re.compile(r"\bschema migrations?\b|\bdatabase migrations?\b|\bdata backfill\b", re.IGNORECASE),
    "apis": re.compile(r"\bapi\b|\bapis\b|\brest apis?\b|\brestful apis?\b", re.IGNORECASE),
    "integrations": re.compile(r"\bintegrations?\b|\bintegration platform\b", re.IGNORECASE),
    "reliability": re.compile(r"\breliability\b|\breliable\b|\bproduction systems?\b|\bon-call\b", re.IGNORECASE),
    "etl": re.compile(r"\betl\b|\bdata ingestion\b|\bdata pipelines?\b", re.IGNORECASE),
    "observability": re.compile(r"\bobservability\b|\bmetrics\b|\blogging\b|\btracing\b", re.IGNORECASE),
    "testing": re.compile(r"\btesting\b|\bunit tests?\b|\bintegration tests?\b|\btestable design\b", re.IGNORECASE),
    "documentation": re.compile(r"\bwell-documented\b|\bdocumentation\b|\bspecifications?\b|\bacceptance criteria\b", re.IGNORECASE),
}


def score_level_match(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how closely the job level matches the candidate's experience.

    Level mismatch is treated as a strong constraint because it affects both fit
    and the likelihood of getting screened in.
    """
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


def score_role_type_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how the inferred role type aligns with preferred and avoided tracks.

    Avoided roles get hard penalties while adjacent roles stay neutral rather
    than strongly positive.
    """
    if not job.role_type:
        return 0.5

    if job.role_type in profile.avoid_roles:
        return 0.0
    if job.role_type in profile.preferred_roles:
        return 1.0
    if job.role_type == "data":
        return 0.25
    if job.role_type == "business-systems":
        return 0.15
    return 0.5


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
        return 1.0
    if years_gap <= 1.0:
        return 0.8
    if years_gap <= 2.0:
        return 0.55
    return 0.25

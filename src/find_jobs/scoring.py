"""Scoring logic built on comparison results."""

from __future__ import annotations

import re

from find_jobs.models import CandidateProfile, JobScore, ParsedJob, ScoreBreakdown


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
    if negative_matches:
        return max(0.0, (positive_matches - negative_matches) / len(job_domains))
    return positive_matches / len(job_domains)


def score_strength_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score how well the raw job text matches the candidate's strongest areas."""
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
    """Score how well a job's role type aligns with the candidate profile."""
    if not job.role_type:
        return 0.5

    if job.role_type in profile.avoid_roles:
        return 0.0
    if job.role_type in profile.preferred_roles:
        return 1.0
    return 0.5


def score_competition_realism(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score whether a job seems realistically worth pursuing."""
    if job.seniority in {"staff", "principal"}:
        return 0.0
    if job.role_type in profile.avoid_roles:
        return 0.0

    if job.years_experience_required is None:
        if job.seniority == "senior":
            return 0.35
        return 0.6

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


def score_job(job: ParsedJob, profile: CandidateProfile) -> JobScore:
    """Calculate a weighted fit score and recommendation for a job."""
    breakdown = ScoreBreakdown(
        level_match=score_level_match(job, profile),
        stack_alignment=score_stack_alignment(job, profile),
        domain_alignment=score_domain_alignment(job, profile),
        strength_alignment=score_strength_alignment(job, profile),
        role_type_alignment=score_role_type_alignment(job, profile),
        competition_realism=score_competition_realism(job, profile),
    )

    weighted_score = (
        breakdown.level_match * 0.30
        + breakdown.stack_alignment * 0.25
        + ((breakdown.domain_alignment + breakdown.strength_alignment) / 2) * 0.15
        + breakdown.role_type_alignment * 0.15
        + breakdown.competition_realism * 0.15
    )

    fit_score = round(weighted_score * 100)
    skills_alignment = _skills_alignment_for_breakdown(job, profile, breakdown)
    interview_probability_min, interview_probability_max = _interview_probability_for_breakdown(
        breakdown,
        fit_score,
        skills_alignment,
        job,
    )
    recommendation = _recommendation_for_score(fit_score)
    priority = _priority_for_score(fit_score)
    reasons, risks = _build_reasons_and_risks(job, profile, breakdown)

    return JobScore(
        fit_score=fit_score,
        skills_alignment=skills_alignment,
        interview_probability_min=interview_probability_min,
        interview_probability_max=interview_probability_max,
        recommendation=recommendation,
        priority=priority,
        reasons=reasons,
        risks=risks,
        score_breakdown=breakdown,
    )


def _skills_alignment_for_breakdown(
    job: ParsedJob,
    profile: CandidateProfile,
    breakdown: ScoreBreakdown,
) -> int:
    """Estimate technical overlap independent of level fit."""
    weighted_score = (
        score_skills_stack_alignment(job, profile) * 0.60
        + breakdown.strength_alignment * 0.25
        + breakdown.domain_alignment * 0.15
    )
    return round(weighted_score * 100)


def _candidate_known_technologies(profile: CandidateProfile) -> set[str]:
    """Return the candidate's broader known technology set."""
    return {
        *profile.primary_languages,
        *profile.secondary_languages,
        *profile.frameworks,
        *profile.cloud_platforms,
        *profile.databases,
        *profile.infrastructure_tools,
        *profile.developer_tools,
        *profile.preferred_technologies,
    }


def score_skills_stack_alignment(job: ParsedJob, profile: CandidateProfile) -> float:
    """Score stack overlap using the candidate's broader known technologies."""
    if not job.technologies:
        return 0.5

    known_technologies = _candidate_known_technologies(profile)
    if not known_technologies:
        return 0.0

    matched_known = len(set(job.technologies).intersection(known_technologies)) / len(set(job.technologies))
    return min(1.0, matched_known)


def _interview_probability_for_breakdown(
    breakdown: ScoreBreakdown,
    fit_score: int,
    skills_alignment: int,
    job: ParsedJob,
) -> tuple[int, int]:
    """Estimate interview probability range from fit and realism."""
    base_probability = (
        fit_score * 0.40
        + skills_alignment * 0.25
        + breakdown.competition_realism * 100 * 0.15
        + breakdown.level_match * 100 * 0.10
        + breakdown.role_type_alignment * 100 * 0.10
    )

    if breakdown.stack_alignment < 0.4:
        base_probability -= 8
    elif breakdown.stack_alignment < 0.6:
        base_probability -= 4

    if 0.0 < breakdown.role_type_alignment < 1.0:
        base_probability -= 4

    if job.seniority == "senior":
        base_probability -= 8
    if job.seniority in {"staff", "principal"}:
        base_probability -= 15
    if job.years_experience_required is not None and job.years_experience_required >= 7.0:
        base_probability -= 20

    center = max(0, min(100, round(base_probability)))
    lower_bound = max(0, center - 5)
    upper_bound = min(100, center + 5)
    return lower_bound, upper_bound


def _recommendation_for_score(fit_score: int) -> str:
    if fit_score >= 80:
        return "apply"
    if fit_score >= 60:
        return "consider"
    return "skip"


def _priority_for_score(fit_score: int) -> str:
    if fit_score >= 80:
        return "high"
    if fit_score >= 55:
        return "medium"
    return "low"


def _build_reasons_and_risks(
    job: ParsedJob,
    profile: CandidateProfile,
    breakdown: ScoreBreakdown,
) -> tuple[list[str], list[str]]:
    reasons: list[str] = []
    risks: list[str] = []

    if breakdown.role_type_alignment >= 1.0 and job.role_type:
        reasons.append(f"Role type aligns well with your target focus ({job.role_type}).")

    if breakdown.strength_alignment >= 0.85:
        reasons.append("Job content matches several of your strongest backend and systems skills.")

    if breakdown.domain_alignment >= 0.75 and job.domain_signals:
        reasons.append("Domain signals overlap well with your preferred backend and integration work.")

    matched_technologies = sorted(set(job.technologies).intersection(profile.preferred_technologies))
    if matched_technologies:
        reasons.append(f"Relevant stack overlap found: {', '.join(matched_technologies[:4])}.")

    if job.work_style_signals and "remote" in job.work_style_signals:
        reasons.append("Work style includes remote flexibility.")

    if job.years_experience_required is not None and job.years_experience_required > profile.years_experience:
        risks.append(
            f"Experience requirement is above your current profile ({job.years_experience_required:g}+ years vs {profile.years_experience:g})."
        )

    if job.seniority == "senior":
        risks.append("Role is explicitly senior-level.")

    if breakdown.stack_alignment < 0.4:
        risks.append("Core stack overlap is limited, so ramp-up may be required.")

    if breakdown.competition_realism <= 0.55:
        risks.append("This may be a stretch role relative to your current experience level.")

    if job.role_type in profile.avoid_roles:
        risks.append(f"Role type is in your avoid list ({job.role_type}).")

    return reasons, risks

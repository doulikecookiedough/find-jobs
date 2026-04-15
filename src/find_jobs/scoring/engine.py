"""Aggregate scoring orchestration.

This module assembles fit, skills, and interview signals into the final
`JobScore` payload returned to the rest of the application.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, JobScore, ParsedJob, ScoreBreakdown
from find_jobs.scoring.fit import (
    score_competition_realism,
    score_domain_alignment,
    score_level_match,
    score_role_type_alignment,
    score_stack_alignment,
    score_strength_alignment,
)
from find_jobs.scoring.fit.patterns import STRENGTH_PATTERNS
from find_jobs.scoring.interview import score_interview_probability
from find_jobs.scoring.shared import format_years
from find_jobs.scoring.specialization import (
    job_requires_inference_infrastructure,
    matched_specialized_domains,
    profile_has_inference_infrastructure_proof,
)
from find_jobs.scoring.skills import score_skills_alignment


def score_job(job: ParsedJob, profile: CandidateProfile) -> JobScore:
    """Calculate the aggregate fit score and supporting recommendation fields.

    This is the single orchestration entrypoint that turns parsed job data into
    the combined score object used by the CLI and API.
    """
    breakdown = ScoreBreakdown(
        level_match=score_level_match(job, profile),
        stack_alignment=score_stack_alignment(job, profile),
        domain_alignment=score_domain_alignment(job, profile),
        strength_alignment=score_strength_alignment(job, profile),
        role_type_alignment=score_role_type_alignment(job, profile),
        competition_realism=score_competition_realism(job, profile),
    )
    breakdown.missing_inference_infra_proof = job_requires_inference_infrastructure(
        job
    ) and not profile_has_inference_infrastructure_proof(profile)
    breakdown.matched_specialized_domains = matched_specialized_domains(job, profile)

    weighted_score = (
        breakdown.level_match * 0.30
        + breakdown.stack_alignment * 0.25
        + ((breakdown.domain_alignment + breakdown.strength_alignment) / 2) * 0.15
        + breakdown.role_type_alignment * 0.15
        + breakdown.competition_realism * 0.15
    )
    if breakdown.missing_inference_infra_proof:
        weighted_score -= 0.10
    if "adtech" in job.domain_signals and "adtech" in profile.preferred_domains:
        weighted_score += 0.05

    fit_score = round(weighted_score * 100)
    skills_alignment = score_skills_alignment(job, profile, breakdown)
    interview_probability_min, interview_probability_max = score_interview_probability(
        breakdown,
        fit_score,
        skills_alignment,
        job,
        profile,
    )
    (
        years_experience_gap,
        years_experience_match_status,
        years_experience_match_label,
    ) = _years_experience_match(job, profile)
    recommendation = _recommendation_for_score(fit_score)
    priority = _priority_for_score(fit_score)
    reasons, risks = _build_reasons_and_risks(job, profile, breakdown)

    return JobScore(
        fit_score=fit_score,
        skills_alignment=skills_alignment,
        interview_probability_min=interview_probability_min,
        interview_probability_max=interview_probability_max,
        years_experience_required=job.years_experience_required,
        candidate_years_experience=profile.years_experience,
        years_experience_gap=years_experience_gap,
        years_experience_match_status=years_experience_match_status,
        years_experience_match_label=years_experience_match_label,
        recommendation=recommendation,
        priority=priority,
        reasons=reasons,
        risks=risks,
        score_breakdown=breakdown,
    )


def _years_experience_match(
    job: ParsedJob, profile: CandidateProfile
) -> tuple[float | None, str, str]:
    """Summarize how closely the experience requirement matches the profile.

    The label is user-facing, so it stays descriptive rather than exposing raw
    thresholds alone.
    """
    if job.years_experience_required is None:
        return None, "unknown", "Experience requirement unclear"

    years_gap = round(max(job.years_experience_required - profile.years_experience, 0.0), 1)
    required_years = format_years(job.years_experience_required)
    candidate_years = format_years(profile.years_experience)

    if years_gap <= 1.0:
        return (
            years_gap,
            "strong",
            (
                f"Strong match: requires about {required_years} years, "
                f"profile is {candidate_years} years."
            ),
        )
    if years_gap <= 3.0:
        return (
            years_gap,
            "close",
            (
                f"Close stretch: requires about {required_years} years, "
                f"profile is {candidate_years} years."
            ),
        )

    return (
        years_gap,
        "stretch",
        (
            f"Far stretch: requires about {required_years} years, "
            f"profile is {candidate_years} years."
        ),
    )


def _recommendation_for_score(fit_score: int) -> str:
    """Map the fit score to an application recommendation band."""
    if fit_score >= 80:
        return "apply"
    if fit_score >= 60:
        return "consider"
    return "skip"


def _priority_for_score(fit_score: int) -> str:
    """Map the fit score to a coarse review priority level."""
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
    """Build human-readable reasons and risks from the score breakdown.

    These lists are meant for review ergonomics, not for additional scoring.
    """
    reasons: list[str] = []
    risks: list[str] = []

    if breakdown.role_type_alignment >= 1.0 and job.role_type:
        reasons.append(f"Role type aligns well with your target focus ({job.role_type}).")

    if breakdown.strength_alignment >= 0.85:
        reasons.append("Job content matches several of your strongest backend and systems skills.")

    product_engineering_pattern = STRENGTH_PATTERNS.get("product-engineering")
    if (
        "product-engineering" in profile.strengths
        and product_engineering_pattern
        and product_engineering_pattern.search(job.raw_text)
    ):
        reasons.append("Role shows startup/product ownership signals that align with your profile.")

    if breakdown.domain_alignment >= 0.75 and job.domain_signals:
        reasons.append(
            "Domain signals overlap well with your preferred backend and integration work."
        )

    if breakdown.matched_specialized_domains:
        matched_domains = ", ".join(breakdown.matched_specialized_domains)
        reasons.append(f"Matched specialization: {matched_domains} experience directly overlaps this role.")

    matched_technologies = sorted(
        set(job.technologies).intersection(profile.preferred_technologies)
    )
    if matched_technologies:
        reasons.append(f"Relevant stack overlap found: {', '.join(matched_technologies[:4])}.")

    if job.work_style_signals and "remote" in job.work_style_signals:
        reasons.append("Work style includes remote flexibility.")

    if (
        job.years_experience_required is not None
        and job.years_experience_required > profile.years_experience
    ):
        risks.append(
            (
                "Experience requirement is above your current profile "
                f"({job.years_experience_required:g}+ years vs "
                f"{profile.years_experience:g})."
            )
        )

    if job.seniority == "senior":
        risks.append("Role is explicitly senior-level.")

    if breakdown.stack_alignment < 0.4:
        risks.append("Core stack overlap is limited, so ramp-up may be required.")

    if breakdown.missing_inference_infra_proof:
        risks.append("Role expects specialized inference or GPU infrastructure experience.")

    if breakdown.competition_realism <= 0.55:
        risks.append("This may be a stretch role relative to your current experience level.")

    if job.role_type == "product-engineering" and job.role_type not in profile.preferred_roles:
        risks.append("Role is centered on product-engineering ownership more than your target focus.")

    if job.role_type in profile.avoid_roles:
        risks.append(f"Role type is in your avoid list ({job.role_type}).")

    return reasons, risks

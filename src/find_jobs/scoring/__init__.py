"""Scoring package entrypoint.

This module keeps the public scoring API stable while the underlying concerns
are split into smaller, reviewable modules.
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
from find_jobs.scoring.shared import format_years
from find_jobs.scoring.skills import score_skills_alignment, score_skills_stack_alignment


def score_job(job: ParsedJob, profile: CandidateProfile) -> JobScore:
    """Calculate the aggregate fit score and supporting recommendation fields."""
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
    skills_alignment = score_skills_alignment(job, profile, breakdown)
    interview_probability_min, interview_probability_max = _interview_probability_for_breakdown(
        breakdown,
        fit_score,
        skills_alignment,
        job,
    )
    years_experience_gap, years_experience_match_status, years_experience_match_label = _years_experience_match(job, profile)
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

def _years_experience_match(job: ParsedJob, profile: CandidateProfile) -> tuple[float | None, str, str]:
    if job.years_experience_required is None:
        return None, "unknown", "Experience requirement unclear"

    years_gap = round(max(job.years_experience_required - profile.years_experience, 0.0), 1)
    required_years = format_years(job.years_experience_required)
    candidate_years = format_years(profile.years_experience)

    if years_gap <= 1.0:
        return (
            years_gap,
            "strong",
            f"Strong match: requires about {required_years} years, profile is {candidate_years} years.",
        )
    if years_gap <= 3.0:
        return (
            years_gap,
            "close",
            f"Close stretch: requires about {required_years} years, profile is {candidate_years} years.",
        )

    return (
        years_gap,
        "stretch",
        f"Far stretch: requires about {required_years} years, profile is {candidate_years} years.",
    )
def _interview_probability_for_breakdown(
    breakdown: ScoreBreakdown,
    fit_score: int,
    skills_alignment: int,
    job: ParsedJob,
) -> tuple[int, int]:
    """Estimate interview probability with a deliberately conservative bias.

    The output is intended to reflect screening odds, not eventual interview
    performance once a candidate is already in process.
    """

    def clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
        return max(lower, min(upper, value))

    base_probability = (
        fit_score * 0.22
        + skills_alignment * 0.10
        + breakdown.competition_realism * 100 * 0.18
        + breakdown.level_match * 100 * 0.25
        + breakdown.role_type_alignment * 100 * 0.25
    )

    multiplier = 1.0
    upper_cap = 100
    required_stack_proof = getattr(
        breakdown,
        "required_stack_proof",
        breakdown.stack_alignment,
    )

    if breakdown.stack_alignment < 0.30:
        base_probability -= 28
        multiplier *= 0.42
    elif breakdown.stack_alignment < 0.50:
        base_probability -= 18
        multiplier *= 0.62
    elif breakdown.stack_alignment < 0.65:
        base_probability -= 10
        multiplier *= 0.82

    if required_stack_proof < 0.25:
        base_probability -= 20
        multiplier *= 0.45
        upper_cap = min(upper_cap, 15)
    elif required_stack_proof < 0.50:
        base_probability -= 12
        multiplier *= 0.68
        upper_cap = min(upper_cap, 20)
    elif required_stack_proof < 0.70:
        base_probability -= 6
        multiplier *= 0.86
        upper_cap = min(upper_cap, 28)

    if breakdown.role_type_alignment < 0.50:
        base_probability -= 16
        multiplier *= 0.68
    elif breakdown.role_type_alignment < 0.80:
        base_probability -= 8
        multiplier *= 0.86

    if breakdown.level_match < 0.50:
        base_probability -= 20
        multiplier *= 0.62
    elif breakdown.level_match < 0.75:
        base_probability -= 10
        multiplier *= 0.82

    if breakdown.competition_realism < 0.30:
        multiplier *= 0.58
    elif breakdown.competition_realism < 0.50:
        multiplier *= 0.74
    elif breakdown.competition_realism < 0.70:
        multiplier *= 0.88

    if job.seniority == "senior":
        base_probability -= 15
        multiplier *= 0.80
    elif job.seniority in {"staff", "principal"}:
        base_probability -= 32
        multiplier *= 0.52
        upper_cap = min(upper_cap, 18)

    if job.years_experience_required is not None:
        years_required = job.years_experience_required
        if years_required >= 10:
            base_probability -= 24
            multiplier *= 0.70
        elif years_required >= 7:
            base_probability -= 18
            multiplier *= 0.80
        elif years_required >= 5:
            base_probability -= 10
            multiplier *= 0.90
    else:
        base_probability -= 8
        multiplier *= 0.78
        upper_cap = min(upper_cap, 18)

    if job.role_type == "data":
        base_probability -= 10
        multiplier *= 0.72
        upper_cap = min(upper_cap, 12)
    elif job.role_type == "business-systems":
        base_probability -= 16
        multiplier *= 0.58
        upper_cap = min(upper_cap, 8)

    if getattr(job, "core_stack_mismatch", False):
        base_probability -= 22
        multiplier *= 0.35
        upper_cap = min(upper_cap, 15)

    if getattr(job, "multiple_core_stack_misses", False):
        base_probability -= 10
        multiplier *= 0.72
        upper_cap = min(upper_cap, 12)

    if getattr(job, "is_stretch_role", False):
        multiplier *= 0.78
        upper_cap = min(upper_cap, 18)

    medium_mismatches = 0
    if breakdown.stack_alignment < 0.65:
        medium_mismatches += 1
    if required_stack_proof < 0.50:
        medium_mismatches += 1
    if breakdown.role_type_alignment < 0.80:
        medium_mismatches += 1
    if breakdown.level_match < 0.75:
        medium_mismatches += 1
    if breakdown.competition_realism < 0.60:
        medium_mismatches += 1

    if medium_mismatches >= 4:
        multiplier *= 0.62
    elif medium_mismatches == 3:
        multiplier *= 0.76
    elif medium_mismatches == 2:
        multiplier *= 0.90

    final_probability = base_probability * multiplier * 0.85
    center = round(clamp(final_probability, 0, upper_cap))

    if center >= 30:
        lower_spread = 7
        upper_spread = 4
    elif center >= 15:
        lower_spread = 6
        upper_spread = 3
    else:
        lower_spread = 4
        upper_spread = 2

    lower_bound = max(0, center - lower_spread)
    upper_bound = min(upper_cap, center + upper_spread)
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

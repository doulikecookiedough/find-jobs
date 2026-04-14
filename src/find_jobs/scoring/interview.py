"""Interview probability scoring helpers.

These functions estimate screening odds using a pessimistic policy that favors
clear evidence over optimistic fit averages.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob, ScoreBreakdown


HARD_BACKEND_TECHNOLOGIES = {
    "java",
    "kafka",
    "cassandra",
    "solr",
    "scala",
    "spring-boot",
}


def score_interview_probability(
    breakdown: ScoreBreakdown,
    fit_score: int,
    skills_alignment: int,
    job: ParsedJob,
    profile: CandidateProfile,
) -> tuple[int, int]:
    """Estimate an interview probability range from fit, skills, and penalties.

    The range reflects cold-application screening odds rather than eventual
    performance once a candidate is already inside the interview process.
    """

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
    base_probability, multiplier, upper_cap = _apply_stack_penalties(
        breakdown,
        required_stack_proof,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_fit_penalties(
        breakdown,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_seniority_penalties(
        job,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_years_penalties(
        job,
        profile,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_role_type_penalties(
        job,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_special_case_penalties(
        job,
        breakdown,
        required_stack_proof,
        base_probability,
        multiplier,
        upper_cap,
    )
    base_probability, multiplier, upper_cap = _apply_full_stack_fundamentals_relief(
        job,
        breakdown,
        required_stack_proof,
        base_probability,
        multiplier,
        upper_cap,
    )
    multiplier = _apply_medium_mismatch_penalty(
        breakdown,
        required_stack_proof,
        multiplier,
    )

    final_probability = base_probability * multiplier * 0.85
    center = round(_clamp(final_probability, 0, upper_cap))
    lower_spread, upper_spread = _spread_for_center(center)

    lower_bound = max(0, center - lower_spread)
    upper_bound = min(upper_cap, center + upper_spread)
    return lower_bound, upper_bound


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    """Clamp a probability-like value to a bounded range."""

    return max(lower, min(upper, value))


def _apply_stack_penalties(
    breakdown: ScoreBreakdown,
    required_stack_proof: float,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply stack overlap and proof penalties."""

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

    return base_probability, multiplier, upper_cap


def _apply_fit_penalties(
    breakdown: ScoreBreakdown,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply fit-based role, level, and competition penalties."""

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

    return base_probability, multiplier, upper_cap


def _apply_seniority_penalties(
    job: ParsedJob,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply seniority-specific screening penalties."""

    if job.seniority == "senior":
        base_probability -= 15
        multiplier *= 0.80
    elif job.seniority in {"staff", "principal"}:
        base_probability -= 32
        multiplier *= 0.52
        upper_cap = min(upper_cap, 18)

    return base_probability, multiplier, upper_cap


def _apply_years_penalties(
    job: ParsedJob,
    profile: CandidateProfile,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply years-of-experience penalties relative to the candidate profile."""

    if job.years_experience_required is None:
        base_probability -= 8
        multiplier *= 0.78
        upper_cap = min(upper_cap, 18)
        return base_probability, multiplier, upper_cap

    years_gap = job.years_experience_required - profile.years_experience
    if years_gap > 3.0:
        base_probability -= 24
        multiplier *= 0.70
    elif years_gap > 2.0:
        base_probability -= 18
        multiplier *= 0.80
    elif years_gap > 1.0:
        base_probability -= 10
        multiplier *= 0.90
    elif years_gap > 0:
        base_probability -= 10
        multiplier *= 0.76
        upper_cap = min(upper_cap, 14)

    return base_probability, multiplier, upper_cap


def _apply_role_type_penalties(
    job: ParsedJob,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply coarse penalties for harder role families."""

    if job.role_type == "data":
        base_probability -= 10
        multiplier *= 0.72
        upper_cap = min(upper_cap, 12)
    elif job.role_type == "business-systems":
        base_probability -= 16
        multiplier *= 0.58
        upper_cap = min(upper_cap, 8)

    return base_probability, multiplier, upper_cap


def _apply_special_case_penalties(
    job: ParsedJob,
    breakdown: ScoreBreakdown,
    required_stack_proof: float,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Apply special-case caps and penalties for explicit mismatch signals."""

    if _has_partial_hard_backend_stack(job, breakdown, required_stack_proof):
        base_probability -= 10
        multiplier *= 0.72
        upper_cap = min(upper_cap, 20)

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

    if breakdown.missing_inference_infra_proof:
        base_probability -= 18
        multiplier *= 0.58
        upper_cap = min(upper_cap, 10)

    return base_probability, multiplier, upper_cap


def _apply_medium_mismatch_penalty(
    breakdown: ScoreBreakdown,
    required_stack_proof: float,
    multiplier: float,
) -> float:
    """Apply an extra multiplier when several medium mismatches stack up."""

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
        return multiplier * 0.62
    if medium_mismatches == 3:
        return multiplier * 0.76
    if medium_mismatches == 2:
        return multiplier * 0.90
    return multiplier


def _apply_full_stack_fundamentals_relief(
    job: ParsedJob,
    breakdown: ScoreBreakdown,
    required_stack_proof: float,
    base_probability: float,
    multiplier: float,
    upper_cap: int,
) -> tuple[float, float, int]:
    """Soften stack pessimism for strong full-stack fundamentals matches.

    This protects startup-style full-stack roles from collapsing to near-zero
    screening odds when the candidate clearly matches on years, systems
    fundamentals, and domain adjacency but not on direct preferred stack proof.
    """
    if job.role_type != "full-stack":
        return base_probability, multiplier, upper_cap
    if breakdown.level_match < 0.85 or breakdown.strength_alignment < 0.85:
        return base_probability, multiplier, upper_cap
    if breakdown.domain_alignment < 0.50 or breakdown.competition_realism < 0.85:
        return base_probability, multiplier, upper_cap
    if breakdown.stack_alignment >= 0.30 or required_stack_proof >= 0.25:
        return base_probability, multiplier, upper_cap

    base_probability += 8
    multiplier *= 1.6
    upper_cap = max(upper_cap, 18)
    return base_probability, multiplier, upper_cap


def _spread_for_center(center: int) -> tuple[int, int]:
    """Return the lower and upper spread for the final probability range."""

    if center >= 30:
        return 7, 4
    if center >= 15:
        return 6, 3
    return 4, 2


def _has_partial_hard_backend_stack(
    job: ParsedJob,
    breakdown: ScoreBreakdown,
    required_stack_proof: float,
) -> bool:
    """Detect backend roles that lean on harder stack evidence than the profile clearly proves.

    These roles should screen harsher than generic backend matches when the stack
    overlap is only partial but the technologies point to a stronger Java/eventing ecosystem.
    """
    if job.role_type != "backend":
        return False
    if breakdown.stack_alignment >= 0.65 or required_stack_proof >= 0.70:
        return False

    technologies = set(job.technologies)
    return bool(technologies.intersection(HARD_BACKEND_TECHNOLOGIES))

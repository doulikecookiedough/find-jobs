"""Interview probability scoring helpers.

These functions estimate screening odds using a pessimistic policy that favors
clear evidence over optimistic fit averages.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob, ScoreBreakdown
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

    if _has_unproven_specialized_domain(job, profile):
        base_probability -= 18
        multiplier *= 0.45
        upper_cap = min(upper_cap, 12)

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


def _has_unproven_specialized_domain(job: ParsedJob, profile: CandidateProfile) -> bool:
    """Detect specialized domains that the current profile does not credibly cover.

    Screening odds should drop sharply when a role is specialized in AI, CV, or
    video inference but the profile lacks matching domain or tool evidence.
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

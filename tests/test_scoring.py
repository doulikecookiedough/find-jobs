"""Scoring tests for fit, skills, and interview calculations."""

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.fit import (
    score_competition_realism as fit_score_competition_realism,
    score_domain_alignment as fit_score_domain_alignment,
    score_level_match as fit_score_level_match,
    score_role_type_alignment as fit_score_role_type_alignment,
    score_stack_alignment as fit_score_stack_alignment,
    score_strength_alignment as fit_score_strength_alignment,
)
from find_jobs.scoring.skills import (
    score_skills_alignment as package_score_skills_alignment,
    score_skills_stack_alignment as package_score_skills_stack_alignment,
)
from find_jobs.scoring import (
    score_job,
    score_competition_realism,
    score_domain_alignment,
    score_interview_probability,
    score_level_match,
    score_role_type_alignment,
    score_skills_alignment,
    score_skills_stack_alignment,
    score_stack_alignment,
    score_strength_alignment,
)


def make_candidate_profile() -> CandidateProfile:
    """Create a test candidate based on creator's profile"""
    return CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend", "platform"],
        preferred_domains=["distributed-systems", "apis", "integrations", "backend"],
        preferred_technologies=["python", "aws", "postgresql", "kubernetes", "java"],
        strengths=[
            "backend",
            "distributed-systems",
            "apis",
            "integrations",
            "reliability",
            "observability",
        ],
        avoid_domains=["mobile", "frontend", "networking", "business-systems"],
        avoid_roles=["mobile", "frontend", "business-systems"],
    )


def test_score_level_match_is_high_for_matching_experience() -> None:
    """Scores a perfect level match when required years equal the profile."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=3.0, seniority="mid")

    assert score_level_match(job, profile) == 1.0


def test_score_level_match_drops_for_small_experience_gap() -> None:
    """Reduces level match for a small but manageable experience gap."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=4.0, seniority="mid")

    assert score_level_match(job, profile) == 0.85


def test_score_level_match_is_zero_for_strong_level_mismatch() -> None:
    """Returns zero level match for clearly overleveled roles."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=7.0, seniority="senior")

    assert score_level_match(job, profile) == 0.0


def test_score_level_match_uses_seniority_when_years_are_missing() -> None:
    """Falls back to seniority when no explicit years requirement is present."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", seniority="senior")

    assert score_level_match(job, profile) == 0.35


def test_score_stack_alignment_is_high_for_strong_overlap() -> None:
    """Gives full stack alignment when all job technologies are preferred."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", technologies=["python", "aws", "postgresql"])

    assert score_stack_alignment(job, profile) == 1.0


def test_score_stack_alignment_is_partial_for_mixed_stack() -> None:
    """Returns a partial stack score when only some technologies overlap."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", technologies=["python", "ruby", "mysql", "aws"])

    assert score_stack_alignment(job, profile) == 0.5


def test_score_stack_alignment_returns_neutral_when_job_stack_is_missing() -> None:
    """Uses a neutral stack score when the parser found no technologies."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job")

    assert score_stack_alignment(job, profile) == 0.5


def test_score_domain_alignment_is_high_for_preferred_domains() -> None:
    """Rewards jobs whose domain signals stay inside preferred areas."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["backend", "apis", "distributed-systems"])

    assert score_domain_alignment(job, profile) == 1.0


def test_score_domain_alignment_returns_neutral_for_unknown_domains() -> None:
    """Keeps domain alignment neutral when signals are neither preferred nor avoided."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["wearables"])

    assert score_domain_alignment(job, profile) == 0.5


def test_score_domain_alignment_drops_for_avoid_domains() -> None:
    """Suppresses domain alignment when the job lands in avoided areas."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["mobile", "frontend"])

    assert score_domain_alignment(job, profile) == 0.0


def test_score_strength_alignment_is_high_for_multiple_matching_strengths() -> None:
    """Scores strength alignment highly when the raw text hits several strengths."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Build backend infrastructure, improve API reliability, and design systems "
            "that scale across multiple integrations."
        )
    )

    assert score_strength_alignment(job, profile) == 1.0


def test_score_strength_alignment_returns_neutral_without_matching_strengths() -> None:
    """Falls back to a neutral strength score when no patterns match."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="Work on wearables partnerships and customer engagement tools.")

    assert score_strength_alignment(job, profile) == 0.5


def test_score_strength_alignment_counts_startup_product_signals() -> None:
    """Matches product-engineering strength on startup ownership language."""
    profile = CandidateProfile(
        years_experience=3.0,
        strengths=["product-engineering"],
    )
    job = ParsedJob(
        raw_text=(
            "Ship code frequently, own meaningful features, and figure things out "
            "independently in a fast-paced environment with AI-augmented development."
        )
    )

    assert score_strength_alignment(job, profile) == 0.7


def test_score_job_surfaces_adtech_reason_when_domain_matches() -> None:
    """Adds a reviewer-facing reason when adtech domain experience overlaps."""

    profile = CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend"],
        preferred_domains=["backend", "adtech"],
        preferred_technologies=["python", "aws"],
        strengths=["backend", "adtech"],
    )
    job = ParsedJob(
        raw_text=(
            "Build backend systems for contextual advertising, ad delivery, and analytics "
            "infrastructure."
        ),
        role_type="backend",
        domain_signals=["backend", "adtech"],
        technologies=["python", "aws"],
    )

    score = score_job(job, profile)

    assert "Role domain aligns with your prior adtech experience." in score.reasons


def test_score_job_rewards_matched_adtech_domain_proof() -> None:
    """Adds a small fit lift when adtech domain proof matches the active profile."""

    base_profile = CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend"],
        preferred_domains=["backend"],
        preferred_technologies=["python", "aws"],
        strengths=["backend"],
    )
    adtech_profile = CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend"],
        preferred_domains=["backend", "adtech"],
        preferred_technologies=["python", "aws"],
        strengths=["backend", "adtech"],
    )
    job = ParsedJob(
        raw_text="Build backend systems for contextual advertising and ad delivery.",
        role_type="backend",
        domain_signals=["backend", "adtech"],
        technologies=["python", "aws"],
    )

    base_score = score_job(job, base_profile)
    adtech_score = score_job(job, adtech_profile)

    assert adtech_score.fit_score > base_score.fit_score


def test_score_job_relieves_interview_pessimism_for_matched_specialized_domains() -> None:
    """Raises interview odds when a niche job domain is proven by the active profile."""

    base_profile = CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend"],
        preferred_domains=["backend"],
        preferred_technologies=["python", "aws"],
        strengths=["backend"],
    )
    adtech_profile = CandidateProfile(
        years_experience=3.0,
        preferred_roles=["backend"],
        preferred_domains=["backend", "adtech"],
        preferred_technologies=["python", "aws"],
        strengths=["backend", "adtech"],
    )
    job = ParsedJob(
        raw_text=(
            "Build backend systems for contextual advertising, ad delivery, and analytics "
            "infrastructure."
        ),
        years_experience_required=4.0,
        role_type="backend",
        domain_signals=["backend", "adtech"],
        technologies=["python", "aws", "mongodb"],
    )

    base_score = score_job(job, base_profile)
    adtech_score = score_job(job, adtech_profile)

    assert adtech_score.interview_probability_max > base_score.interview_probability_max


def test_score_role_type_alignment_is_high_for_preferred_role() -> None:
    """Gives a perfect role-type score for explicitly preferred roles."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="backend")

    assert score_role_type_alignment(job, profile) == 1.0


def test_score_role_type_alignment_is_neutral_for_unknown_role() -> None:
    """Keeps adjacent but non-preferred roles below a strong match."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="data")

    assert score_role_type_alignment(job, profile) == 0.25


def test_score_role_type_alignment_is_zero_for_business_systems_avoid_role() -> None:
    """Zeroes role alignment for business-systems roles in the avoid lane."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="business-systems")

    assert score_role_type_alignment(job, profile) == 0.0


def test_score_role_type_alignment_is_partial_for_product_engineering() -> None:
    """Keeps product-engineering roles below backend while still above a hard avoid."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="product-engineering")

    assert score_role_type_alignment(job, profile) == 0.25


def test_score_role_type_alignment_is_zero_for_avoid_role() -> None:
    """Returns zero role alignment for other explicitly avoided roles."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="frontend")

    assert score_role_type_alignment(job, profile) == 0.0


def test_score_competition_realism_is_high_for_reachable_role() -> None:
    """Treats reachable mid-level backend roles as highly realistic."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="job",
        years_experience_required=3.0,
        seniority="mid",
        role_type="backend",
    )

    assert score_competition_realism(job, profile) == 1.0


def test_score_competition_realism_drops_for_stretch_role() -> None:
    """Reduces competition realism when the role is a moderate stretch."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="job",
        years_experience_required=5.0,
        seniority="senior",
        role_type="backend",
    )

    assert score_competition_realism(job, profile) == 0.55


def test_score_competition_realism_is_zero_for_avoid_role() -> None:
    """Returns zero competition realism for avoided role tracks."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="job",
        years_experience_required=3.0,
        seniority="mid",
        role_type="frontend",
    )

    assert score_competition_realism(job, profile) == 0.0


def test_scoring_package_exports_support_cross_module_calls() -> None:
    """Confirms package exports still compose correctly across split modules."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="Build backend APIs on Python and AWS.",
        years_experience_required=3.0,
        seniority="mid",
        role_type="backend",
        technologies=["python", "aws"],
        domain_signals=["backend", "apis"],
    )

    score = score_job(job, profile)

    assert score_skills_stack_alignment(job, profile) == 1.0
    assert score_skills_alignment(job, profile, score.score_breakdown) >= 80
    assert score_interview_probability(
        score.score_breakdown, score.fit_score, score.skills_alignment, job, profile
    ) == (
        score.interview_probability_min,
        score.interview_probability_max,
    )


def test_fit_package_exports_match_top_level_scoring_exports() -> None:
    """Keeps the dedicated fit package aligned with the public scoring exports."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="Build backend APIs on Python and AWS with distributed systems concerns.",
        years_experience_required=3.0,
        seniority="mid",
        role_type="backend",
        technologies=["python", "aws"],
        domain_signals=["backend", "apis"],
    )

    assert fit_score_level_match(job, profile) == score_level_match(job, profile)
    assert fit_score_stack_alignment(job, profile) == score_stack_alignment(job, profile)
    assert fit_score_domain_alignment(job, profile) == score_domain_alignment(job, profile)
    assert fit_score_strength_alignment(job, profile) == score_strength_alignment(job, profile)
    assert fit_score_role_type_alignment(job, profile) == score_role_type_alignment(job, profile)
    assert fit_score_competition_realism(job, profile) == score_competition_realism(job, profile)


def test_skills_package_exports_match_top_level_scoring_exports() -> None:
    """Keeps the dedicated skills package aligned with the public scoring exports."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="Build backend APIs on Python and AWS.",
        years_experience_required=3.0,
        seniority="mid",
        role_type="backend",
        technologies=["python", "aws"],
        domain_signals=["backend", "apis"],
    )
    score = score_job(job, profile)

    assert package_score_skills_stack_alignment(job, profile) == score_skills_stack_alignment(
        job, profile
    )
    assert package_score_skills_alignment(
        job, profile, score.score_breakdown
    ) == score_skills_alignment(
        job,
        profile,
        score.score_breakdown,
    )


def test_score_job_returns_apply_for_strong_fit() -> None:
    """Produces an apply recommendation for a role with strong alignment everywhere."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="Build reliable backend APIs and distributed systems integrations.",
        years_experience_required=3.0,
        seniority="mid",
        role_type="backend",
        technologies=["python", "aws", "postgresql"],
        domain_signals=["backend", "apis", "distributed-systems"],
    )

    score = score_job(job, profile)

    assert score.fit_score == 100
    assert score.skills_alignment == 100
    assert score.interview_probability_min == 78
    assert score.interview_probability_max == 89
    assert score.years_experience_gap == 0.0
    assert score.years_experience_match_status == "strong"
    assert (
        score.years_experience_match_label
        == "Strong match: requires about 3 years, profile is 3 years."
    )
    assert score.recommendation == "apply"
    assert score.priority == "high"
    assert score.score_breakdown.strength_alignment == 1.0
    assert "Role type aligns well with your target focus (backend)." in score.reasons
    assert any("Relevant stack overlap found:" in reason for reason in score.reasons)
    assert not score.risks


def test_score_job_returns_skip_for_clear_mismatch() -> None:
    """Produces a skip recommendation for an obviously mismatched role."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="job",
        years_experience_required=7.0,
        seniority="senior",
        role_type="frontend",
        technologies=["ruby", "mysql"],
        domain_signals=["mobile", "frontend"],
    )

    score = score_job(job, profile)

    assert score.fit_score < 40
    assert score.skills_alignment < 30
    assert score.interview_probability_max <= 10
    assert score.years_experience_match_status == "stretch"
    assert score.recommendation == "skip"
    assert score.priority == "low"
    assert any("Role type is in your avoid list" in risk for risk in score.risks)


def test_score_job_returns_consider_for_mixed_fit() -> None:
    """Produces a consider recommendation for a mixed but plausible match."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text="job",
        years_experience_required=4.0,
        seniority="mid",
        role_type="platform",
        technologies=["java", "aws", "mysql"],
        domain_signals=["integrations", "wearables"],
    )

    score = score_job(job, profile)

    assert 60 <= score.fit_score < 80
    assert 40 <= score.skills_alignment <= 70
    assert 8 <= score.interview_probability_min <= 16
    assert 10 <= score.interview_probability_max <= 18
    assert score.years_experience_match_status == "strong"
    assert score.recommendation == "consider"
    assert score.priority == "medium"
    assert any(
        "Experience requirement is above your current profile" in risk for risk in score.risks
    )
    assert any(
        "Role type aligns well with your target focus (platform)." in reason
        for reason in score.reasons
    )


def test_score_job_can_show_stronger_skills_than_overall_fit_for_stretch_role() -> None:
    """Allows strong technical overlap even when overall fit stays weak."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Build distributed systems and backend infrastructure in Python on AWS. "
            "Own API reliability and scalable service integrations."
        ),
        years_experience_required=7.0,
        seniority="senior",
        role_type="backend",
        technologies=["python", "aws", "java"],
        domain_signals=["backend", "distributed-systems", "apis"],
    )

    score = score_job(job, profile)

    assert score.fit_score < score.skills_alignment
    assert score.skills_alignment >= 80
    assert 0 <= score.interview_probability_min <= 5
    assert 0 <= score.interview_probability_max <= 10
    assert score.years_experience_match_status == "stretch"


def test_score_job_reduces_interview_odds_for_partial_hard_backend_stack() -> None:
    """Reduces interview odds when a backend role relies on a harder Java/eventing stack."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Backend Java Engineer building scalable APIs, distributed systems, "
            "microservices, and event-streaming services with Kafka."
        ),
        years_experience_required=4.0,
        role_type="backend",
        technologies=["java", "kafka"],
        domain_signals=[
            "distributed-systems",
            "backend",
            "integrations",
            "apis",
            "microservices",
            "event-streaming",
            "ci-cd",
        ],
    )

    score = score_job(job, profile)

    assert score.fit_score >= 70
    assert score.interview_probability_min <= 14
    assert score.interview_probability_max <= 20


def test_score_job_penalizes_four_year_requirement_when_profile_is_one_year_short() -> None:
    """Penalizes interview odds for a four-year role when the profile is still one year short."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Backend Java Engineer building scalable APIs, distributed systems, "
            "microservices, and event-streaming services with Kafka."
        ),
        years_experience_required=4.0,
        role_type="backend",
        technologies=["java", "kafka"],
        domain_signals=[
            "distributed-systems",
            "backend",
            "integrations",
            "apis",
            "microservices",
            "event-streaming",
            "ci-cd",
        ],
    )

    score = score_job(job, profile)

    assert score.years_experience_gap == 1.0
    assert score.interview_probability_min <= 10
    assert score.interview_probability_max <= 16


def test_score_job_does_not_penalize_years_when_profile_meets_requirement() -> None:
    """Keeps years-based interview penalties off when the candidate already meets
    the requirement."""
    profile = CandidateProfile(
        years_experience=5.0,
        preferred_roles=["backend", "platform"],
        preferred_domains=["distributed-systems", "apis", "integrations", "backend"],
        preferred_technologies=["python", "aws", "postgresql", "kubernetes", "java"],
        strengths=[
            "backend",
            "distributed-systems",
            "apis",
            "integrations",
            "reliability",
            "observability",
        ],
        avoid_domains=["mobile", "frontend", "networking", "business-systems"],
        avoid_roles=["mobile", "frontend", "business-systems"],
    )
    job = ParsedJob(
        raw_text="Build backend APIs and distributed systems in Python and AWS.",
        years_experience_required=5.0,
        role_type="backend",
        technologies=["python", "aws"],
        domain_signals=["distributed-systems", "backend", "apis", "integrations"],
    )

    score = score_job(job, profile)

    assert score.years_experience_gap == 0.0
    assert score.interview_probability_min >= 30


def test_score_job_relieves_full_stack_fundamentals_interview_penalty() -> None:
    """Avoids near-zero odds for full-stack roles with strong fundamentals and years fit."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Ship code frequently in a startup environment while building backend APIs, "
            "integrations, and full-stack product features across frontend and backend systems."
        ),
        years_experience_required=2.0,
        role_type="full-stack",
        technologies=["javascript", "react", "mongodb", "git"],
        domain_signals=["backend", "integrations", "apis"],
    )

    score = score_job(job, profile)

    assert score.interview_probability_max >= 6


def test_score_job_marks_small_years_gap_as_close_stretch() -> None:
    """Labels a small experience shortfall as a close stretch."""
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=5.0, seniority="senior")

    score = score_job(job, profile)

    assert score.years_experience_gap == 2.0
    assert score.years_experience_match_status == "close"
    assert (
        score.years_experience_match_label
        == "Close stretch: requires about 5 years, profile is 3 years."
    )


def test_score_job_surfaces_product_engineering_reason_when_present() -> None:
    """Adds a reviewer-facing reason for startup and product ownership alignment."""
    profile = CandidateProfile(
        years_experience=3.0,
        strengths=["product-engineering"],
        preferred_roles=["backend", "platform"],
        preferred_domains=["apis", "integrations", "backend"],
        preferred_technologies=["python", "aws"],
    )
    job = ParsedJob(
        raw_text=(
            "Own meaningful features, ship code frequently, and navigate a fast-paced "
            "environment with AI-augmented development."
        ),
        years_experience_required=2.0,
        role_type="full-stack",
        technologies=["javascript"],
        domain_signals=["apis", "integrations"],
    )

    score = score_job(job, profile)

    assert "Role shows startup/product ownership signals that align with your profile." in score.reasons


def test_score_job_penalizes_missing_inference_infrastructure_proof() -> None:
    """Penalizes specialized inference infrastructure roles without matching profile proof."""
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Build edge inference infrastructure with NVIDIA CUDA, TensorRT, and "
            "Triton Inference Server for AI/ML serving across distributed edge nodes."
        ),
        years_experience_required=3.0,
        role_type="backend",
        technologies=["python", "aws", "kubernetes", "cuda", "tensorrt"],
        domain_signals=[
            "backend",
            "distributed-systems",
            "apis",
            "gpu-computing",
            "model-serving",
            "edge-inference",
            "ml-infrastructure",
        ],
    )

    score = score_job(job, profile)

    assert score.fit_score < 80
    assert score.interview_probability_max <= 10
    assert "Role expects specialized inference or GPU infrastructure experience." in score.risks

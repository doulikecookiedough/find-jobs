from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring import (
    score_job,
    score_competition_realism,
    score_domain_alignment,
    score_level_match,
    score_role_type_alignment,
    score_stack_alignment,
    score_strength_alignment,
)


def make_candidate_profile() -> CandidateProfile:
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
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=3.0, seniority="mid")

    assert score_level_match(job, profile) == 1.0


def test_score_level_match_drops_for_small_experience_gap() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=4.0, seniority="mid")

    assert score_level_match(job, profile) == 0.85


def test_score_level_match_is_zero_for_strong_level_mismatch() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=7.0, seniority="senior")

    assert score_level_match(job, profile) == 0.0


def test_score_level_match_uses_seniority_when_years_are_missing() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", seniority="senior")

    assert score_level_match(job, profile) == 0.35


def test_score_stack_alignment_is_high_for_strong_overlap() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", technologies=["python", "aws", "postgresql"])

    assert score_stack_alignment(job, profile) == 1.0


def test_score_stack_alignment_is_partial_for_mixed_stack() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", technologies=["python", "ruby", "mysql", "aws"])

    assert score_stack_alignment(job, profile) == 0.5


def test_score_stack_alignment_returns_neutral_when_job_stack_is_missing() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job")

    assert score_stack_alignment(job, profile) == 0.5


def test_score_domain_alignment_is_high_for_preferred_domains() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["backend", "apis", "distributed-systems"])

    assert score_domain_alignment(job, profile) == 1.0


def test_score_domain_alignment_returns_neutral_for_unknown_domains() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["wearables"])

    assert score_domain_alignment(job, profile) == 0.5


def test_score_domain_alignment_drops_for_avoid_domains() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", domain_signals=["mobile", "frontend"])

    assert score_domain_alignment(job, profile) == 0.0


def test_score_strength_alignment_is_high_for_multiple_matching_strengths() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(
        raw_text=(
            "Build backend infrastructure, improve API reliability, and design systems "
            "that scale across multiple integrations."
        )
    )

    assert score_strength_alignment(job, profile) == 1.0


def test_score_strength_alignment_returns_neutral_without_matching_strengths() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="Work on wearables partnerships and customer engagement tools.")

    assert score_strength_alignment(job, profile) == 0.5


def test_score_role_type_alignment_is_high_for_preferred_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="backend")

    assert score_role_type_alignment(job, profile) == 1.0


def test_score_role_type_alignment_is_neutral_for_unknown_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="data")

    assert score_role_type_alignment(job, profile) == 0.25


def test_score_role_type_alignment_is_zero_for_business_systems_avoid_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="business-systems")

    assert score_role_type_alignment(job, profile) == 0.0


def test_score_role_type_alignment_is_zero_for_avoid_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", role_type="frontend")

    assert score_role_type_alignment(job, profile) == 0.0


def test_score_competition_realism_is_high_for_reachable_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=3.0, seniority="mid", role_type="backend")

    assert score_competition_realism(job, profile) == 1.0


def test_score_competition_realism_drops_for_stretch_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=5.0, seniority="senior", role_type="backend")

    assert score_competition_realism(job, profile) == 0.55


def test_score_competition_realism_is_zero_for_avoid_role() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=3.0, seniority="mid", role_type="frontend")

    assert score_competition_realism(job, profile) == 0.0


def test_score_job_returns_apply_for_strong_fit() -> None:
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
    assert score.years_experience_match_label == "Strong match: requires about 3 years, profile is 3 years."
    assert score.recommendation == "apply"
    assert score.priority == "high"
    assert score.score_breakdown.strength_alignment == 1.0
    assert "Role type aligns well with your target focus (backend)." in score.reasons
    assert any("Relevant stack overlap found:" in reason for reason in score.reasons)
    assert score.risks == []


def test_score_job_returns_skip_for_clear_mismatch() -> None:
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
    assert 20 <= score.interview_probability_min <= 30
    assert score.years_experience_match_status == "strong"
    assert score.recommendation == "consider"
    assert score.priority == "medium"
    assert any("Experience requirement is above your current profile" in risk for risk in score.risks)
    assert any("Role type aligns well with your target focus (platform)." in reason for reason in score.reasons)


def test_score_job_can_show_stronger_skills_than_overall_fit_for_stretch_role() -> None:
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


def test_score_job_marks_small_years_gap_as_close_stretch() -> None:
    profile = make_candidate_profile()
    job = ParsedJob(raw_text="job", years_experience_required=5.0, seniority="senior")

    score = score_job(job, profile)

    assert score.years_experience_gap == 2.0
    assert score.years_experience_match_status == "close"
    assert score.years_experience_match_label == "Close stretch: requires about 5 years, profile is 3 years."

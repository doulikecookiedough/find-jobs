"""Comparison tests for parsed job evaluation against the default profile."""

from pathlib import Path

from find_jobs.comparison import evaluate_job_text
from find_jobs.profile import build_default_candidate_profile


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    """Load a parser fixture file by name."""
    return (FIXTURES_DIR / name).read_text()


def test_evaluate_job_text_returns_parsed_job_and_score_for_affirm() -> None:
    """Returns a strong backend match for the Affirm fixture."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("affirm_backend_engineer.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Affirm"
    assert parsed_job.role_type == "backend"
    assert job_score.fit_score >= 80
    assert job_score.recommendation == "apply"
    assert job_score.priority == "high"
    assert not job_score.missing_fields
    assert not job_score.parser_warnings


def test_evaluate_job_text_returns_mixed_fit_for_zepp() -> None:
    """Returns a mixed result for the Zepp full-stack fixture."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("zepp_connected_partnerships.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Zepp Health"
    assert parsed_job.role_type == "full-stack"
    assert 40 <= job_score.fit_score < 80
    assert job_score.recommendation in {"consider", "skip"}


def test_evaluate_job_text_surfaces_missing_field_diagnostics() -> None:
    """Keeps diagnostics empty when the parser recovers all key fields."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("berkeley_payments_senior_backend.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.title == "Senior Software Engineer"
    assert not job_score.missing_fields
    assert not job_score.parser_warnings


def test_evaluate_job_text_returns_apply_for_stripe_with_strength_alignment() -> None:
    """Returns an apply result when Stripe aligns strongly on fit signals."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("stripe_backend_engineer.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Stripe"
    assert parsed_job.role_type == "backend"
    assert job_score.fit_score >= 80
    assert job_score.recommendation == "apply"
    assert job_score.score_breakdown.level_match == 1.0
    assert job_score.score_breakdown.strength_alignment == 1.0
    assert job_score.score_breakdown.competition_realism == 1.0


def test_evaluate_job_text_returns_low_probability_stretch_for_narvar() -> None:
    """Keeps interview odds low for a senior distributed-systems stretch role."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("narvar_distributed_systems.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Narvar"
    assert parsed_job.years_experience_required == 7.0
    assert parsed_job.seniority == "senior"
    assert job_score.skills_alignment >= 60
    assert job_score.fit_score <= 50
    assert job_score.interview_probability_max <= 30
    assert job_score.skills_alignment > job_score.fit_score
    assert job_score.recommendation in {"consider", "skip"}


def test_evaluate_job_text_returns_balanced_midlevel_fit_for_workleap() -> None:
    """Returns a balanced consider result for the Workleap fixture."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("workleap_sharegate_protect.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Workleap"
    assert parsed_job.role_type == "full-stack"
    assert parsed_job.years_experience_required == 3.0
    assert 65 <= job_score.fit_score <= 80
    assert 60 <= job_score.skills_alignment <= 75
    assert 0 <= job_score.interview_probability_min <= 15
    assert 0 <= job_score.interview_probability_max <= 15
    assert job_score.recommendation == "consider"


def test_evaluate_job_text_recovers_wellfound_picovoice_fields() -> None:
    """Recovers key fields even from the noisier Wellfound fixture layout."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("picovoice_wellfound.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Picovoice"
    assert parsed_job.location == "Vancouver"
    assert parsed_job.years_experience_required == 2.0
    assert parsed_job.role_type is None
    assert "aws" in parsed_job.technologies
    assert "python" in parsed_job.technologies
    assert "years_experience_required" not in job_score.missing_fields
    assert "role_type" in job_score.missing_fields


def test_evaluate_job_text_filters_down_data_engineer_screening_odds() -> None:
    """Filters down screening odds for a data role outside the target lane."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("coalition_data_engineer_security.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.title == "Data Engineer, Security"
    assert parsed_job.company == "Coalition, Inc."
    assert parsed_job.role_type == "data"
    assert parsed_job.years_experience_required is None
    assert "go" not in parsed_job.technologies
    assert job_score.fit_score <= 45
    assert job_score.interview_probability_max <= 2
    assert job_score.recommendation == "skip"


def test_evaluate_job_text_filters_down_business_systems_roles() -> None:
    """Filters down business-systems roles that sit in the avoid lane."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("surveymonkey_zuora_developer.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.title == "Zuora Developer"
    assert parsed_job.company == "SurveyMonkey"
    assert parsed_job.role_type == "business-systems"
    assert "zuora" in parsed_job.technologies
    assert "salesforce" in parsed_job.technologies
    assert job_score.fit_score <= 40
    assert job_score.interview_probability_max <= 5
    assert job_score.recommendation == "skip"


def test_evaluate_job_text_aligns_with_real_screening_case_for_versaterm() -> None:
    """Keeps a strong but realistic backend result for the Versaterm fixture."""

    parsed_job, job_score = evaluate_job_text(
        load_fixture("versaterm_se2_dems.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.title == "Software Engineer II - DEMS"
    assert parsed_job.company == "Versaterm"
    assert parsed_job.years_experience_required == 2.0
    assert parsed_job.role_type == "backend"
    assert job_score.fit_score >= 80
    assert job_score.skills_alignment >= 75
    assert 14 <= job_score.interview_probability_min <= 20
    assert 14 <= job_score.interview_probability_max <= 20
    assert job_score.recommendation in {"consider", "apply"}

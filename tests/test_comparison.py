from pathlib import Path

from find_jobs.comparison import evaluate_job_text
from find_jobs.profile import build_default_candidate_profile


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


def test_evaluate_job_text_returns_parsed_job_and_score_for_affirm() -> None:
    parsed_job, job_score = evaluate_job_text(
        load_fixture("affirm_backend_engineer.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Affirm"
    assert parsed_job.role_type == "backend"
    assert job_score.fit_score >= 80
    assert job_score.recommendation == "apply"
    assert job_score.priority == "high"
    assert job_score.missing_fields == []
    assert job_score.parser_warnings == []


def test_evaluate_job_text_returns_mixed_fit_for_zepp() -> None:
    parsed_job, job_score = evaluate_job_text(
        load_fixture("zepp_connected_partnerships.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Zepp Health"
    assert parsed_job.role_type == "full-stack"
    assert 40 <= job_score.fit_score < 80
    assert job_score.recommendation in {"consider", "skip"}


def test_evaluate_job_text_surfaces_missing_field_diagnostics() -> None:
    parsed_job, job_score = evaluate_job_text(
        load_fixture("berkeley_payments_senior_backend.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.title == "Senior Software Engineer"
    assert job_score.missing_fields == []
    assert job_score.parser_warnings == []


def test_evaluate_job_text_returns_apply_for_stripe_with_strength_alignment() -> None:
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

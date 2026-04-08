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


def test_evaluate_job_text_returns_mixed_fit_for_zepp() -> None:
    parsed_job, job_score = evaluate_job_text(
        load_fixture("zepp_connected_partnerships.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Zepp Health"
    assert parsed_job.role_type == "full-stack"
    assert 40 <= job_score.fit_score < 80
    assert job_score.recommendation in {"consider", "skip"}


def test_evaluate_job_text_returns_consider_for_stripe_under_current_rules() -> None:
    parsed_job, job_score = evaluate_job_text(
        load_fixture("stripe_backend_engineer.txt"),
        build_default_candidate_profile(),
    )

    assert parsed_job.company == "Stripe"
    assert parsed_job.role_type == "backend"
    assert 70 <= job_score.fit_score < 80
    assert job_score.recommendation == "consider"
    assert job_score.score_breakdown.level_match == 1.0
    assert job_score.score_breakdown.competition_realism == 1.0

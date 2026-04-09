import json

from find_jobs.comparison import evaluate_job_text
from find_jobs.models import CandidateProfile


def test_incomplete_evaluation_is_logged(monkeypatch, tmp_path) -> None:
    log_path = tmp_path / "incomplete.jsonl"
    monkeypatch.setenv("FIND_JOBS_INCOMPLETE_LOG_PATH", str(log_path))

    profile = CandidateProfile(years_experience=3.0)
    parsed_job, job_score = evaluate_job_text("Wearables role with no clear company or stack.", profile)

    assert parsed_job.company is None
    assert log_path.exists()

    payload = json.loads(log_path.read_text().strip())
    assert payload["missing_fields"]
    assert payload["parser_warnings"]
    assert payload["raw_text"] == "Wearables role with no clear company or stack."
    assert payload["recommendation"] == job_score.recommendation


def test_complete_evaluation_is_not_logged(monkeypatch, tmp_path) -> None:
    log_path = tmp_path / "incomplete.jsonl"
    monkeypatch.setenv("FIND_JOBS_INCOMPLETE_LOG_PATH", str(log_path))

    profile = CandidateProfile(years_experience=3.0)
    evaluate_job_text(
        (
            "Software Engineer, Backend\n"
            "Remote Canada\n"
            "Affirm is hiring.\n"
            "You have 3+ years of experience.\n"
            "Backend systems with Python, AWS, PostgreSQL, and Kubernetes."
        ),
        profile,
    )

    assert not log_path.exists()

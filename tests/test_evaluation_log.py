import json
from pathlib import Path

from find_jobs.comparison import evaluate_job_text
from find_jobs.models import CandidateProfile
from find_jobs.profile import build_default_candidate_profile


def test_incomplete_evaluation_is_logged(monkeypatch, tmp_path) -> None:
    log_path = tmp_path / "incomplete.jsonl"
    monkeypatch.setenv("FIND_JOBS_INCOMPLETE_LOG_PATH", str(log_path))

    profile = CandidateProfile(years_experience=3.0)
    parsed_job, job_score = evaluate_job_text(
        "Wearables role with no clear company or stack.", profile
    )

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


def test_high_interview_evaluation_is_logged(monkeypatch, tmp_path) -> None:
    log_path = tmp_path / "high_interview.jsonl"
    monkeypatch.setenv("FIND_JOBS_HIGH_INTERVIEW_LOG_PATH", str(log_path))

    raw_text = Path("tests/fixtures/versaterm_se2_dems.txt").read_text(encoding="utf8")
    parsed_job, job_score = evaluate_job_text(
        raw_text, build_default_candidate_profile()
    )

    assert parsed_job.company == "Versaterm"
    assert job_score.interview_probability_max >= 20
    assert log_path.exists()

    payload = json.loads(log_path.read_text().strip())
    assert payload["company"] == "Versaterm"
    assert payload["interview_probability_max"] == job_score.interview_probability_max
    assert payload["skills_alignment"] == job_score.skills_alignment
    assert payload["raw_text"].startswith("Software Engineer II - DEMS")


def test_below_threshold_interview_evaluation_is_not_logged(
    monkeypatch, tmp_path
) -> None:
    log_path = tmp_path / "high_interview.jsonl"
    monkeypatch.setenv("FIND_JOBS_HIGH_INTERVIEW_LOG_PATH", str(log_path))

    profile = CandidateProfile(years_experience=3.0)
    evaluate_job_text(
        (
            "Sr. Software Engineer II (Distributed Systems)\n"
            "Narvar\n"
            "Canada\n"
            "You have 7+ years of experience as a software engineer working on distributed systems.\n"
            "Deep hands-on expertise in Python, Go, or Java.\n"
            "Experience with AWS, APIs, Postgres, Redis, DynamoDB, and scalable cloud systems.\n"
        ),
        profile,
    )

    assert not log_path.exists()

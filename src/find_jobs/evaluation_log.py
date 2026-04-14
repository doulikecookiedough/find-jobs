"""Logging helpers for evaluation review queues."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from find_jobs.models import JobScore, ParsedJob


DEFAULT_INCOMPLETE_LOG_PATH = Path("logs/incomplete_evaluations.jsonl")
DEFAULT_COMPLETE_LOG_PATH = Path("logs/complete_evaluations.jsonl")
DEFAULT_HIGH_INTERVIEW_LOG_PATH = Path("logs/high_interview_evaluations.jsonl")
DEFAULT_HIGH_INTERVIEW_THRESHOLD = 20


def _build_payload(parsed_job: ParsedJob, job_score: JobScore) -> dict[str, object]:
    return {
        "logged_at": datetime.now(UTC).isoformat(),
        "title": parsed_job.title,
        "company": parsed_job.company,
        "location": parsed_job.location,
        "fit_score": job_score.fit_score,
        "skills_alignment": job_score.skills_alignment,
        "interview_probability_min": job_score.interview_probability_min,
        "interview_probability_max": job_score.interview_probability_max,
        "recommendation": job_score.recommendation,
        "priority": job_score.priority,
        "missing_fields": job_score.missing_fields,
        "parser_warnings": job_score.parser_warnings,
        "raw_text": parsed_job.raw_text,
    }


def _append_log(log_path: Path, payload: dict[str, object]) -> Path:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload) + "\n")

    return log_path


def log_incomplete_evaluation(parsed_job: ParsedJob, job_score: JobScore) -> Path | None:
    """Persist incomplete parse details for later parser/scorer review."""
    if not job_score.missing_fields and not job_score.parser_warnings:
        return None

    log_path = Path(
        os.environ.get("FIND_JOBS_INCOMPLETE_LOG_PATH", DEFAULT_INCOMPLETE_LOG_PATH),
    )
    return _append_log(log_path, _build_payload(parsed_job, job_score))


def log_complete_evaluation(parsed_job: ParsedJob, job_score: JobScore) -> Path:
    """Persist every completed evaluation for later calibration review."""

    log_path = Path(
        os.environ.get("FIND_JOBS_COMPLETE_LOG_PATH", DEFAULT_COMPLETE_LOG_PATH),
    )
    return _append_log(log_path, _build_payload(parsed_job, job_score))


def log_high_interview_evaluation(parsed_job: ParsedJob, job_score: JobScore) -> Path | None:
    """Persist high-interview-likelihood evaluations for calibration review."""
    threshold = int(
        os.environ.get(
            "FIND_JOBS_HIGH_INTERVIEW_THRESHOLD",
            DEFAULT_HIGH_INTERVIEW_THRESHOLD,
        ),
    )
    if job_score.interview_probability_max < threshold:
        return None

    log_path = Path(
        os.environ.get("FIND_JOBS_HIGH_INTERVIEW_LOG_PATH", DEFAULT_HIGH_INTERVIEW_LOG_PATH),
    )
    return _append_log(log_path, _build_payload(parsed_job, job_score))

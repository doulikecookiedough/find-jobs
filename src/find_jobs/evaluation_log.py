"""Logging helpers for incomplete job evaluations."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

from find_jobs.models import JobScore, ParsedJob


DEFAULT_LOG_PATH = Path("logs/incomplete_evaluations.jsonl")


def log_incomplete_evaluation(parsed_job: ParsedJob, job_score: JobScore) -> Path | None:
    """Persist incomplete parse details for later parser/scorer review."""
    if not job_score.missing_fields and not job_score.parser_warnings:
        return None

    log_path = Path(os.environ.get("FIND_JOBS_INCOMPLETE_LOG_PATH", DEFAULT_LOG_PATH))
    log_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "logged_at": datetime.now(UTC).isoformat(),
        "title": parsed_job.title,
        "company": parsed_job.company,
        "location": parsed_job.location,
        "fit_score": job_score.fit_score,
        "recommendation": job_score.recommendation,
        "missing_fields": job_score.missing_fields,
        "parser_warnings": job_score.parser_warnings,
        "raw_text": parsed_job.raw_text,
    }

    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload) + "\n")

    return log_path

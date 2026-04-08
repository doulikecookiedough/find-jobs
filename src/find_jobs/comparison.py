"""Comparison logic between raw job text, parsed jobs, and candidate profiles."""

from __future__ import annotations

from find_jobs.models import CandidateProfile, JobScore, ParsedJob
from find_jobs.parser import parse_job_description
from find_jobs.scoring import score_job


def evaluate_job_text(raw_text: str, profile: CandidateProfile) -> tuple[ParsedJob, JobScore]:
    """Parse raw job text and return both the parsed job and its score."""
    parsed_job = parse_job_description(raw_text)
    job_score = score_job(parsed_job, profile)
    return parsed_job, job_score

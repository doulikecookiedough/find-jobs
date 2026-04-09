"""Comparison logic between raw job text, parsed jobs, and candidate profiles."""

from __future__ import annotations

from find_jobs.evaluation_log import log_incomplete_evaluation
from find_jobs.models import CandidateProfile, JobScore, ParsedJob
from find_jobs.parser import parse_job_description
from find_jobs.scoring import score_job


def evaluate_job_text(raw_text: str, profile: CandidateProfile) -> tuple[ParsedJob, JobScore]:
    """Parse raw job text and return both the parsed job and its score."""
    parsed_job = parse_job_description(raw_text)
    job_score = score_job(parsed_job, profile)
    job_score.missing_fields = _collect_missing_fields(parsed_job)
    job_score.parser_warnings = _build_parser_warnings(parsed_job, job_score.missing_fields)
    log_incomplete_evaluation(parsed_job, job_score)
    return parsed_job, job_score


def _collect_missing_fields(parsed_job: ParsedJob) -> list[str]:
    missing_fields: list[str] = []

    if parsed_job.title is None:
        missing_fields.append("title")
    if parsed_job.company is None:
        missing_fields.append("company")
    if parsed_job.location is None:
        missing_fields.append("location")
    if parsed_job.years_experience_required is None:
        missing_fields.append("years_experience_required")
    if parsed_job.role_type is None:
        missing_fields.append("role_type")
    if not parsed_job.technologies:
        missing_fields.append("technologies")

    return missing_fields


def _build_parser_warnings(parsed_job: ParsedJob, missing_fields: list[str]) -> list[str]:
    warnings: list[str] = []

    if "title" in missing_fields:
        warnings.append("No clear title was detected from the job description.")
    if "company" in missing_fields:
        warnings.append("No company name was detected from the job description.")
    if "years_experience_required" in missing_fields:
        warnings.append("No years-of-experience requirement was detected.")
    if "role_type" in missing_fields:
        warnings.append("No role type could be inferred confidently.")
    if "technologies" in missing_fields:
        warnings.append("No technologies were extracted, so stack scoring may be less reliable.")
    if parsed_job.title and parsed_job.title == "Unknown":
        warnings.append("Title was normalized to an unknown fallback value.")

    return warnings

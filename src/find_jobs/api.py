"""FastAPI application for job evaluation."""

from __future__ import annotations

from fastapi import Body, FastAPI
from pydantic import BaseModel

from find_jobs.comparison import evaluate_job_text
from find_jobs.profile import build_default_candidate_profile


app = FastAPI(title="find-jobs")


class EvaluateJobRequest(BaseModel):
    job_text: str


class EvaluateJobResponse(BaseModel):
    title: str | None
    company: str | None
    location: str | None
    fit_score: int
    skills_alignment: int
    interview_probability_min: int
    interview_probability_max: int
    recommendation: str
    priority: str
    reasons: list[str]
    risks: list[str]
    missing_fields: list[str]
    parser_warnings: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health endpoint for local development."""
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluateJobResponse)
def evaluate(request: EvaluateJobRequest) -> EvaluateJobResponse:
    """Evaluate raw job text using the default candidate profile."""
    return _evaluate_job_text(request.job_text)


@app.post("/evaluate-text", response_model=EvaluateJobResponse)
def evaluate_text(job_text: str = Body(..., media_type="text/plain")) -> EvaluateJobResponse:
    """Evaluate raw job text from a plain-text request body."""
    return _evaluate_job_text(job_text)


def _evaluate_job_text(job_text: str) -> EvaluateJobResponse:
    """Shared evaluator used by both JSON and plain-text endpoints."""
    parsed_job, job_score = evaluate_job_text(
        job_text,
        build_default_candidate_profile(),
    )
    return EvaluateJobResponse(
        title=parsed_job.title,
        company=parsed_job.company,
        location=parsed_job.location,
        fit_score=job_score.fit_score,
        skills_alignment=job_score.skills_alignment,
        interview_probability_min=job_score.interview_probability_min,
        interview_probability_max=job_score.interview_probability_max,
        recommendation=job_score.recommendation,
        priority=job_score.priority,
        reasons=job_score.reasons,
        risks=job_score.risks,
        missing_fields=job_score.missing_fields,
        parser_warnings=job_score.parser_warnings,
    )

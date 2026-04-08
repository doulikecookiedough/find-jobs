"""FastAPI application for job evaluation."""

from __future__ import annotations

from fastapi import FastAPI
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
    recommendation: str
    priority: str
    reasons: list[str]
    risks: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health endpoint for local development."""
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluateJobResponse)
def evaluate(request: EvaluateJobRequest) -> EvaluateJobResponse:
    """Evaluate raw job text using the default candidate profile."""
    parsed_job, job_score = evaluate_job_text(
        request.job_text,
        build_default_candidate_profile(),
    )
    return EvaluateJobResponse(
        title=parsed_job.title,
        company=parsed_job.company,
        location=parsed_job.location,
        fit_score=job_score.fit_score,
        recommendation=job_score.recommendation,
        priority=job_score.priority,
        reasons=job_score.reasons,
        risks=job_score.risks,
    )

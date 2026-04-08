"""FastAPI application for job evaluation."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(title="find-jobs")


@app.get("/health")
def health() -> dict[str, str]:
    """Simple health endpoint for local development."""
    return {"status": "ok"}

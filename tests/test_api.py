from pathlib import Path

from fastapi.testclient import TestClient

from find_jobs.api import app


client = TestClient(app)
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_evaluate_returns_scored_job_summary() -> None:
    response = client.post(
        "/evaluate",
        json={"job_text": (FIXTURES_DIR / "affirm_backend_engineer.txt").read_text()},
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "Software Engineer II, Backend (Consumer Authentication)",
        "company": "Affirm",
        "location": "Remote Canada",
        "fit_score": 85,
        "recommendation": "apply",
        "priority": "high",
        "reasons": [
            "Role type aligns well with your target focus (backend).",
            "Job content matches several of your strongest backend and systems skills.",
            "Relevant stack overlap found: aws, kubernetes, python.",
            "Work style includes remote flexibility.",
        ],
        "risks": [],
    }

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
        "skills_alignment": 67,
        "interview_probability_min": 91,
        "interview_probability_max": 100,
        "recommendation": "apply",
        "priority": "high",
        "reasons": [
            "Role type aligns well with your target focus (backend).",
            "Job content matches several of your strongest backend and systems skills.",
            "Relevant stack overlap found: aws, kubernetes, python.",
            "Work style includes remote flexibility.",
        ],
        "risks": [],
        "missing_fields": [],
        "parser_warnings": [],
    }


def test_evaluate_text_returns_scored_job_summary_for_plain_text_body() -> None:
    response = client.post(
        "/evaluate-text",
        content=(FIXTURES_DIR / "affirm_backend_engineer.txt").read_text(),
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["title"] == "Software Engineer II, Backend (Consumer Authentication)"
    assert payload["company"] == "Affirm"
    assert payload["fit_score"] == 85
    assert payload["skills_alignment"] == 67
    assert payload["interview_probability_min"] == 91
    assert payload["interview_probability_max"] == 100
    assert payload["recommendation"] == "apply"
    assert payload["priority"] == "high"
    assert payload["missing_fields"] == []
    assert payload["parser_warnings"] == []


def test_evaluate_text_returns_validation_error_for_missing_plain_text_body() -> None:
    response = client.post("/evaluate-text", content="", headers={"Content-Type": "text/plain"})

    assert response.status_code == 422


def test_evaluate_returns_validation_error_when_job_text_is_missing() -> None:
    response = client.post("/evaluate", json={})

    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"][0]["loc"] == ["body", "job_text"]
    assert payload["detail"][0]["type"] == "missing"


def test_evaluate_returns_validation_error_for_wrong_job_text_type() -> None:
    response = client.post("/evaluate", json={"job_text": 123})

    assert response.status_code == 422

    payload = response.json()
    assert payload["detail"][0]["loc"] == ["body", "job_text"]


def test_evaluate_returns_consider_case_with_reasons_and_risks() -> None:
    response = client.post(
        "/evaluate",
        json={"job_text": (FIXTURES_DIR / "berkeley_payments_senior_backend.txt").read_text()},
    )

    assert response.status_code == 200

    payload = response.json()
    assert payload["title"] == "Senior Software Engineer"
    assert payload["company"] == "Berkeley Payments"
    assert payload["fit_score"] == 62
    assert 45 <= payload["skills_alignment"] <= 65
    assert payload["interview_probability_min"] >= 35
    assert payload["interview_probability_max"] <= 65
    assert payload["recommendation"] == "consider"
    assert payload["priority"] == "medium"
    assert any("Role type aligns well with your target focus (backend)." == reason for reason in payload["reasons"])
    assert any("Role is explicitly senior-level." == risk for risk in payload["risks"])
    assert payload["missing_fields"] == []
    assert payload["parser_warnings"] == []

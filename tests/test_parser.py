from pathlib import Path

from find_jobs.parser import parse_job_description


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_parse_job_description_extracts_direct_fields() -> None:
    raw_text = (FIXTURES_DIR / "affirm_backend_engineer.txt").read_text()

    parsed_job = parse_job_description(raw_text)

    assert parsed_job.title == "Software Engineer II, Backend (Consumer Authentication)"
    assert parsed_job.company == "Affirm"
    assert parsed_job.location == "Remote Canada"
    assert parsed_job.years_experience_required == 1.5
    assert parsed_job.seniority == "mid"
    assert parsed_job.role_type == "backend"
    assert parsed_job.salary_min == 125000
    assert parsed_job.salary_max == 175000
    assert parsed_job.salary_currency == "CAD"
    assert parsed_job.salary_period == "yearly"


def test_parse_job_description_leaves_inferred_fields_empty_for_now() -> None:
    raw_text = (FIXTURES_DIR / "affirm_backend_engineer.txt").read_text()

    parsed_job = parse_job_description(raw_text)

    assert parsed_job.technologies == ["python", "kotlin", "aws", "mysql", "kubernetes"]
    assert parsed_job.domain_signals == [
        "authentication",
        "security",
        "fraud",
        "distributed-systems",
        "backend",
        "account-management",
    ]
    assert parsed_job.work_style_signals == ["remote", "on-call"]


def test_parse_job_description_extracts_integrations_job_fields() -> None:
    raw_text = (FIXTURES_DIR / "integrations_engineer.txt").read_text()

    parsed_job = parse_job_description(raw_text)

    assert parsed_job.title == "Software Engineer, Integrations"
    assert parsed_job.company is None
    assert parsed_job.location == "Vancouver, BC"
    assert parsed_job.years_experience_required == 3.0
    assert parsed_job.seniority == "mid"
    assert parsed_job.role_type == "platform"
    assert parsed_job.salary_min == 105000
    assert parsed_job.salary_max == 115000
    assert parsed_job.salary_currency == "CAD"
    assert parsed_job.salary_period == "yearly"
    assert parsed_job.technologies == [
        "c#",
        "dotnet-core",
        "typescript",
        "azure",
        "docker",
        "postgresql",
        "sql-server",
        "cosmosdb",
        "kafka",
        "oauth2",
        "jwt",
        "saml",
        "kong",
    ]
    assert parsed_job.domain_signals == [
        "authentication",
        "security",
        "distributed-systems",
        "integrations",
        "apis",
        "microservices",
        "event-streaming",
    ]
    assert parsed_job.work_style_signals == ["hybrid"]


def test_parse_job_description_extracts_apple_workflow_job_fields() -> None:
    raw_text = (FIXTURES_DIR / "apple_workflow_foundations.txt").read_text()

    parsed_job = parse_job_description(raw_text)

    assert parsed_job.title == "Software Engineer, Workflow Foundations"
    assert parsed_job.company == "Apple"
    assert parsed_job.location == "Vancouver, British Columbia, Canada"
    assert parsed_job.years_experience_required == 3.0
    assert parsed_job.seniority == "mid"
    assert parsed_job.role_type == "backend"
    assert parsed_job.salary_min == 116800
    assert parsed_job.salary_max == 226000
    assert parsed_job.salary_currency == "CAD"
    assert parsed_job.salary_period == "yearly"
    assert parsed_job.technologies == [
        "go",
        "python",
        "java",
        "scala",
        "kotlin",
    ]
    assert parsed_job.domain_signals == [
        "distributed-systems",
        "backend",
        "integrations",
        "apis",
        "microservices",
        "developer-productivity",
        "event-driven",
        "observability",
        "ci-cd",
    ]
    assert parsed_job.work_style_signals == ["on-call"]

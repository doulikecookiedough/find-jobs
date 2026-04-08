from pathlib import Path

from find_jobs.models import ParsedJob
from find_jobs.parser import parse_job_description


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


def parsed_job_snapshot(parsed_job: ParsedJob) -> dict[str, object]:
    return {
        "title": parsed_job.title,
        "company": parsed_job.company,
        "location": parsed_job.location,
        "years_experience_required": parsed_job.years_experience_required,
        "seniority": parsed_job.seniority,
        "role_type": parsed_job.role_type,
        "salary_min": parsed_job.salary_min,
        "salary_max": parsed_job.salary_max,
        "salary_currency": parsed_job.salary_currency,
        "salary_period": parsed_job.salary_period,
        "technologies": sorted(parsed_job.technologies),
        "domain_signals": sorted(parsed_job.domain_signals),
        "work_style_signals": sorted(parsed_job.work_style_signals),
    }


def test_parse_job_description_extracts_affirm_job_fields() -> None:
    parsed_job = parse_job_description(load_fixture("affirm_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer II, Backend (Consumer Authentication)",
        "company": "Affirm",
        "location": "Remote Canada",
        "years_experience_required": 1.5,
        "seniority": "mid",
        "role_type": "backend",
        "salary_min": 125000,
        "salary_max": 175000,
        "salary_currency": "CAD",
        "salary_period": "yearly",
        "technologies": ["aws", "kotlin", "kubernetes", "mysql", "python"],
        "domain_signals": [
            "account-management",
            "authentication",
            "backend",
            "distributed-systems",
            "fraud",
            "security",
        ],
        "work_style_signals": ["on-call", "remote"],
    }


def test_parse_job_description_extracts_integrations_job_fields() -> None:
    parsed_job = parse_job_description(load_fixture("integrations_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer, Integrations",
        "company": None,
        "location": "Vancouver, BC",
        "years_experience_required": 3.0,
        "seniority": "mid",
        "role_type": "platform",
        "salary_min": 105000,
        "salary_max": 115000,
        "salary_currency": "CAD",
        "salary_period": "yearly",
        "technologies": [
            "azure",
            "c#",
            "cosmosdb",
            "docker",
            "dotnet-core",
            "jwt",
            "kafka",
            "kong",
            "oauth2",
            "postgresql",
            "saml",
            "sql-server",
            "typescript",
        ],
        "domain_signals": [
            "apis",
            "authentication",
            "distributed-systems",
            "event-streaming",
            "integrations",
            "microservices",
            "security",
        ],
        "work_style_signals": ["hybrid"],
    }


def test_parse_job_description_extracts_apple_workflow_job_fields() -> None:
    parsed_job = parse_job_description(load_fixture("apple_workflow_foundations.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer, Workflow Foundations",
        "company": "Apple",
        "location": "Vancouver, British Columbia, Canada",
        "years_experience_required": 3.0,
        "seniority": "mid",
        "role_type": "backend",
        "salary_min": 116800,
        "salary_max": 226000,
        "salary_currency": "CAD",
        "salary_period": "yearly",
        "technologies": ["go", "java", "kotlin", "python", "scala"],
        "domain_signals": [
            "apis",
            "backend",
            "ci-cd",
            "developer-platform",
            "developer-productivity",
            "distributed-systems",
            "event-driven",
            "integrations",
            "microservices",
            "observability",
        ],
        "work_style_signals": ["on-call"],
    }


def test_parse_job_description_extracts_zepp_connected_partnerships_fields() -> None:
    parsed_job = parse_job_description(load_fixture("zepp_connected_partnerships.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Full-Stack Engineer, Connected Partnerships",
        "company": "Zepp Health",
        "location": "Vancouver, BC",
        "years_experience_required": 3.0,
        "seniority": "mid",
        "role_type": "full-stack",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": ["java", "oauth", "rest-apis", "spring-boot", "webhooks"],
        "domain_signals": [
            "apis",
            "backend",
            "developer-platform",
            "distributed-systems",
            "integrations",
            "security",
        ],
        "work_style_signals": ["on-site"],
    }


def test_parse_job_description_extracts_genista_backend_fields() -> None:
    parsed_job = parse_job_description(load_fixture("genista_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer",
        "company": "Genista Biosciences",
        "location": "Canada",
        "years_experience_required": 2.0,
        "seniority": "mid",
        "role_type": "backend",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": [
            "django",
            "django-rest-framework",
            "mongodb",
            "mysql",
            "postgresql",
            "python",
            "rest-apis",
        ],
        "domain_signals": ["apis", "backend", "integrations"],
        "work_style_signals": ["remote"],
    }


def test_parse_job_description_extracts_stripe_backend_fields() -> None:
    parsed_job = parse_job_description(load_fixture("stripe_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Backend Engineer, Developer Experience & Product Platform",
        "company": "Stripe",
        "location": "Canada",
        "years_experience_required": 2.0,
        "seniority": "mid",
        "role_type": "backend",
        "salary_min": 135200,
        "salary_max": 258000,
        "salary_currency": "CAD",
        "salary_period": "yearly",
        "technologies": ["aws", "java", "oauth", "ruby", "scim", "sso"],
        "domain_signals": [
            "apis",
            "authentication",
            "backend",
            "developer-platform",
            "iam",
            "security",
        ],
        "work_style_signals": ["hybrid", "remote"],
    }


def test_parse_job_description_extracts_berkeley_payments_backend_fields() -> None:
    parsed_job = parse_job_description(load_fixture("berkeley_payments_senior_backend.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": None,
        "company": "Berkeley Payments",
        "location": "Remote",
        "years_experience_required": 5.0,
        "seniority": "senior",
        "role_type": "backend",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": [
            "aws",
            "docker",
            "github",
            "git",
            "javascript",
            "jenkins",
            "kubernetes",
            "mysql",
            "postgresql",
            "react",
            "rest-apis",
            "terraform",
        ],
        "domain_signals": [
            "apis",
            "backend",
            "integrations",
            "microservices",
            "security",
        ],
        "work_style_signals": ["remote"],
    }

"""Parser tests for extracting normalized job fields from fixtures."""

from pathlib import Path

from find_jobs.models import ParsedJob
from find_jobs.parser import parse_job_description


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    """Load a parser fixture file by name."""
    return (FIXTURES_DIR / name).read_text()


def parsed_job_snapshot(parsed_job: ParsedJob) -> dict[str, object]:
    """Normalize parsed job fields into a stable assertion snapshot."""
    return {
        "title": parsed_job.title,
        "company": parsed_job.company,
        "location": parsed_job.location,
        "years_experience_required": parsed_job.years_experience_required,
        "years_experience_max_required": parsed_job.years_experience_max_required,
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
    """Extracts the expected fields from the Affirm backend fixture."""

    parsed_job = parse_job_description(load_fixture("affirm_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer II, Backend (Consumer Authentication)",
        "company": "Affirm",
        "location": "Remote Canada",
        "years_experience_required": 1.5,
        "years_experience_max_required": 1.5,
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
    """Extracts platform and security signals from the integrations fixture."""

    parsed_job = parse_job_description(load_fixture("integrations_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer, Integrations",
        "company": None,
        "location": "Vancouver, BC",
        "years_experience_required": 3.0,
        "years_experience_max_required": 5.0,
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
    """Extracts the expected backend workflow fields from the Apple fixture."""

    parsed_job = parse_job_description(load_fixture("apple_workflow_foundations.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer, Workflow Foundations",
        "company": "Apple",
        "location": "Vancouver, British Columbia, Canada",
        "years_experience_required": 3.0,
        "years_experience_max_required": 3.0,
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
    """Extracts the expected full-stack fields from the Zepp fixture."""

    parsed_job = parse_job_description(load_fixture("zepp_connected_partnerships.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Full-Stack Engineer, Connected Partnerships",
        "company": "Zepp Health",
        "location": "Vancouver, BC",
        "years_experience_required": 3.0,
        "years_experience_max_required": 3.0,
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
    """Extracts the expected backend fields from the Genista fixture."""

    parsed_job = parse_job_description(load_fixture("genista_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer",
        "company": "Genista Biosciences",
        "location": "Canada",
        "years_experience_required": 2.0,
        "years_experience_max_required": 7.0,
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


def test_parse_job_description_extracts_picovoice_wellfound_fields() -> None:
    """Extracts the expected fields from the noisier Picovoice fixture."""

    parsed_job = parse_job_description(load_fixture("picovoice_wellfound.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer",
        "company": "Picovoice",
        "location": "Vancouver",
        "years_experience_required": 2.0,
        "years_experience_max_required": 2.0,
        "seniority": "mid",
        "role_type": None,
        "salary_min": 75000,
        "salary_max": 150000,
        "salary_currency": "CAD",
        "salary_period": "yearly",
        "technologies": ["aws", "javascript", "python", "react", "typescript"],
        "domain_signals": [],
        "work_style_signals": ["on-site"],
    }


def test_parse_job_description_extracts_coalition_data_engineer_fields() -> None:
    """Extracts the expected data-role fields from the Coalition fixture."""

    parsed_job = parse_job_description(load_fixture("coalition_data_engineer_security.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Data Engineer, Security",
        "company": "Coalition, Inc.",
        "location": "Canada",
        "years_experience_required": None,
        "years_experience_max_required": None,
        "seniority": None,
        "role_type": "data",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": ["dbt", "looker", "python", "snowflake"],
        "domain_signals": ["integrations", "observability", "security"],
        "work_style_signals": ["remote"],
    }


def test_parse_job_description_extracts_surveymonkey_zuora_fields() -> None:
    """Extracts the expected business-systems fields from the Zuora fixture."""

    parsed_job = parse_job_description(load_fixture("surveymonkey_zuora_developer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Zuora Developer",
        "company": "SurveyMonkey",
        "location": "Canada",
        "years_experience_required": 1.0,
        "years_experience_max_required": 1.0,
        "seniority": "mid",
        "role_type": "business-systems",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": [
            "cpq",
            "mulesoft",
            "netsuite",
            "revpro",
            "salesforce",
            "zuora",
        ],
        "domain_signals": ["apis", "business-systems", "integrations"],
        "work_style_signals": [],
    }


def test_parse_job_description_extracts_versaterm_se2_dems_fields() -> None:
    """Extracts the expected backend fields from the Versaterm fixture."""

    parsed_job = parse_job_description(load_fixture("versaterm_se2_dems.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Software Engineer II - DEMS",
        "company": "Versaterm",
        "location": "Vancouver, British Columbia, Canada",
        "years_experience_required": 2.0,
        "years_experience_max_required": 5.0,
        "seniority": "mid",
        "role_type": "backend",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": [
            "aws",
            "docker",
            "git",
            "github",
            "postgresql",
            "python",
            "react",
            "terraform",
            "typescript",
        ],
        "domain_signals": ["apis", "backend", "integrations", "security"],
        "work_style_signals": [],
    }


def test_parse_job_description_extracts_stripe_backend_fields() -> None:
    """Extracts the expected backend platform fields from the Stripe fixture."""

    parsed_job = parse_job_description(load_fixture("stripe_backend_engineer.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Backend Engineer, Developer Experience & Product Platform",
        "company": "Stripe",
        "location": "Canada",
        "years_experience_required": 2.0,
        "years_experience_max_required": 5.0,
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
    """Extracts the expected senior backend fields from the Berkeley fixture."""

    parsed_job = parse_job_description(load_fixture("berkeley_payments_senior_backend.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Senior Software Engineer",
        "company": "Berkeley Payments",
        "location": "Remote",
        "years_experience_required": 5.0,
        "years_experience_max_required": 5.0,
        "seniority": "senior",
        "role_type": "backend",
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": [
            "aws",
            "azure",
            "docker",
            "git",
            "github",
            "golang",
            "javascript",
            "jenkins",
            "kubernetes",
            "mysql",
            "postgresql",
            "react",
            "spinnaker",
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


def test_parse_job_description_extracts_narvar_distributed_systems_fields() -> None:
    """Extracts the expected stretch-role fields from the Narvar fixture."""

    parsed_job = parse_job_description(load_fixture("narvar_distributed_systems.txt"))

    assert parsed_job_snapshot(parsed_job) == {
        "title": "Sr. Software Engineer II (Distributed Systems)",
        "company": "Narvar",
        "location": "Canada",
        "years_experience_required": 7.0,
        "years_experience_max_required": 7.0,
        "seniority": "senior",
        "role_type": None,
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "technologies": ["aws", "go", "java", "mongodb", "mysql", "python", "scala"],
        "domain_signals": ["apis", "distributed-systems", "integrations"],
        "work_style_signals": ["remote"],
    }


def test_parse_job_description_extracts_company_from_banner_header() -> None:
    """Recovers the company name from a banner-style header layout."""

    parsed_job = parse_job_description(
        (
            "Microsoft\n"
            "Actively Hiring\n"
            "Help People and Businesses Throughout the World Realize Their Full Potential\n"
            "Share\n"
            "Save\n"
            "Software Engineering II- Full stack\n"
            "$85k – $166k\n"
            "|\n"
            "Vancouver\n"
            "|3 years of exp\n"
            "About the job\n"
            "Build modern React and Python experiences.\n"
        ),
    )

    assert parsed_job.title == "Software Engineering II- Full stack"
    assert parsed_job.company == "Microsoft"
    assert parsed_job.salary_min == 85000
    assert parsed_job.salary_max == 166000


def test_parse_job_description_does_not_treat_salary_as_company() -> None:
    """Avoids misclassifying salary lines as company names."""

    parsed_job = parse_job_description(
        (
            "Amazon Web Services\n"
            "Actively Hiring\n"
            "Share\n"
            "Save\n"
            "Software Development Engineer II, AWS Eventbridge\n"
            "$114k – $191k\n"
            "|\n"
            "Vancouver\n"
            "|3 years of exp\n"
            "About the job\n"
            "Develop large scale distributed systems on AWS.\n"
        ),
    )

    assert parsed_job.title == "Software Development Engineer II, AWS Eventbridge"
    assert parsed_job.company == "Amazon Web Services"
    assert parsed_job.salary_min == 114000
    assert parsed_job.salary_max == 191000


def test_parse_job_description_preserves_years_ranges() -> None:
    """Captures both ends of explicit experience ranges from job text."""

    parsed_job = parse_job_description(
        (
            "Junior ServiceNow Developer\n"
            "CGI\n"
            "Vancouver\n"
            "3 - 5 years of hands-on experience as a ServiceNow Developer.\n"
            "About the job\n"
            "Build ServiceNow applications and integrations.\n"
        ),
    )

    assert parsed_job.years_experience_required == 3.0
    assert parsed_job.years_experience_max_required == 5.0


def test_parse_job_description_prefers_detailed_years_range_over_header_snippet() -> None:
    """Prefers a later detailed years range over an earlier shorthand header snippet."""

    parsed_job = parse_job_description(
        (
            "CGI\n"
            "Share\n"
            "Save\n"
            "Junior ServiceNow Developer\n"
            "|3 years of exp\n"
            "About the job\n"
            "3 - 5 years of hands-on experience as a ServiceNow Developer.\n"
            "Build ServiceNow applications and integrations.\n"
        ),
    )

    assert parsed_job.years_experience_required == 3.0
    assert parsed_job.years_experience_max_required == 5.0


def test_parse_job_description_extracts_entry_level_developer_title() -> None:
    """Extracts title lines that use a role suffix like Developer - Entry Level."""

    parsed_job = parse_job_description(
        (
            "CGI\n"
            "Share\n"
            "Save\n"
            "ServiceNow Developer - Entry Level\n"
            "Vancouver\n"
            "About the job\n"
        ),
    )

    assert parsed_job.title == "ServiceNow Developer - Entry Level"


def test_parse_job_description_extracts_servicenow_business_systems_signals() -> None:
    """Extracts ServiceNow-family technologies and business-systems role signals."""

    parsed_job = parse_job_description(
        (
            "CGI\n"
            "ServiceNow Developer - Entry Level\n"
            "Skills\n"
            "CRM\n"
            "servicenow\n"
            "CSM\n"
            "itsm\n"
            "SPM\n"
            "Itom\n"
            "HRSD\n"
            "About the job\n"
            "Develop and customize ServiceNow modules, including ITSM and CSM.\n"
        ),
    )

    assert parsed_job.role_type == "business-systems"
    assert sorted(parsed_job.technologies) == [
        "csm",
        "hrsd",
        "itom",
        "itsm",
        "servicenow",
        "spm",
    ]
    assert "business-systems" in parsed_job.domain_signals

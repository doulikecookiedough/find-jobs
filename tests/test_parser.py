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
    assert parsed_job.salary_min == 125000
    assert parsed_job.salary_max == 175000
    assert parsed_job.salary_currency == "CAD"
    assert parsed_job.salary_period == "yearly"


def test_parse_job_description_leaves_inferred_fields_empty_for_now() -> None:
    raw_text = (FIXTURES_DIR / "affirm_backend_engineer.txt").read_text()

    parsed_job = parse_job_description(raw_text)

    assert parsed_job.technologies == ["python", "kotlin", "aws", "mysql", "kubernetes"]
    assert parsed_job.domain_signals == []
    assert parsed_job.work_style_signals == []

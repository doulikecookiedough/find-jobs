from find_jobs.models import ParsedJob


def test_parsed_job_defaults() -> None:
    parsed_job = ParsedJob(raw_text="Job text")

    assert parsed_job.raw_text == "Job text"
    assert parsed_job.title is None
    assert parsed_job.role_type is None
    assert parsed_job.salary_min is None
    assert parsed_job.technologies == []

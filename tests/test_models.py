from find_jobs.models import CandidateProfile, JobScore, ParsedJob, ScoreBreakdown


def test_parsed_job_defaults() -> None:
    parsed_job = ParsedJob(raw_text="Job text")

    assert parsed_job.raw_text == "Job text"
    assert parsed_job.title is None
    assert parsed_job.seniority is None
    assert parsed_job.role_type is None
    assert parsed_job.salary_min is None
    assert parsed_job.technologies == []


def test_candidate_profile_defaults() -> None:
    profile = CandidateProfile(years_experience=3.0)

    assert profile.years_experience == 3.0
    assert profile.headline is None
    assert profile.primary_languages == []
    assert profile.preferred_roles == []
    assert profile.avoid_domains == []


def test_job_score_defaults() -> None:
    score = JobScore(fit_score=72, recommendation="consider", priority="medium")

    assert score.fit_score == 72
    assert score.score_breakdown == ScoreBreakdown()
    assert score.reasons == []
    assert score.risks == []
    assert score.missing_fields == []
    assert score.parser_warnings == []

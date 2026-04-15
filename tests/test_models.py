"""Model tests for dataclass defaults and score containers."""

from find_jobs.models import CandidateProfile, JobScore, ParsedJob, ScoreBreakdown


def test_parsed_job_defaults() -> None:
    """Initializes parsed jobs with optional fields left empty."""

    parsed_job = ParsedJob(raw_text="Job text")

    assert parsed_job.raw_text == "Job text"
    assert parsed_job.title is None
    assert parsed_job.seniority is None
    assert parsed_job.role_type is None
    assert parsed_job.years_experience_max_required is None
    assert parsed_job.salary_min is None
    assert not parsed_job.technologies


def test_candidate_profile_defaults() -> None:
    """Initializes candidate profiles with empty optional collections."""

    profile = CandidateProfile(years_experience=3.0)

    assert profile.years_experience == 3.0
    assert profile.headline is None
    assert not profile.primary_languages
    assert not profile.preferred_specialized_domains
    assert not profile.avoid_specialized_domains
    assert not profile.preferred_roles
    assert not profile.avoid_domains


def test_job_score_defaults() -> None:
    """Initializes job scores with empty review metadata by default."""

    score = JobScore(fit_score=72, recommendation="consider", priority="medium")

    assert score.fit_score == 72
    assert score.score_breakdown == ScoreBreakdown()
    assert not score.reasons
    assert not score.risks
    assert not score.missing_fields
    assert not score.parser_warnings

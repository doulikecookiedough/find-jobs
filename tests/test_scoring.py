from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring import score_level_match


def test_score_level_match_is_high_for_matching_experience() -> None:
    profile = CandidateProfile(years_experience=3.0)
    job = ParsedJob(raw_text="job", years_experience_required=3.0, seniority="mid")

    assert score_level_match(job, profile) == 1.0


def test_score_level_match_drops_for_small_experience_gap() -> None:
    profile = CandidateProfile(years_experience=3.0)
    job = ParsedJob(raw_text="job", years_experience_required=4.0, seniority="mid")

    assert score_level_match(job, profile) == 0.85


def test_score_level_match_is_zero_for_strong_level_mismatch() -> None:
    profile = CandidateProfile(years_experience=3.0)
    job = ParsedJob(raw_text="job", years_experience_required=7.0, seniority="senior")

    assert score_level_match(job, profile) == 0.0


def test_score_level_match_uses_seniority_when_years_are_missing() -> None:
    profile = CandidateProfile(years_experience=3.0)
    job = ParsedJob(raw_text="job", seniority="senior")

    assert score_level_match(job, profile) == 0.35

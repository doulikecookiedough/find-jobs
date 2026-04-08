from find_jobs.profile import build_default_candidate_profile


def test_build_default_candidate_profile_returns_expected_defaults() -> None:
    profile = build_default_candidate_profile()

    assert profile.years_experience == 3.0
    assert profile.preferred_roles == ["backend", "platform"]
    assert profile.preferred_domains == [
        "backend",
        "distributed-systems",
        "event-driven",
        "apis",
        "integrations",
        "observability",
    ]
    assert profile.preferred_technologies == ["python", "java", "aws", "postgresql", "kubernetes"]
    assert profile.avoid_domains == ["mobile", "frontend", "networking"]
    assert profile.avoid_roles == ["frontend", "mobile"]

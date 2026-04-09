from find_jobs.profile import build_default_candidate_profile


def test_build_default_candidate_profile_returns_expected_defaults() -> None:
    profile = build_default_candidate_profile()

    assert profile.years_experience == 3.0
    assert profile.headline is not None
    assert profile.target_focus == "Backend / Data Platforms / Product Engineering"
    assert profile.primary_languages == ["python"]
    assert profile.secondary_languages == ["java", "typescript", "bash"]
    assert profile.frameworks == ["flask", "django", "next.js", "react", "prisma"]
    assert profile.cloud_platforms == [
        "aws",
        "s3",
        "ec2",
        "lambda",
        "step-functions",
        "sqs",
        "ses",
        "glue",
        "athena",
        "cloudfront",
    ]
    assert profile.databases == ["postgresql", "mysql", "cloudnativepg"]
    assert profile.infrastructure_tools == ["kubernetes", "helm", "docker"]
    assert profile.developer_tools == [
        "git",
        "github",
        "github-actions",
        "maven",
        "junit",
        "pytest",
        "vitest",
    ]
    assert profile.strengths == [
        "backend",
        "full-stack",
        "product-engineering",
        "data-platforms",
        "distributed-systems",
        "data-integrity",
        "concurrency",
        "schema-migrations",
        "apis",
        "integrations",
        "reliability",
        "etl",
        "testing",
        "documentation",
    ]
    assert profile.preferred_roles == ["backend", "platform"]
    assert profile.preferred_domains == [
        "backend",
        "distributed-systems",
        "event-driven",
        "apis",
        "integrations",
        "observability",
        "developer-platform",
    ]
    assert profile.preferred_technologies == [
        "python",
        "java",
        "aws",
        "postgresql",
        "kubernetes",
        "django",
        "rest-apis",
        "docker",
    ]
    assert profile.avoid_domains == ["mobile", "frontend", "networking", "low-level-systems"]
    assert profile.avoid_roles == ["frontend", "mobile"]

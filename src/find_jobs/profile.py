"""Candidate profile helpers."""

from __future__ import annotations

from find_jobs.models import CandidateProfile


def build_default_candidate_profile() -> CandidateProfile:
    """Return the default candidate profile used for local scoring."""
    return CandidateProfile(
        years_experience=3.0,
        headline=(
            "Backend engineer with experience building and operating production "
            "systems using Python, PostgreSQL, AWS, and Kubernetes."
        ),
        target_focus="Backend / Data Platforms",
        primary_languages=["python"],
        secondary_languages=["java", "typescript", "bash"],
        frameworks=["flask", "django", "next.js", "react", "prisma"],
        cloud_platforms=[
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
        ],
        databases=["postgresql", "mysql", "cloudnativepg"],
        infrastructure_tools=["kubernetes", "helm", "docker"],
        developer_tools=["git", "github", "github-actions", "maven", "junit", "pytest", "vitest"],
        strengths=[
            "backend",
            "data-platforms",
            "distributed-systems",
            "data-integrity",
            "concurrency",
            "schema-migrations",
            "apis",
            "integrations",
            "reliability",
            "etl",
        ],
        preferred_roles=["backend", "platform"],
        preferred_domains=[
            "backend",
            "distributed-systems",
            "event-driven",
            "apis",
            "integrations",
            "observability",
            "developer-platform",
        ],
        preferred_technologies=[
            "python",
            "java",
            "aws",
            "postgresql",
            "kubernetes",
            "django",
            "rest-apis",
            "docker",
        ],
        avoid_domains=["mobile", "frontend", "networking", "low-level-systems"],
        avoid_roles=["frontend", "mobile"],
    )

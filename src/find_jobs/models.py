"""Shared domain models for the project."""

from __future__ import annotations

from dataclasses import dataclass, field


# pylint: disable=too-many-instance-attributes


@dataclass(slots=True)
class ParsedJob:
    """Parsed representation of a raw job description."""

    raw_text: str
    title: str | None = None
    company: str | None = None
    location: str | None = None
    years_experience_required: float | None = None
    years_experience_max_required: float | None = None
    seniority: str | None = None
    role_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    salary_period: str | None = None
    technologies: list[str] = field(default_factory=list)
    domain_signals: list[str] = field(default_factory=list)
    work_style_signals: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CandidateProfile:
    """Candidate attributes used by parsing and scoring."""

    years_experience: float
    headline: str | None = None
    target_focus: str | None = None
    primary_languages: list[str] = field(default_factory=list)
    secondary_languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    cloud_platforms: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    infrastructure_tools: list[str] = field(default_factory=list)
    developer_tools: list[str] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    preferred_roles: list[str] = field(default_factory=list)
    preferred_domains: list[str] = field(default_factory=list)
    preferred_technologies: list[str] = field(default_factory=list)
    avoid_domains: list[str] = field(default_factory=list)
    avoid_roles: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScoreBreakdown:
    """Normalized component scores used to assemble the final result."""

    level_match: float = 0.0
    stack_alignment: float = 0.0
    domain_alignment: float = 0.0
    strength_alignment: float = 0.0
    role_type_alignment: float = 0.0
    competition_realism: float = 0.0
    missing_inference_infra_proof: bool = False
    matched_specialized_domains: list[str] = field(default_factory=list)


@dataclass(slots=True)
class JobScore:
    """Final job evaluation returned by the scoring engine."""

    fit_score: int
    recommendation: str
    priority: str
    skills_alignment: int = 0
    interview_probability_min: int = 0
    interview_probability_max: int = 0
    years_experience_required: float | None = None
    candidate_years_experience: float | None = None
    years_experience_gap: float | None = None
    years_experience_match_status: str = "unknown"
    years_experience_match_label: str = "Experience requirement unclear"
    reasons: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    parser_warnings: list[str] = field(default_factory=list)
    score_breakdown: ScoreBreakdown = field(default_factory=ScoreBreakdown)

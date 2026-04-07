"""Shared domain models for the project."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ParsedJob:
    raw_text: str
    title: str | None = None
    company: str | None = None
    location: str | None = None
    years_experience_required: float | None = None
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
    years_experience: float
    preferred_roles: list[str] = field(default_factory=list)
    preferred_domains: list[str] = field(default_factory=list)
    preferred_technologies: list[str] = field(default_factory=list)
    avoid_domains: list[str] = field(default_factory=list)
    avoid_roles: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScoreBreakdown:
    level_match: float = 0.0
    stack_alignment: float = 0.0
    domain_alignment: float = 0.0
    role_type_alignment: float = 0.0
    competition_realism: float = 0.0


@dataclass(slots=True)
class JobScore:
    fit_score: int
    recommendation: str
    priority: str
    reasons: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    score_breakdown: ScoreBreakdown = field(default_factory=ScoreBreakdown)

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
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    salary_period: str | None = None
    technologies: list[str] = field(default_factory=list)
    domain_signals: list[str] = field(default_factory=list)
    work_style_signals: list[str] = field(default_factory=list)

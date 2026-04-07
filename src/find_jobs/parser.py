"""Job description parsing utilities."""

from __future__ import annotations

import re

from find_jobs.models import ParsedJob


COMPANY_PATTERN = re.compile(r"^([A-Z][A-Za-z0-9&'., -]+?) is\b", re.MULTILINE)
EXPERIENCE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\+?\s+years? of experience",
    re.IGNORECASE,
)
SALARY_PATTERN = re.compile(
    r"\b(CAN|CAD|USD|US)\s+base pay range per year:\s*\$([\d,]+)\s*-\s*\$([\d,]+)",
    re.IGNORECASE,
)
TECHNOLOGY_PATTERNS = {
    "python": re.compile(r"\bpython\b", re.IGNORECASE),
    "kotlin": re.compile(r"\bkotlin\b", re.IGNORECASE),
    "aws": re.compile(r"\baws\b", re.IGNORECASE),
    "mysql": re.compile(r"\bmysql\b", re.IGNORECASE),
    "kubernetes": re.compile(r"\bkubernetes\b", re.IGNORECASE),
}
WORK_STYLE_PATTERNS = {
    "remote": re.compile(r"\bremote\b", re.IGNORECASE),
    "on-call": re.compile(r"\bon-call\b", re.IGNORECASE),
}


def parse_job_description(raw_text: str) -> ParsedJob:
    """Parse a raw job description into directly extracted fields."""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    title = lines[0] if lines else None
    location = lines[1] if len(lines) > 1 else None

    company_match = COMPANY_PATTERN.search(raw_text)
    years_match = EXPERIENCE_PATTERN.search(raw_text)
    salary_match = SALARY_PATTERN.search(raw_text)

    salary_currency = None
    salary_min = None
    salary_max = None
    salary_period = None

    if salary_match:
        salary_currency = _normalize_currency(salary_match.group(1))
        salary_min = int(salary_match.group(2).replace(",", ""))
        salary_max = int(salary_match.group(3).replace(",", ""))
        salary_period = "yearly"

    return ParsedJob(
        raw_text=raw_text,
        title=title,
        company=company_match.group(1) if company_match else None,
        location=location,
        years_experience_required=float(years_match.group(1)) if years_match else None,
        salary_min=salary_min,
        salary_max=salary_max,
        salary_currency=salary_currency,
        salary_period=salary_period,
        technologies=_extract_technologies(raw_text),
        work_style_signals=_extract_work_style_signals(raw_text),
    )


def _normalize_currency(raw_currency: str) -> str:
    currency = raw_currency.upper()
    if currency in {"CAN", "CAD"}:
        return "CAD"
    if currency in {"US", "USD"}:
        return "USD"
    return currency


def _extract_technologies(raw_text: str) -> list[str]:
    return [
        technology
        for technology, pattern in TECHNOLOGY_PATTERNS.items()
        if pattern.search(raw_text)
    ]


def _extract_work_style_signals(raw_text: str) -> list[str]:
    return [
        signal
        for signal, pattern in WORK_STYLE_PATTERNS.items()
        if pattern.search(raw_text)
    ]

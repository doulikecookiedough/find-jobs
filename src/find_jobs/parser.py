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
    )


def _normalize_currency(raw_currency: str) -> str:
    currency = raw_currency.upper()
    if currency in {"CAN", "CAD"}:
        return "CAD"
    if currency in {"US", "USD"}:
        return "USD"
    return currency

"""Job description parsing utilities."""

from __future__ import annotations

import re

from find_jobs.models import ParsedJob


COMPANY_PATTERN = re.compile(
    r"^(?!Our company\b)([A-Z][A-Za-z0-9&'., -]+?) is\b",
    re.MULTILINE,
)
AT_COMPANY_PATTERN = re.compile(r"\bAt\s+([A-Z][A-Za-z0-9&'. -]+),", re.MULTILINE)
EXPERIENCE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\+?\s+years?\b",
    re.IGNORECASE,
)
EXPERIENCE_RANGE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s+years?\b",
    re.IGNORECASE,
)
SALARY_PATTERN = re.compile(
    r"\b(CAN|CAD|USD|US)\s+base pay range per year:\s*\$([\d,]+)\s*-\s*\$([\d,]+)",
    re.IGNORECASE,
)
SALARY_RANGE_PATTERN = re.compile(
    r"\$([\d,]+)\s*(?:-|to)\s*\$([\d,]+)\s+per\s+(year|annum)",
    re.IGNORECASE,
)
SALARY_BETWEEN_PATTERN = re.compile(
    r"\bbetween\s+\$([\d,]+)\s+and\s+\$([\d,]+)",
    re.IGNORECASE,
)
SALARY_CURRENCY_RANGE_PATTERN = re.compile(
    r"\b(CA|US)\$([\d,]+)\s*-\s*(?:CA\$|US\$|\$)([\d,]+)",
    re.IGNORECASE,
)
SALARY_THOUSANDS_RANGE_PATTERN = re.compile(
    r"\$([\d,]+)k\s*[–-]\s*\$([\d,]+)k\s+(CAD|USD|US|CA)\b",
    re.IGNORECASE,
)
LOCATION_PATTERN = re.compile(
    r"^[A-Z][A-Za-z .'-]+,\s*[A-Z]{2}(?:\s+[A-Z]\d[A-Z]\d[A-Z]\d,\s*[A-Z]{3})?$"
)
COUNTRY_LOCATION_PATTERN = re.compile(r"^(Canada|United States|USA|US)$", re.IGNORECASE)
REMOTE_LOCATION_PATTERN = re.compile(r"^Remote\s+(Canada|United States|USA|US)$", re.IGNORECASE)
REMOTE_ONLY_LOCATION_PATTERN = re.compile(r"^Remote$", re.IGNORECASE)
REMOTE_POSITION_PATTERN = re.compile(r"^This is a remote position\.?$", re.IGNORECASE)
LONG_LOCATION_PATTERN = re.compile(r"^[A-Z][A-Za-z .'-]+,\s*[A-Z][A-Za-z .'-]+,\s*[A-Z][A-Za-z .'-]+$")
TITLE_PATTERN = re.compile(
    r"^(?=.*\b(?:engineer|developer)\b)(?=.*\b(?:software|backend|frontend|full-stack|platform|senior|junior|staff|principal|lead)\b).+$",
    re.IGNORECASE,
)
TITLE_PHRASE_PATTERN = re.compile(
    r"\b(?:Senior|Junior|Staff|Principal|Lead)\s+(?:Software\s+)?(?:Engineer|Developer)\b|\b(?:Software|Backend|Frontend|Full-Stack|Platform)\s+(?:Engineer|Developer)\b",
    re.IGNORECASE,
)
TECHNOLOGY_PATTERNS = {
    "c#": re.compile(r"(?<!\w)c#(?!\w)", re.IGNORECASE),
    "dotnet-core": re.compile(r"\.net core\b|\bdotnet core\b", re.IGNORECASE),
    "typescript": re.compile(r"\btypescript\b", re.IGNORECASE),
    "javascript": re.compile(r"\bjavascript\b", re.IGNORECASE),
    "go": re.compile(r"(?<!\w)go(?!\w)", re.IGNORECASE),
    "golang": re.compile(r"\bgolang\b", re.IGNORECASE),
    "python": re.compile(r"\bpython\b", re.IGNORECASE),
    "java": re.compile(r"\bjava\b", re.IGNORECASE),
    "ruby": re.compile(r"\bruby\b", re.IGNORECASE),
    "scala": re.compile(r"\bscala\b", re.IGNORECASE),
    "kotlin": re.compile(r"\bkotlin\b", re.IGNORECASE),
    "django": re.compile(r"\bdjango\b", re.IGNORECASE),
    "django-rest-framework": re.compile(r"\bdjango rest framework\b|\bdrf\b", re.IGNORECASE),
    "spring-boot": re.compile(r"\bspring boot\b", re.IGNORECASE),
    "react": re.compile(r"\breact\b", re.IGNORECASE),
    "rest-apis": re.compile(r"\brest apis?\b", re.IGNORECASE),
    "aws": re.compile(r"\baws\b", re.IGNORECASE),
    "azure": re.compile(r"\bazure\b", re.IGNORECASE),
    "docker": re.compile(r"\bdocker\b", re.IGNORECASE),
    "spinnaker": re.compile(r"\bspinnaker\b", re.IGNORECASE),
    "jenkins": re.compile(r"\bjenkins\b", re.IGNORECASE),
    "terraform": re.compile(r"\bterraform\b", re.IGNORECASE),
    "mysql": re.compile(r"\bmysql\b", re.IGNORECASE),
    "mongodb": re.compile(r"\bmongodb\b", re.IGNORECASE),
    "kubernetes": re.compile(r"\bkubernetes\b", re.IGNORECASE),
    "postgresql": re.compile(r"\bpostgresql\b", re.IGNORECASE),
    "sql-server": re.compile(r"\bsql server\b", re.IGNORECASE),
    "cosmosdb": re.compile(r"\bcosmosdb\b", re.IGNORECASE),
    "kafka": re.compile(r"\bkafka\b", re.IGNORECASE),
    "oauth2": re.compile(r"\boauth2\b", re.IGNORECASE),
    "oauth": re.compile(r"\boauth\b", re.IGNORECASE),
    "sso": re.compile(r"\bsso\b", re.IGNORECASE),
    "scim": re.compile(r"\bscim\b", re.IGNORECASE),
    "jwt": re.compile(r"\bjwt\b", re.IGNORECASE),
    "saml": re.compile(r"\bsaml\b", re.IGNORECASE),
    "webhooks": re.compile(r"\bwebhooks\b", re.IGNORECASE),
    "kong": re.compile(r"\bkong\b", re.IGNORECASE),
    "git": re.compile(r"\bgit\b", re.IGNORECASE),
    "github": re.compile(r"\bgithub\b", re.IGNORECASE),
}
WORK_STYLE_PATTERNS = {
    "hybrid": re.compile(r"\bhybrid\b", re.IGNORECASE),
    "on-site": re.compile(r"\bon-site\b|\bonsite\b", re.IGNORECASE),
    "remote": re.compile(r"\bremote\b", re.IGNORECASE),
    "on-call": re.compile(r"\bon-call\b", re.IGNORECASE),
}
DOMAIN_SIGNAL_PATTERNS = {
    "authentication": re.compile(r"\bauthentication\b", re.IGNORECASE),
    "security": re.compile(r"\bsecurity\b", re.IGNORECASE),
    "fraud": re.compile(r"\bfraud\b|\baccount takeover\b|\bATO\b", re.IGNORECASE),
    "distributed-systems": re.compile(r"\bdistributed systems\b", re.IGNORECASE),
    "backend": re.compile(r"\bbackend(?: systems?| services?)?\b", re.IGNORECASE),
    "account-management": re.compile(r"\baccount management\b", re.IGNORECASE),
    "integrations": re.compile(r"\bintegrations?\b|\bintegration platform\b", re.IGNORECASE),
    "apis": re.compile(r"\bapi\b|\bapis\b|\bapi gateways\b|\bapi development\b", re.IGNORECASE),
    "microservices": re.compile(r"\bmicroservices architecture\b|\bmicroservices\b", re.IGNORECASE),
    "event-streaming": re.compile(r"\bevent streaming\b|\bmessage queues\b|\bservice bus\b|\bkafka\b", re.IGNORECASE),
    "iam": re.compile(r"\biam\b|\bidentity and access management\b", re.IGNORECASE),
    "developer-platform": re.compile(
        r"\bdeveloper platform\b|\bdeveloper ecosystems?\b|\bproduct platform\b|\bdeveloper experience\b",
        re.IGNORECASE,
    ),
    "developer-productivity": re.compile(r"\bdeveloper productivity\b|\bworkflow engine\b|\bdevelopment workflow\b", re.IGNORECASE),
    "event-driven": re.compile(r"\bevent-driven architectures?\b|\basynchronous messaging systems?\b", re.IGNORECASE),
    "observability": re.compile(r"\bobservability\b|\blogging\b|\btracing\b", re.IGNORECASE),
    "ci-cd": re.compile(r"\bci/cd\b|\bbuild systems?\b|\bdeveloper workflows\b", re.IGNORECASE),
}
ROLE_TYPE_PATTERNS = (
    ("backend", re.compile(r"\bbackend\b", re.IGNORECASE)),
    ("full-stack", re.compile(r"\bfull[ -]?stack\b", re.IGNORECASE)),
    ("platform", re.compile(r"\bplatform\b", re.IGNORECASE)),
    ("frontend", re.compile(r"\bfront[ -]?end\b", re.IGNORECASE)),
    ("mobile", re.compile(r"\bmobile\b|\bios\b|\bandroid\b", re.IGNORECASE)),
)
MID_LEVEL_PATTERN = re.compile(r"\b(engineer ii|software engineer ii|mid(?:-level)?|intermediate)\b", re.IGNORECASE)
SENIOR_LEVEL_PATTERN = re.compile(r"\b(senior|sr\.?|staff|principal|lead)\b", re.IGNORECASE)
JUNIOR_LEVEL_PATTERN = re.compile(r"\b(junior|entry[ -]?level|new grad|intern)\b", re.IGNORECASE)


def parse_job_description(raw_text: str) -> ParsedJob:
    """Parse a raw job description into directly extracted fields."""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    content_lines = [line for line in lines if not _is_ignored_opening_line(line)]
    title = _extract_title(content_lines)
    opening_text = "\n".join(content_lines[:6])
    location = _extract_location(lines)

    company = _extract_company(raw_text, opening_text)
    years_required = _extract_years_experience_required(raw_text)
    salary_min, salary_max, salary_currency, salary_period = _extract_salary(lines)

    return ParsedJob(
        raw_text=raw_text,
        title=title,
        company=company,
        location=location,
        years_experience_required=years_required,
        seniority=_extract_seniority(title, years_required),
        role_type=_extract_role_type(raw_text, title),
        salary_min=salary_min,
        salary_max=salary_max,
        salary_currency=salary_currency,
        salary_period=salary_period,
        technologies=_extract_technologies(raw_text),
        domain_signals=_extract_domain_signals(raw_text),
        work_style_signals=_extract_work_style_signals(raw_text),
    )


def _normalize_currency(raw_currency: str) -> str:
    currency = raw_currency.upper()
    if currency in {"CA", "CAN", "CAD"}:
        return "CAD"
    if currency in {"US", "USD"}:
        return "USD"
    return currency


def _extract_company(raw_text: str, opening_text: str) -> str | None:
    company_match = COMPANY_PATTERN.search(opening_text)
    if company_match:
        return company_match.group(1)

    header_company = _extract_company_from_header(raw_text)
    if header_company:
        return header_company

    at_company_match = AT_COMPANY_PATTERN.search(raw_text)
    if at_company_match:
        return at_company_match.group(1)

    return None


def _extract_company_from_header(raw_text: str) -> str | None:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if len(lines) < 2:
        return None

    if lines[0].lower().endswith(" logo"):
        candidate = lines[1]
        lowered = candidate.lower()
        if lowered not in {"share", "show more options"} and " · " not in candidate:
            return candidate

    return None


def _extract_salary(lines: list[str]) -> tuple[int | None, int | None, str | None, str | None]:
    for line in lines:
        normalized_line = line.strip()
        if not normalized_line:
            continue

        salary_thousands_range_match = SALARY_THOUSANDS_RANGE_PATTERN.search(normalized_line)
        if salary_thousands_range_match:
            return (
                int(salary_thousands_range_match.group(1).replace(",", "")) * 1000,
                int(salary_thousands_range_match.group(2).replace(",", "")) * 1000,
                _normalize_currency(salary_thousands_range_match.group(3)),
                "yearly",
            )

        salary_match = SALARY_PATTERN.search(normalized_line)
        if salary_match:
            return (
                int(salary_match.group(2).replace(",", "")),
                int(salary_match.group(3).replace(",", "")),
                _normalize_currency(salary_match.group(1)),
                "yearly",
            )

        salary_range_match = SALARY_RANGE_PATTERN.search(normalized_line)
        if salary_range_match:
            return (
                int(salary_range_match.group(1).replace(",", "")),
                int(salary_range_match.group(2).replace(",", "")),
                "CAD",
                "yearly",
            )

        salary_between_match = SALARY_BETWEEN_PATTERN.search(normalized_line)
        if salary_between_match:
            return (
                int(salary_between_match.group(1).replace(",", "")),
                int(salary_between_match.group(2).replace(",", "")),
                "CAD",
                "yearly",
            )

        salary_currency_range_match = SALARY_CURRENCY_RANGE_PATTERN.search(normalized_line)
        if salary_currency_range_match:
            return (
                int(salary_currency_range_match.group(2).replace(",", "")),
                int(salary_currency_range_match.group(3).replace(",", "")),
                _normalize_currency(salary_currency_range_match.group(1)),
                "yearly",
            )

    return None, None, None, None


def _extract_years_experience_required(raw_text: str) -> float | None:
    for line in raw_text.splitlines():
        normalized_line = line.strip()
        if not normalized_line:
            continue
        lowered = normalized_line.lower()
        if "experience" not in lowered and "exp" not in lowered:
            continue

        years_required = _extract_years_from_line(normalized_line)
        if years_required is not None:
            return years_required

    return None


def _extract_years_from_line(line: str) -> float | None:
    range_match = EXPERIENCE_RANGE_PATTERN.search(line)
    if range_match:
        return float(range_match.group(1))

    years_match = EXPERIENCE_PATTERN.search(line)
    if years_match:
        return float(years_match.group(1))

    return None


def _extract_location(lines: list[str]) -> str | None:
    for index, line in enumerate(lines[:20]):
        lowered = line.lower()
        if lowered in {"job location", "location"} and index + 1 < len(lines):
            candidate = _normalize_location_candidate(lines[index + 1].lstrip("|").strip())
            if candidate:
                return candidate
        if line.startswith("Job category:") or line.startswith("Requisition number:"):
            continue
        normalized_line = _normalize_location_candidate(line)
        if REMOTE_POSITION_PATTERN.match(normalized_line):
            return "Remote"
        if REMOTE_ONLY_LOCATION_PATTERN.match(normalized_line):
            return normalized_line
        if REMOTE_LOCATION_PATTERN.match(normalized_line):
            return normalized_line
        if COUNTRY_LOCATION_PATTERN.match(normalized_line):
            return normalized_line
        if LONG_LOCATION_PATTERN.match(normalized_line):
            return normalized_line
        if LOCATION_PATTERN.match(normalized_line):
            if ", CAN" in normalized_line:
                return normalized_line.split(", CAN", maxsplit=1)[0]
            return normalized_line
    return None


def _extract_title(lines: list[str]) -> str | None:
    ignored_prefixes = (
        "share",
        "show more options",
        "save",
        "easy apply",
        "about the job",
        "applied ",
        "see application",
    )

    for line in lines[:20]:
        normalized_line = line.strip()
        if not normalized_line:
            continue

        lowered = normalized_line.lower()
        if lowered.endswith(" logo"):
            continue
        if lowered.startswith(ignored_prefixes):
            continue
        if _is_section_heading(normalized_line):
            continue
        phrase_match = TITLE_PHRASE_PATTERN.search(normalized_line)
        if " at " in lowered and phrase_match:
            return phrase_match.group(0)
        if TITLE_PATTERN.search(normalized_line):
            return normalized_line
        if phrase_match:
            return phrase_match.group(0)

    return None


def _is_ignored_opening_line(line: str) -> bool:
    lowered = line.strip().lower()
    return lowered in {
        "this is a remote position.",
        "this is a remote position",
    }


def _is_section_heading(line: str) -> bool:
    return line.strip().lower() in {
        "about us:",
        "role overview:",
        "key responsibilities:",
        "tech stack:",
        "qualifications:",
        "preferred skills:",
        "what we offer:",
    }


def _normalize_location_candidate(line: str) -> str:
    candidate = line.split(" · ", maxsplit=1)[0]
    candidate = re.sub(r"\s+\([^)]*\)$", "", candidate)
    return candidate.strip()


def _extract_technologies(raw_text: str) -> list[str]:
    return [
        technology
        for technology, pattern in TECHNOLOGY_PATTERNS.items()
        if pattern.search(raw_text)
    ]


def _extract_work_style_signals(raw_text: str) -> list[str]:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    detected_signals: list[str] = []

    for index, line in enumerate(lines):
        if line.lower() == "remote work policy" and index + 1 < len(lines):
            policy_value = lines[index + 1].strip().lower()
            if policy_value in {"in office", "in-office", "on-site", "onsite"}:
                detected_signals.append("on-site")
            elif "hybrid" in policy_value:
                detected_signals.append("hybrid")
            elif "remote" in policy_value:
                detected_signals.append("remote")

    sanitized_text = re.sub(r"\bRemote Work Policy\b", "", raw_text, flags=re.IGNORECASE)

    for signal, pattern in WORK_STYLE_PATTERNS.items():
        if pattern.search(sanitized_text):
            detected_signals.append(signal)

    deduped_signals = list(dict.fromkeys(detected_signals))
    if "on-site" in deduped_signals and "remote" in deduped_signals:
        deduped_signals.remove("remote")

    return deduped_signals


def _extract_domain_signals(raw_text: str) -> list[str]:
    return [
        signal
        for signal, pattern in DOMAIN_SIGNAL_PATTERNS.items()
        if pattern.search(raw_text)
    ]


def _extract_role_type(raw_text: str, title: str | None) -> str | None:
    title_text = title or ""

    if re.search(r"\bintegrations?\b", title_text, re.IGNORECASE):
        return "platform"

    for role_type, pattern in ROLE_TYPE_PATTERNS:
        if pattern.search(title_text):
            return role_type

    search_text = "\n".join(filter(None, [title, _text_for_role_inference(raw_text)]))

    for role_type, pattern in ROLE_TYPE_PATTERNS:
        if role_type in {"platform", "mobile"}:
            continue
        if pattern.search(search_text):
            return role_type

    return None


def _text_for_role_inference(raw_text: str) -> str:
    return re.sub(
        r"\bSkills\b.*?\bAbout the job\b",
        "About the job",
        raw_text,
        flags=re.IGNORECASE | re.DOTALL,
    )


def _extract_seniority(
    title: str | None,
    years_required: float | None,
) -> str | None:
    title_text = title or ""

    if SENIOR_LEVEL_PATTERN.search(title_text):
        return "senior"

    if MID_LEVEL_PATTERN.search(title_text):
        return "mid"

    if JUNIOR_LEVEL_PATTERN.search(title_text):
        return "junior"

    if years_required is not None:
        if years_required < 1.0:
            return "junior"
        if years_required <= 3.0:
            return "mid"
        if years_required >= 5.0:
            return "senior"

    return None

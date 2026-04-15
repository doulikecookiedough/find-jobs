"""Job description parsing utilities."""

from __future__ import annotations

import re

from find_jobs.models import ParsedJob


COMPANY_PATTERN = re.compile(
    r"^(?!Our company\b)([A-Z][A-Za-z0-9&'., -]+?) is\b",
    re.MULTILINE,
)
AT_COMPANY_PATTERN = re.compile(r"\bAt\s+([A-Z][A-Za-z0-9&'. -]+),", re.MULTILINE)
TITLE_AT_COMPANY_PATTERN = re.compile(
    r"^(?P<title>.+?)\s+at\s+(?P<company>[A-Z][A-Za-z0-9&'. -]+)$",
    re.IGNORECASE,
)
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
SALARY_BARE_THOUSANDS_RANGE_PATTERN = re.compile(
    r"\$([\d,]+)k\s*[–-]\s*\$([\d,]+)k\b",
    re.IGNORECASE,
)
LOCATION_PATTERN = re.compile(
    r"^[A-Z][A-Za-z .'-]+,\s*[A-Z]{2}(?:\s+[A-Z]\d[A-Z]\d[A-Z]\d,\s*[A-Z]{3})?$"
)
COUNTRY_LOCATION_PATTERN = re.compile(r"^(Canada|United States|USA|US)$", re.IGNORECASE)
REMOTE_LOCATION_PATTERN = re.compile(r"^Remote\s+(Canada|United States|USA|US)$", re.IGNORECASE)
REMOTE_ONLY_LOCATION_PATTERN = re.compile(r"^Remote$", re.IGNORECASE)
REMOTE_POSITION_PATTERN = re.compile(r"^This is a remote position\.?$", re.IGNORECASE)
LONG_LOCATION_PATTERN = re.compile(
    r"^[A-Z][A-Za-z .'-]+,\s*[A-Z][A-Za-z .'-]+,\s*[A-Z][A-Za-z .'-]+$"
)
TITLE_PATTERN = re.compile(
    (
        r"^(?=.*\b(?:engineer|engineering|developer)\b)"
        r"(?=.*\b(?:software|backend|back-end|frontend|front-end|full-stack|full stack|platform|data|"
        r"product|zuora|salesforce|netsuite|mulesoft|senior|junior|staff|principal|lead|"
        r"entry[ -]?level)\b).+$"
    ),
    re.IGNORECASE,
)
TITLE_PHRASE_PATTERN = re.compile(
    (
        r"\b(?:Senior|Junior|Staff|Principal|Lead)\s+(?:Software\s+)?"
        r"(?:Engineer|Developer)\b|\b(?:Software|Backend|Back-End|Frontend|Front-End|Full-Stack|"
        r"Platform|Data|Product|Zuora|Salesforce)\s+(?:Engineer|Developer)\b|"
        r"\b[A-Z][A-Za-z0-9+#./ -]*\b(?:Engineer|Developer)\s*[-,]\s*Entry[ -]?Level\b"
    ),
    re.IGNORECASE,
)
IGNORED_COMPANY_LINES = {
    "ready to interview",
    "home",
    "profile",
    "jobs",
    "applied",
    "messages",
    "discover",
    "on-demand",
    "refer a friend",
    "earn $200",
}
TECHNOLOGY_PATTERNS = {
    "c#": re.compile(r"(?<!\w)c#(?!\w)", re.IGNORECASE),
    "dotnet-core": re.compile(r"\.net core\b|\bdotnet core\b", re.IGNORECASE),
    "typescript": re.compile(r"\btypescript\b", re.IGNORECASE),
    "javascript": re.compile(r"\bjavascript\b", re.IGNORECASE),
    "go": re.compile(r"\bgo\b(?!-)", re.IGNORECASE),
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
    "dbt": re.compile(r"\bdbt\b", re.IGNORECASE),
    "snowflake": re.compile(r"\bsnowflake\b", re.IGNORECASE),
    "looker": re.compile(r"\blooker\b|\blookml\b", re.IGNORECASE),
    "zuora": re.compile(r"\bzuora\b", re.IGNORECASE),
    "salesforce": re.compile(r"\bsalesforce\b", re.IGNORECASE),
    "servicenow": re.compile(r"\bservicenow\b", re.IGNORECASE),
    "cpq": re.compile(r"\bcpq\b", re.IGNORECASE),
    "netsuite": re.compile(r"\bnetsuite\b", re.IGNORECASE),
    "revpro": re.compile(r"\brevpro\b", re.IGNORECASE),
    "mulesoft": re.compile(r"\bmulesoft\b", re.IGNORECASE),
    "itsm": re.compile(r"\bitsm\b", re.IGNORECASE),
    "csm": re.compile(r"\bcsm\b", re.IGNORECASE),
    "spm": re.compile(r"\bspm\b", re.IGNORECASE),
    "itom": re.compile(r"\bitom\b", re.IGNORECASE),
    "hrsd": re.compile(r"\bhrsd\b", re.IGNORECASE),
    "rest-apis": re.compile(r"\brest apis?\b", re.IGNORECASE),
    "aws": re.compile(r"\baws\b", re.IGNORECASE),
    "azure": re.compile(r"\bazure\b", re.IGNORECASE),
    "docker": re.compile(r"\bdocker\b", re.IGNORECASE),
    "cuda": re.compile(r"\bcuda\b", re.IGNORECASE),
    "tensorrt": re.compile(r"\btensorrt\b", re.IGNORECASE),
    "triton-inference-server": re.compile(
        r"\btriton inference server\b|\bnvidia triton\b", re.IGNORECASE
    ),
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
    "business-systems": re.compile(
        (
            r"\bzuora\b|\bsalesforce\b|\bcpq\b|\bnetsuite\b|\brevpro\b|"
            r"\bmulesoft\b|\bservicenow\b|\bitsm\b|\bcsm\b|\bspm\b|"
            r"\bitom\b|\bhrsd\b|\bquote-to-cash\b|\border-to-revenue\b"
        ),
        re.IGNORECASE,
    ),
    "apis": re.compile(r"\bapi\b|\bapis\b|\bapi gateways\b|\bapi development\b", re.IGNORECASE),
    "microservices": re.compile(r"\bmicroservices architecture\b|\bmicroservices\b", re.IGNORECASE),
    "event-streaming": re.compile(
        r"\bevent streaming\b|\bmessage queues\b|\bservice bus\b|\bkafka\b", re.IGNORECASE
    ),
    "iam": re.compile(r"\biam\b|\bidentity and access management\b", re.IGNORECASE),
    "developer-platform": re.compile(
        (
            r"\bdeveloper platform\b|\bdeveloper ecosystems?\b|"
            r"\bproduct platform\b|\bdeveloper experience\b"
        ),
        re.IGNORECASE,
    ),
    "product-engineering": re.compile(
        r"\bproduct engineers?\b|\bproduct engineer\b",
        re.IGNORECASE,
    ),
    "developer-productivity": re.compile(
        r"\bdeveloper productivity\b|\bworkflow engine\b|\bdevelopment workflow\b", re.IGNORECASE
    ),
    "event-driven": re.compile(
        r"\bevent-driven architectures?\b|\basynchronous messaging systems?\b", re.IGNORECASE
    ),
    "observability": re.compile(r"\bobservability\b|\blogging\b|\btracing\b", re.IGNORECASE),
    "ci-cd": re.compile(r"\bci/cd\b|\bbuild systems?\b|\bdeveloper workflows\b", re.IGNORECASE),
    "gpu-computing": re.compile(
        r"\bgpu computing\b|\bnvidia cuda\b|\bgpu memory\b", re.IGNORECASE
    ),
    "model-serving": re.compile(
        (
            r"\bmodel serving\b|\binference serving\b|\btriton inference server\b|"
            r"\bai/ml serving\b|\bmodel optimization\b"
        ),
        re.IGNORECASE,
    ),
    "edge-inference": re.compile(
        r"\bedge inference\b|\bedge inference infrastructure\b|\bedge nodes\b", re.IGNORECASE
    ),
    "ml-infrastructure": re.compile(
        r"\bai inference\b|\bml infrastructure\b|\bai/ml serving\b|\btensorrt\b",
        re.IGNORECASE,
    ),
}
ROLE_TYPE_PATTERNS = (
    (
        "product-engineering",
        re.compile(
            r"\bproduct engineer(?:ing)?\b|\bproduct engineers?\b|\bproduct engineer\b",
            re.IGNORECASE,
        ),
    ),
    ("backend", re.compile(r"\bbackend\b", re.IGNORECASE)),
    ("full-stack", re.compile(r"\bfull[ -]?stack\b", re.IGNORECASE)),
    ("platform", re.compile(r"\bplatform\b", re.IGNORECASE)),
    (
        "data",
        re.compile(
            r"\bdata engineer(?:ing)?\b|\bdata platform\b|\bdata pipelines?\b", re.IGNORECASE
        ),
    ),
    (
        "business-systems",
        re.compile(
            (
                r"\bzuora developer\b|\bzuora\b|\bsalesforce\b|\bcpq\b|"
                r"\bnetsuite\b|\brevpro\b|\bmulesoft\b|\bservicenow\b"
            ),
            re.IGNORECASE,
        ),
    ),
    ("frontend", re.compile(r"\bfront[ -]?end\b", re.IGNORECASE)),
    ("mobile", re.compile(r"\bmobile\b|\bios\b|\bandroid\b", re.IGNORECASE)),
)
MID_LEVEL_PATTERN = re.compile(
    r"\b(engineer ii|software engineer ii|mid(?:-level)?|intermediate)\b", re.IGNORECASE
)
SENIOR_LEVEL_PATTERN = re.compile(r"\b(senior|sr\.?|staff|principal|lead)\b", re.IGNORECASE)
JUNIOR_LEVEL_PATTERN = re.compile(r"\b(junior|entry[ -]?level|new grad|intern)\b", re.IGNORECASE)


def parse_job_description(raw_text: str) -> ParsedJob:
    """Parse a raw job description into directly extracted fields."""
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    content_lines = [line for line in lines if not _is_ignored_opening_line(line)]
    title = _extract_title(content_lines)
    opening_text = "\n".join(content_lines[:6])
    location = _extract_location(lines)

    company = _extract_company(raw_text, opening_text, title)
    years_required, max_years_required = _extract_years_experience_required(raw_text)
    salary_min, salary_max, salary_currency, salary_period = _extract_salary(lines)

    return ParsedJob(
        raw_text=raw_text,
        title=title,
        company=company,
        location=location,
        years_experience_required=years_required,
        years_experience_max_required=max_years_required,
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


def _extract_company(raw_text: str, opening_text: str, title: str | None = None) -> str | None:
    title_company = _extract_company_from_title(raw_text)
    if title_company:
        return title_company

    company_match = COMPANY_PATTERN.search(opening_text)
    if company_match:
        return company_match.group(1)

    title_adjacent_company = _extract_company_after_title(raw_text, title)
    if title_adjacent_company:
        return title_adjacent_company

    header_company = _extract_company_from_header(raw_text)
    if header_company:
        return header_company

    at_company_match = AT_COMPANY_PATTERN.search(raw_text)
    if at_company_match:
        return at_company_match.group(1)

    return None


def _extract_company_from_title(raw_text: str) -> str | None:
    """Extract company from `Title at Company` lines when present."""

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    for line in lines[:25]:
        match = TITLE_AT_COMPANY_PATTERN.match(line)
        if not match:
            continue
        title = match.group("title").strip()
        if not _looks_like_title_text(title):
            continue
        company = match.group("company").strip()
        if _is_probable_company_name(company):
            return company
    return None


def _extract_company_from_header(raw_text: str) -> str | None:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    if not lines:
        return None

    if len(lines) >= 2 and _looks_like_title_text(lines[0]) and _looks_like_company_after_title(
        lines[1]
    ):
        return lines[1]

    if lines[0].lower().endswith(" logo"):
        if len(lines) < 2:
            return None
        candidate = lines[1]
        lowered = candidate.lower()
        if lowered not in {"share", "show more options"} and " · " not in candidate:
            return candidate

    candidate = lines[0]
    if _is_probable_company_name(candidate):
        return candidate

    return None


def _extract_company_after_title(raw_text: str, title: str | None) -> str | None:
    """Read the line after the title when it looks like a company name."""

    if not title:
        return None

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    try:
        title_index = lines.index(title)
    except ValueError:
        return None

    if title_index + 1 >= len(lines):
        return None

    candidate = lines[title_index + 1]
    return candidate if _looks_like_company_after_title(candidate) else None


def _extract_salary(lines: list[str]) -> tuple[int | None, int | None, str | None, str | None]:
    """Extract the first supported salary range from the job text."""

    for line in lines:
        normalized_line = line.strip()
        if not normalized_line:
            continue

        salary = _extract_salary_from_line(normalized_line)
        if salary is not None:
            return salary

    return None, None, None, None


def _extract_years_experience_required(raw_text: str) -> tuple[float | None, float | None]:
    """Extract the years requirement, preserving both ends of explicit ranges."""

    best_years_required: tuple[float | None, float | None] = (None, None)
    best_priority = -10_000

    for line in raw_text.splitlines():
        normalized_line = line.strip()
        if not normalized_line:
            continue
        lowered = normalized_line.lower()
        if "experience" not in lowered and "exp" not in lowered:
            continue

        years_required = _extract_years_from_line(normalized_line)
        if years_required == (None, None):
            continue

        priority = _experience_line_priority(normalized_line, years_required)
        if priority > best_priority:
            best_years_required = years_required
            best_priority = priority

    return best_years_required


def _extract_years_from_line(line: str) -> tuple[float | None, float | None]:
    """Extract a minimum and optional maximum years requirement from one line."""

    range_match = EXPERIENCE_RANGE_PATTERN.search(line)
    if range_match:
        return float(range_match.group(1)), float(range_match.group(2))

    years_match = EXPERIENCE_PATTERN.search(line)
    if years_match:
        years_required = float(years_match.group(1))
        return years_required, years_required

    return None, None


def _experience_line_priority(
    line: str,
    years_required: tuple[float | None, float | None],
) -> int:
    """Rank experience lines so richer requirement lines beat shorthand headers."""

    lower_years, upper_years = years_required
    priority = 0
    normalized_line = line.lower()

    if upper_years is not None and lower_years is not None and upper_years > lower_years:
        priority += 100
    if "hands-on experience" in normalized_line:
        priority += 30
    if "years of experience" in normalized_line:
        priority += 20
    if "professional experience" in normalized_line:
        priority += 15
    if "relevant experience" in normalized_line:
        priority += 10
    if "experience as" in normalized_line or "experience in" in normalized_line:
        priority += 10
    if "at least" in normalized_line:
        priority += 25
    if "you’ll bring" in normalized_line or "you'll bring" in normalized_line:
        priority += 20
    if "bonus points" in normalized_line:
        priority -= 10
    if _looks_like_bio_line(normalized_line):
        priority -= 60
    if "|" in line:
        priority -= 20

    return priority


def _extract_location(lines: list[str]) -> str | None:
    """Extract the first plausible location string from the opening lines."""

    for index, line in enumerate(lines[:20]):
        candidate = _extract_location_candidate(index, line, lines)
        if candidate:
            return candidate
    for index, line in enumerate(lines):
        if line.lower() not in {"job location", "location", "hires remotely in"}:
            continue
        candidate = _extract_location_candidate(index, line, lines)
        if candidate:
            return candidate
    return None


def _extract_title(lines: list[str]) -> str | None:
    """Extract the first plausible job title from the opening lines."""

    ignored_prefixes = (
        "share",
        "show more options",
        "save",
        "easy apply",
        "about the job",
        "applied ",
        "see application",
    )

    for line in lines[:40]:
        normalized_line = re.sub(r"\s+\|\s+LinkedIn$", "", line.strip(), flags=re.IGNORECASE)
        if not normalized_line:
            continue

        lowered = normalized_line.lower()
        if _looks_like_salary_line(normalized_line):
            continue
        if lowered.endswith(" logo"):
            continue
        if lowered.startswith(ignored_prefixes):
            continue
        if _is_section_heading(normalized_line):
            continue
        title_at_company_match = TITLE_AT_COMPANY_PATTERN.match(normalized_line)
        if title_at_company_match and TITLE_PATTERN.search(title_at_company_match.group("title")):
            return title_at_company_match.group("title").strip()
        phrase_match = TITLE_PHRASE_PATTERN.search(normalized_line)
        if " at " in lowered and phrase_match:
            return phrase_match.group(0)
        if TITLE_PATTERN.search(normalized_line):
            return normalized_line
        if phrase_match:
            return phrase_match.group(0)

    return None


def _looks_like_title_text(text: str) -> bool:
    """Return whether a string is structured like a plausible job title."""

    normalized_text = text.strip()
    if not normalized_text:
        return False
    if len(normalized_text.split()) > 10:
        return False
    return bool(TITLE_PATTERN.search(normalized_text) or TITLE_PHRASE_PATTERN.search(normalized_text))


def _looks_like_salary_line(line: str) -> bool:
    normalized_line = line.replace("—", "-").replace("–", "-")
    if re.search(r"\$\s*[\d,]+k\s*-\s*\$\s*[\d,]+k\b", normalized_line, re.IGNORECASE):
        return True
    if re.search(r"\$\s*[\d,]+\s*-\s*\$\s*[\d,]+\b", normalized_line, re.IGNORECASE):
        return True
    return any(
        pattern.search(normalized_line)
        for pattern in (
            SALARY_THOUSANDS_RANGE_PATTERN,
            SALARY_PATTERN,
            SALARY_RANGE_PATTERN,
            SALARY_BETWEEN_PATTERN,
            SALARY_CURRENCY_RANGE_PATTERN,
        )
    )


def _is_probable_company_name(line: str) -> bool:
    """Filter out common non-company strings from header candidates."""

    normalized_line = line.strip()
    lowered = normalized_line.lower()
    return not any(
        (
            not normalized_line,
            normalized_line.endswith("."),
            "|" in normalized_line,
            _looks_like_salary_line(normalized_line),
            len(normalized_line.split()) > 6,
            lowered
            in {
                *IGNORED_COMPANY_LINES,
                "share",
                "save",
                "about the job",
                "show more options",
                "actively hiring",
                "job location",
                "remote work policy",
                "visa sponsorship",
                "relocation",
                "skills",
            },
            lowered.startswith(
                (
                    "posted:",
                    "reposted:",
                    "top job picks",
                    "avatar for ",
                    "help people and businesses",
                    "job category:",
                    "requisition number:",
                ),
            ),
            bool(TITLE_PATTERN.search(normalized_line)),
            _looks_like_location(normalized_line),
        )
    )


def _looks_like_bio_line(line: str) -> bool:
    return bool(
        re.search(
            r"\b(cto|ceo|designer|manager|coordinator|analyst|employee|lead|founder)\b",
            line,
            re.IGNORECASE,
        )
        or "years of experience within" in line
        or "years of experience as a" in line
    )


def _looks_like_location(line: str) -> bool:
    """Return whether a line matches one of the supported location formats."""

    return any(
        pattern.match(line)
        for pattern in (
            LOCATION_PATTERN,
            COUNTRY_LOCATION_PATTERN,
            REMOTE_LOCATION_PATTERN,
            REMOTE_ONLY_LOCATION_PATTERN,
            REMOTE_POSITION_PATTERN,
            LONG_LOCATION_PATTERN,
        )
    )


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
        signal for signal, pattern in DOMAIN_SIGNAL_PATTERNS.items() if pattern.search(raw_text)
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
        if role_type in {"platform", "mobile", "product-engineering"}:
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
    """Infer seniority from title cues first, then fall back to years required."""

    title_text = title or ""
    for seniority, pattern in (
        ("senior", SENIOR_LEVEL_PATTERN),
        ("mid", MID_LEVEL_PATTERN),
        ("junior", JUNIOR_LEVEL_PATTERN),
    ):
        if pattern.search(title_text):
            return seniority

    return _seniority_from_years(years_required)


def _looks_like_company_after_title(candidate: str) -> bool:
    """Validate whether the line after the title still looks like a company name."""

    lowered = candidate.lower()
    return not any(
        (
            " · " in candidate,
            _looks_like_salary_line(candidate),
            lowered.startswith(
                (
                    "job category:",
                    "requisition number:",
                    "location:",
                    "remote work policy",
                    "remote",
                    "hybrid",
                    "on-site",
                    "onsite",
                    "in office",
                )
            ),
            lowered in {"about the job", "apply", "save", "share", "show more options"},
            lowered
            in {"remote", "on-site", "onsite", "in office", "hybrid", "full-time", "full time"},
            bool(TITLE_PATTERN.search(candidate)),
            _looks_like_location(candidate),
        )
    )


def _extract_salary_from_line(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Return the first supported salary tuple found in a normalized line."""

    salary_extractors = (
        _extract_thousands_salary_range,
        _extract_bare_thousands_salary_range,
        _extract_currency_salary_range,
        _extract_plain_salary_range,
        _extract_between_salary_range,
        _extract_prefixed_currency_salary_range,
    )
    for extractor in salary_extractors:
        salary = extractor(normalized_line)
        if salary is not None:
            return salary

    return None


def _extract_thousands_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a salary range written in thousands with an explicit currency."""

    match = SALARY_THOUSANDS_RANGE_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(1).replace(",", "")) * 1000,
        int(match.group(2).replace(",", "")) * 1000,
        _normalize_currency(match.group(3)),
        "yearly",
    )


def _extract_bare_thousands_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a salary range written in thousands without a currency code."""

    match = SALARY_BARE_THOUSANDS_RANGE_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(1).replace(",", "")) * 1000,
        int(match.group(2).replace(",", "")) * 1000,
        None,
        "yearly",
    )


def _extract_currency_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a salary range with a single leading currency label."""

    match = SALARY_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(2).replace(",", "")),
        int(match.group(3).replace(",", "")),
        _normalize_currency(match.group(1)),
        "yearly",
    )


def _extract_plain_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a plain dollar salary range with yearly wording."""

    match = SALARY_RANGE_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(1).replace(",", "")),
        int(match.group(2).replace(",", "")),
        "CAD",
        "yearly",
    )


def _extract_between_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a salary range written as 'between X and Y'."""

    match = SALARY_BETWEEN_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(1).replace(",", "")),
        int(match.group(2).replace(",", "")),
        "CAD",
        "yearly",
    )


def _extract_prefixed_currency_salary_range(
    normalized_line: str,
) -> tuple[int, int, str | None, str] | None:
    """Extract a salary range where each value carries a currency prefix."""

    match = SALARY_CURRENCY_RANGE_PATTERN.search(normalized_line)
    if not match:
        return None

    return (
        int(match.group(2).replace(",", "")),
        int(match.group(3).replace(",", "")),
        _normalize_currency(match.group(1)),
        "yearly",
    )


def _extract_location_candidate(index: int, line: str, lines: list[str]) -> str | None:
    """Extract one plausible location candidate from a header line."""

    lowered = line.lower()
    if lowered in {"job location", "location"} and index + 1 < len(lines):
        candidate = _normalize_location_candidate(lines[index + 1].lstrip("|").strip())
        if candidate:
            return candidate
    if lowered == "hires remotely in" and index + 1 < len(lines):
        candidate = _normalize_location_candidate(lines[index + 1].strip())
        if candidate:
            return candidate

    if line.startswith("Job category:") or line.startswith("Requisition number:"):
        return None

    normalized_line = _normalize_location_candidate(line)
    if REMOTE_POSITION_PATTERN.match(normalized_line):
        return "Remote"
    if _looks_like_location(normalized_line):
        return (
            normalized_line.split(", CAN", maxsplit=1)[0]
            if ", CAN" in normalized_line
            else normalized_line
        )

    return None


def _seniority_from_years(years_required: float | None) -> str | None:
    """Infer seniority from the years requirement when title cues are absent."""

    if years_required is None:
        return None
    if years_required < 1.0:
        return "junior"
    if years_required <= 3.0:
        return "mid"
    if years_required >= 5.0:
        return "senior"
    return None

"""Regex patterns used by fit-strength scoring.

These patterns stay separate so the strength vocabulary is easy to review
without reading the full fit-scoring implementation.
"""

from __future__ import annotations

import re


STRENGTH_PATTERNS = {
    "backend": re.compile(r"\bbackend(?: systems?| services?| infrastructure)?\b", re.IGNORECASE),
    "full-stack": re.compile(
        r"\bfull[ -]?stack\b|\bfront-end to back-end\b|\bacross the stack\b", re.IGNORECASE
    ),
    "product-engineering": re.compile(
        r"\bproduct decisions?\b|\bcustomer value\b|\bproduct development\b|\bproduct-oriented\b",
        re.IGNORECASE,
    ),
    "data-platforms": re.compile(
        r"\bdata platforms?\b|\bdata pipelines?\b|\bdata lake\b", re.IGNORECASE
    ),
    "distributed-systems": re.compile(
        r"\bdistributed systems?\b|\bsystems? that scale\b|\bscalable\b", re.IGNORECASE
    ),
    "data-integrity": re.compile(
        r"\bdata integrity\b|\bconsistency\b|\bcorrectness\b", re.IGNORECASE
    ),
    "concurrency": re.compile(r"\bconcurr(?:ent|ency)\b|\basynchronous\b|\basync\b", re.IGNORECASE),
    "schema-migrations": re.compile(
        r"\bschema migrations?\b|\bdatabase migrations?\b|\bdata backfill\b", re.IGNORECASE
    ),
    "apis": re.compile(r"\bapi\b|\bapis\b|\brest apis?\b|\brestful apis?\b", re.IGNORECASE),
    "integrations": re.compile(r"\bintegrations?\b|\bintegration platform\b", re.IGNORECASE),
    "reliability": re.compile(
        r"\breliability\b|\breliable\b|\bproduction systems?\b|\bon-call\b", re.IGNORECASE
    ),
    "etl": re.compile(r"\betl\b|\bdata ingestion\b|\bdata pipelines?\b", re.IGNORECASE),
    "observability": re.compile(
        r"\bobservability\b|\bmetrics\b|\blogging\b|\btracing\b", re.IGNORECASE
    ),
    "testing": re.compile(
        r"\btesting\b|\bunit tests?\b|\bintegration tests?\b|\btestable design\b", re.IGNORECASE
    ),
    "documentation": re.compile(
        r"\bwell-documented\b|\bdocumentation\b|\bspecifications?\b|\bacceptance criteria\b",
        re.IGNORECASE,
    ),
}

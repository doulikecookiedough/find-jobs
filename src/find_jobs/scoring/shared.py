"""Shared helpers used by the scoring modules.

These functions support multiple scoring concerns without carrying scoring policy
of their own.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile


def candidate_known_technologies(profile: CandidateProfile) -> set[str]:
    """Return the broader technology set the candidate can plausibly claim.

    This is wider than the preferred stack so skills scoring can reward adjacent
    but credible experience.
    """
    return {
        *profile.primary_languages,
        *profile.secondary_languages,
        *profile.frameworks,
        *profile.cloud_platforms,
        *profile.databases,
        *profile.infrastructure_tools,
        *profile.developer_tools,
        *profile.preferred_technologies,
    }


def format_years(value: float) -> str:
    """Render years of experience without unnecessary decimal noise.

    Whole numbers stay compact while partial years remain explicit.
    """
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}"

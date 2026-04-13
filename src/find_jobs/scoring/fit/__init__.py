"""Public exports for fit scoring.

This package keeps the fit import path stable while splitting the underlying
rules into small, reviewable modules.
"""

from find_jobs.scoring.fit.competition import score_competition_realism
from find_jobs.scoring.fit.domain import score_domain_alignment
from find_jobs.scoring.fit.level import score_level_match
from find_jobs.scoring.fit.role import score_role_type_alignment
from find_jobs.scoring.fit.stack import score_stack_alignment
from find_jobs.scoring.fit.strength import score_strength_alignment

__all__ = [
    "score_competition_realism",
    "score_domain_alignment",
    "score_level_match",
    "score_role_type_alignment",
    "score_stack_alignment",
    "score_strength_alignment",
]

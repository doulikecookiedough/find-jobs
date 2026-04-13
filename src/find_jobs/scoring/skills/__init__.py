"""Public exports for skills scoring.

This package keeps the skills import path stable while splitting the underlying
rules into small, reviewable modules.
"""

from find_jobs.scoring.skills.engine import score_skills_alignment
from find_jobs.scoring.skills.stack import score_skills_stack_alignment

__all__ = [
    "score_skills_alignment",
    "score_skills_stack_alignment",
]

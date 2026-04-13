"""Public scoring exports.

This package keeps its import path stable while the implementation lives in
smaller modules that are easier to review independently.
"""

from find_jobs.scoring.engine import score_job
from find_jobs.scoring.fit import (
    score_competition_realism,
    score_domain_alignment,
    score_level_match,
    score_role_type_alignment,
    score_stack_alignment,
    score_strength_alignment,
)
from find_jobs.scoring.interview import score_interview_probability
from find_jobs.scoring.skills import score_skills_alignment, score_skills_stack_alignment

__all__ = [
    "score_competition_realism",
    "score_domain_alignment",
    "score_interview_probability",
    "score_job",
    "score_level_match",
    "score_role_type_alignment",
    "score_skills_alignment",
    "score_skills_stack_alignment",
    "score_stack_alignment",
    "score_strength_alignment",
]

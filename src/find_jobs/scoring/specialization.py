"""Specialization-proof helpers for domain-specific scoring penalties.

These helpers isolate niche domain checks so the generic scoring utilities stay
focused on reusable logic.
"""

from __future__ import annotations

from find_jobs.models import CandidateProfile, ParsedJob
from find_jobs.scoring.shared import candidate_known_technologies


INFERENCE_INFRASTRUCTURE_DOMAINS = {
    "gpu-computing",
    "model-serving",
    "edge-inference",
    "ml-infrastructure",
}
INFERENCE_INFRASTRUCTURE_TECHNOLOGIES = {
    "cuda",
    "tensorrt",
    "triton-inference-server",
}


def profile_has_inference_infrastructure_proof(profile: CandidateProfile) -> bool:
    """Return whether the profile explicitly supports inference and GPU infra work."""

    known_technologies = candidate_known_technologies(profile)
    if known_technologies.intersection(INFERENCE_INFRASTRUCTURE_TECHNOLOGIES):
        return True

    domain_signals = set(profile.preferred_domains).union(profile.avoid_domains)
    if domain_signals.intersection(INFERENCE_INFRASTRUCTURE_DOMAINS):
        return True

    return bool(
        set(profile.strengths).intersection(
            {"gpu-computing", "model-serving", "edge-inference", "ml-infrastructure"}
        )
    )


def job_requires_inference_infrastructure(job: ParsedJob) -> bool:
    """Return whether the parsed job signals specialized inference infrastructure work."""

    return bool(
        set(job.domain_signals).intersection(INFERENCE_INFRASTRUCTURE_DOMAINS)
        or set(job.technologies).intersection(INFERENCE_INFRASTRUCTURE_TECHNOLOGIES)
    )

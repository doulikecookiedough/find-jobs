"""CLI entrypoint for evaluating job descriptions."""

from __future__ import annotations

import argparse
from pathlib import Path

from find_jobs.comparison import evaluate_job_text
from find_jobs.profile import build_default_candidate_profile


def main(argv: list[str] | None = None) -> int:
    """Project CLI entrypoint."""
    parser = argparse.ArgumentParser(prog="find-jobs")
    subparsers = parser.add_subparsers(dest="command")

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("job_file")

    args = parser.parse_args(argv)

    if args.command != "evaluate":
        print("Usage: find-jobs evaluate <job-file>")
        return 1

    raw_text = Path(args.job_file).read_text()
    parsed_job, job_score = evaluate_job_text(raw_text, build_default_candidate_profile())

    print(f"Title: {parsed_job.title or 'Unknown'}")
    print(f"Company: {parsed_job.company or 'Unknown'}")
    print(f"Fit Score: {job_score.fit_score}")
    print(f"Recommendation: {job_score.recommendation}")
    print(f"Priority: {job_score.priority}")

    return 0

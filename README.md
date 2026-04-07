# find-jobs

`find-jobs` is an experimental Python project for evaluating job postings against a candidate profile and producing a simple match assessment.

The goal is to reduce job-search fatigue by turning raw job descriptions into something easier to review, compare, and eventually rank.

This repository is intentionally being built in small stages. The current focus is not completeness. The focus is a clean structure, strong tests, and a workflow that is easy to iterate on.

## Why this exists

The long-term idea is:

- ingest a full job description
- extract key signals
- compare those signals against a candidate profile
- produce a score, reasons, and risks
- eventually support batch evaluation and CSV export

Today, the project is in the parser-first phase. The parser is being hardened against real-world fixtures before scoring logic is introduced.

## Current approach

This project is being developed with a simple progression:

1. scaffold the package and test layout
2. build a parser for raw job descriptions
3. add a candidate profile model
4. compare profile data against parsed job signals
5. add scoring and recommendations

The initial implementation will be rule-based and deterministic. LLM-assisted evaluation may be added later, but it is not the starting point.

## Current state

The parser currently extracts:

- title
- company
- location
- years of experience
- salary range and currency when present
- seniority
- role type
- technologies
- domain signals
- work style signals

The parser is tested against multiple real-world fixture styles, including:

- direct pasted job descriptions
- enterprise platform/integrations postings
- Apple-style branded listings
- LinkedIn-wrapped postings with duplicated UI metadata

Current parser fixtures:

- `tests/fixtures/affirm_backend_engineer.txt`
- `tests/fixtures/integrations_engineer.txt`
- `tests/fixtures/apple_workflow_foundations.txt`
- `tests/fixtures/zepp_connected_partnerships.txt`
- `tests/fixtures/genista_backend_engineer.txt`
- `tests/fixtures/stripe_backend_engineer.txt`

## Project goals

- Parse raw job descriptions into structured data.
- Score job postings against a candidate profile using explicit rules.
- Produce a clear, CLI-friendly evaluation output.
- Keep the architecture modular, testable, and easy to evolve.

## Development principles

- clear domain models
- readable rule-based logic first
- tests as a first-class part of development
- incremental design instead of premature complexity
- simple local execution for reviewers and contributors

## Project structure

The Python package is organized by responsibility:

- `src/find_jobs/cli.py`: command-line entrypoint
- `src/find_jobs/parser.py`: job description parsing
- `src/find_jobs/profile.py`: candidate profile handling
- `src/find_jobs/comparison.py`: profile-to-job comparison logic
- `src/find_jobs/scoring.py`: scoring and recommendation logic
- `src/find_jobs/models.py`: shared domain models

Each module has a corresponding pytest file under `tests/`.

## Quick start

This project uses `uv` for environment and dependency management.

From the repository root:

```bash
uv sync
uv run pytest
uv run find-jobs
```

At the moment, the CLI is still a scaffold. The main implemented area is the parser plus its test fixtures.

## Reviewer notes

If you want to try the project locally:

- run `uv sync` to create the local environment
- run `uv run pytest` to execute the test suite
- inspect `src/find_jobs/parser.py` and `tests/test_parser.py` together
- review `tests/fixtures/` to see the types of postings currently used to shape the parser

This repository is intentionally experimental. Expect small, reviewable changes rather than a large initial implementation.

## Near-term scope

The first phase will focus on:

1. project structure
2. core models
3. rule-based parsing
4. scoring logic
5. a CLI entrypoint

## Status

Repository initialized. Python/uv scaffold added. Rule-based parser is implemented and fixture-driven tests are passing. Scoring and profile comparison are the next major steps.

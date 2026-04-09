# find-jobs

`find-jobs` is an experimental Python project for evaluating job postings against a candidate profile and producing an explainable fit assessment.

The goal is to reduce job-search fatigue by turning raw job descriptions into something easier to review, compare, and eventually rank.

This repository is intentionally being built in small stages. The focus is a clean structure, strong tests, and a workflow that is easy to iterate on.

## Why this exists

The long-term idea is to:

- ingest a full job description
- extract key signals
- compare those signals against a candidate profile
- produce a score, reasons, and risks
- eventually support batch evaluation, CSV export, and browser-assisted ingestion

The current MVP supports parsing and scoring from a text file, a local FastAPI endpoint, and a local Chrome extension that can evaluate visible job pages directly.

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

The scorer currently produces:

- fit score
- recommendation
- priority
- reasons
- risks
- score breakdown by factor
- missing-field diagnostics for incomplete parses

The API currently exposes:

- `GET /health`
- `POST /evaluate`
- `POST /evaluate-text`

The Chrome extension currently provides:

- a popup UI for evaluating the active browser tab
- visible text extraction from LinkedIn-style job pages
- a collapsed extracted-text preview for real-world parser debugging
- local API integration through `POST /evaluate-text`

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
- `tests/fixtures/berkeley_payments_senior_backend.txt`

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
uv run find-jobs evaluate tests/fixtures/affirm_backend_engineer.txt
```

To run the local API:

```bash
uv run uvicorn find_jobs.api:app --host 127.0.0.1 --port 8000 --reload
```

Then test it:

```bash
curl -s http://127.0.0.1:8000/health
```

To test the Chrome extension locally:

1. Start the local API with the `uvicorn` command above.
2. Open `chrome://extensions`.
3. Enable `Developer mode`.
4. Click `Load unpacked`.
5. Select the `extension/` directory in this repository.
6. Open a job posting page.
7. Click the `find-jobs` extension to open the side panel.
8. Click `Evaluate Job`.
9. Expand `Preview extracted text` if the score looks wrong.

For manual reviewer testing, the easiest option is FastAPI docs:

- open `http://127.0.0.1:8000/docs`
- use `POST /evaluate-text`
- click `Try it out`
- paste a full job description as plain text
- click `Execute`

You can also test the plain-text endpoint from the command line:

```bash
curl -s \
  -X POST http://127.0.0.1:8000/evaluate-text \
  -H "Content-Type: text/plain" \
  --data-binary @tests/fixtures/affirm_backend_engineer.txt
```

Example output:

```text
Title: Software Engineer II, Backend (Consumer Authentication)
Company: Affirm
Fit Score: 85
Recommendation: apply
Priority: high
Reasons:
- Role type aligns well with your target focus (backend).
- Job content matches several of your strongest backend and systems skills.
- Relevant stack overlap found: aws, kubernetes, python.
- Work style includes remote flexibility.
```

## Incomplete evaluation logging

When an evaluation is missing important parsed fields, the project writes a structured review record to:

- `logs/incomplete_evaluations.jsonl`

This file is intended to help improve the parser and scorer over time. Each line stores:

- parsed metadata
- missing fields
- parser warnings
- fit score and recommendation
- the raw job description text

The `logs/` directory is tracked so its location is obvious, but the log contents are git-ignored.

You can override the default path with:

```bash
FIND_JOBS_INCOMPLETE_LOG_PATH=/custom/path/incomplete.jsonl
```

## Scoring model

The current weighted score uses:

- level match
- stack alignment
- domain alignment
- strength alignment
- role type alignment
- competition realism

The implementation is still heuristic and intentionally transparent. The score is meant to support triage, not replace judgment.

## Reviewer notes

If you want to try the project locally:

- run `uv sync` to create the local environment
- run `uv run pytest` to execute the test suite
- run `uv run find-jobs evaluate tests/fixtures/affirm_backend_engineer.txt`
- run `uv run uvicorn find_jobs.api:app --host 127.0.0.1 --port 8000 --reload`
- call `GET /health`, `POST /evaluate`, or `POST /evaluate-text` against the local API
- open `http://127.0.0.1:8000/docs` for interactive API testing
- inspect `src/find_jobs/parser.py`, `src/find_jobs/scoring.py`, and the corresponding tests
- inspect `src/find_jobs/api.py` and `tests/test_api.py` for the local service boundary
- review `tests/fixtures/` to see the posting styles shaping the parser

This repository is intentionally experimental. Expect small, reviewable changes rather than a large initial implementation.

## Near-term scope

Near-term work is likely to focus on:

1. a persistent Chrome side panel for evaluating multiple LinkedIn jobs without reopening the popup
2. pasted text / stdin support
3. batch mode and CSV export
4. configurable candidate profiles
5. local API refinements for extension integration

## Status

Parser, profile, scoring, end-to-end comparison, CLI MVP, local FastAPI evaluation API, and Chrome extension MVP are implemented. The project is now in the “make ingestion faster for real job-search workflows” phase rather than the “can we score jobs at all?” phase.

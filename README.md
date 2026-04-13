# find-jobs

`find-jobs` is a local, rule-based tool for evaluating job postings against a candidate profile.

It is being developed iteratively for real job-search use, so the priority is fast reviewer onboarding, explainable scoring, and small, testable changes.

## Quick start

This project uses `uv`.

```bash
uv sync
uv run pytest
uv run find-jobs evaluate tests/fixtures/affirm_backend_engineer.txt
```

Run the local API:

```bash
uv run uvicorn find_jobs.api:app --host 127.0.0.1 --port 8000 --reload
```

Sanity-check it:

```bash
curl -s http://127.0.0.1:8000/health
```

Test the plain-text endpoint:

```bash
curl -s \
  -X POST http://127.0.0.1:8000/evaluate-text \
  -H "Content-Type: text/plain" \
  --data-binary @tests/fixtures/affirm_backend_engineer.txt
```

Use FastAPI docs for manual testing:

- open `http://127.0.0.1:8000/docs`
- use `POST /evaluate-text`
- paste a full job description

## What it does

Current inputs:

- raw job description text from files, API requests, or the Chrome extension

Current parser outputs:

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

Current scoring outputs:

- fit score
- skills alignment
- interview probability range
- recommendation
- priority
- reasons
- risks
- factor breakdown
- missing-field diagnostics for incomplete parses

Current surfaces:

- CLI
- local FastAPI API
- Chrome side panel extension

## Project structure

- `src/find_jobs/cli.py`: CLI entrypoint
- `src/find_jobs/api.py`: FastAPI wrapper
- `src/find_jobs/parser.py`: job text parsing
- `src/find_jobs/profile.py`: candidate profile defaults
- `src/find_jobs/comparison.py`: parse + score orchestration
- `src/find_jobs/scoring/engine.py`: final score assembly
- `src/find_jobs/scoring/fit/`: fit scoring helpers
- `src/find_jobs/scoring/skills/`: skills scoring helpers
- `src/find_jobs/scoring/interview.py`: interview probability scoring
- `src/find_jobs/scoring/shared.py`: shared scoring helpers
- `src/find_jobs/models.py`: shared models
- `tests/`: behavior contract
- `tests/fixtures/`: real-world parsing fixtures
- `extension/`: Chrome extension client

## Scoring notes

The scoring system is intentionally heuristic and explainable.

Fit currently uses:

- level match
- stack alignment
- domain alignment
- strength alignment
- role type alignment
- competition realism

Interview probability is calibrated against the active candidate profile, not just the job posting. Years-of-experience penalties are based on the gap between the parsed job requirement and the candidate profile.

## Review logs

The project writes review queues under `logs/`:

- `logs/incomplete_evaluations.jsonl`: evaluations with missing parsed fields or parser warnings
- `logs/high_interview_evaluations.jsonl`: evaluations whose interview upper bound clears the configured threshold

Overrides:

```bash
FIND_JOBS_INCOMPLETE_LOG_PATH=/custom/path/incomplete.jsonl
FIND_JOBS_HIGH_INTERVIEW_LOG_PATH=/custom/path/high-interview.jsonl
FIND_JOBS_HIGH_INTERVIEW_THRESHOLD=20
```

## Chrome extension

To test the extension locally:

1. Start the local API.
2. Open `chrome://extensions`.
3. Enable `Developer mode`.
4. Click `Load unpacked`.
5. Select the `extension/` directory.
6. Open a job posting.
7. Open the `find-jobs` side panel.
8. Click `Evaluate Job`.
9. Expand `Preview extracted text` if the result looks wrong.

## Example output

```text
Title: Software Engineer
Company: PathPilot
Fit Score: 84
Skills Alignment: 79
Interview Probability: 14-20%
Years Match: Strong match: requires about 3 years, profile is 3 years.
Recommendation: apply
Priority: high
Reasons:
- Role type aligns well with your target focus (backend).
- Job content matches several of your strongest backend and systems skills.
- Domain signals overlap well with your preferred backend and integration work.
- Relevant stack overlap found: aws, python, rest-apis.
```

## Status

This is an actively iterated local tool, not a finished platform. Expect small refactors, scoring calibration, and workflow changes as real job-review usage exposes gaps.

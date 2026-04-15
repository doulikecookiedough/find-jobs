# find-jobs

`find-jobs` is a local, rule-based tool for evaluating job postings against a candidate profile.

It is being developed iteratively for real job-search use, so the priority is fast reviewer onboarding, explainable scoring, and small, testable changes.

## Reviewer setup

This project uses `uv` for dependency management and command execution.

If `uv` is not installed:

- macOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Homebrew: `brew install uv`
- Windows: `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"`

After installation, restart your shell if `uv` is not yet on your `PATH`.

## Quick start

From the repository root:

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

## System design

The system is intentionally split into a thin browser client and a local scoring backend:

- the Chrome extension extracts visible job text and displays the result
- FastAPI is the scoring boundary
- the parser turns messy job text into structured fields
- the scoring engine compares those fields against the candidate profile
- logs feed calibration and regression testing

```mermaid
flowchart LR
    subgraph Browser
        A["Job posting page"]
        B["Chrome side panel extension"]
    end

    subgraph Backend
        C["FastAPI /evaluate-text"]
        D["Parser"]
        E["Scoring Engine"]
        F["Candidate Profile"]
    end

    subgraph Outputs
        G["UI response"]
        H["Incomplete evaluation log"]
        I["High-interview log"]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    F --> E
    E --> G
    D --> H
    E --> I
    G --> B
```

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

### Fit flow

`fit_score` is the application-priority score. It answers: "is this worth spending time on?"

```mermaid
flowchart TD
    A["Parsed job"] --> B["Level match"]
    A --> C["Stack alignment"]
    A --> D["Domain alignment"]
    A --> E["Strength alignment"]
    A --> F["Role type alignment"]
    A --> G["Competition realism"]
    H["Candidate profile"] --> B
    H --> C
    H --> D
    H --> E
    H --> F
    H --> G

    B --> I["Weighted fit score"]
    C --> I
    D --> I
    E --> I
    F --> I
    G --> I

    I --> J["Recommendation / priority / reasons / risks"]
```

### Skills flow

`skills_alignment` is narrower than fit. It answers: "how much of the actual technical work overlaps with the profile?"

```mermaid
flowchart TD
    A["Parsed technologies"] --> D["Stack overlap"]
    B["Parsed domain signals"] --> E["Domain overlap"]
    C["Parsed role content"] --> F["Strength overlap"]

    G["Candidate profile"] --> D
    G --> E
    G --> F

    D --> H["Skills alignment score"]
    E --> H
    F --> H
```

### Interview flow

`interview_probability` is the cold-application likelihood estimate. It is deliberately more conservative than fit or skills.

```mermaid
flowchart TD
    A["Fit score"] --> E["Base interview likelihood"]
    B["Skills alignment"] --> E
    C["Level / years match"] --> E
    D["Competition realism"] --> E

    E --> F["Penalty pass"]
    F --> F1["Missing years"]
    F --> F2["Senior stretch"]
    F --> F3["Role mismatch"]
    F --> F4["Stack mismatch"]
    F --> F5["Avoid-role / avoid-domain signals"]

    F1 --> G["Interview probability range"]
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G
```

## Review logs

The project writes review queues under `logs/`:

- `logs/complete_evaluations.jsonl`: every completed evaluation
- `logs/incomplete_evaluations.jsonl`: evaluations with missing parsed fields or parser warnings
- `logs/high_interview_evaluations.jsonl`: evaluations whose interview upper bound clears the configured threshold

Overrides:

```bash
FIND_JOBS_COMPLETE_LOG_PATH=/custom/path/complete.jsonl
FIND_JOBS_INCOMPLETE_LOG_PATH=/custom/path/incomplete.jsonl
FIND_JOBS_HIGH_INTERVIEW_LOG_PATH=/custom/path/high-interview.jsonl
FIND_JOBS_HIGH_INTERVIEW_THRESHOLD=20
```

## Chrome extension

To test the extension locally:

1. Install `uv` if needed, then run `uv sync`.
2. Start the local API.
3. Open `chrome://extensions`.
4. Enable `Developer mode`.
5. Click `Load unpacked`.
6. Select the `extension/` directory.
7. Open a job posting.
8. Open the `find-jobs` side panel.
9. Click `Evaluate Job`.
10. Expand `Preview extracted text` if the result looks wrong.

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

# AGENT.md

This file gives coding agents the minimum context needed to work effectively in this repository without wasting tokens.

## Purpose

`find-jobs` is a small, deterministic job-evaluation project.

The core rule for agents working here:

- prefer narrow, local changes over broad redesign
- preserve explainability and testability
- minimize context gathering before acting

If a task can be completed by reading 1-3 files and running 1-3 targeted tests, do that instead of scanning the whole repository.

## Project Shape

Main Python modules:

- `src/find_jobs/parser.py`: extract structured job signals from raw job text
- `src/find_jobs/profile.py`: candidate profile defaults and profile helpers
- `src/find_jobs/comparison.py`: compare parsed jobs against the candidate profile
- `src/find_jobs/scoring/engine.py`: orchestrate final scoring outputs
- `src/find_jobs/scoring/fit/`: fit scoring helpers split by concern
- `src/find_jobs/scoring/skills/`: skills scoring helpers split by concern
- `src/find_jobs/scoring/interview.py`: interview probability scoring
- `src/find_jobs/scoring/shared.py`: shared scoring helpers
- `src/find_jobs/models.py`: shared domain models
- `src/find_jobs/api.py`: FastAPI wrapper around evaluation
- `src/find_jobs/cli.py`: CLI entrypoint
- `src/find_jobs/evaluation_log.py`: incomplete-evaluation logging

Supporting surfaces:

- `tests/`: primary source of expected behavior
- `tests/fixtures/`: real-world job text fixtures used to shape parser behavior
- `extension/`: Chrome extension UI for local evaluation via the API

## Working Norms

- Keep the system rule-based and transparent unless the user explicitly asks for LLM-assisted behavior.
- Treat tests as the contract. Update or add the smallest test that proves the behavior change.
- Avoid speculative abstractions. This repo is intentionally small.
- Prefer one scoped task at a time: finish it, review it, and commit it before starting the next change.
- Do not let unrelated uncommitted changes accumulate across parser, scoring, extension, and docs at the same time.
- Do not move responsibilities across modules without a clear reason.
- Preserve the current boundary: parsing, comparison, scoring, and presentation should stay separable.
- Keep public import paths stable when refactoring internals unless the user explicitly wants a contract change.
- Prefer concise 1-2 sentence docstrings for public scoring helpers and focused tests when behavior needs quick reviewer context.
- When a scoring refactor is requested, prefer incremental commits that separate structure, tests, and docs.

## Token Discipline

When working in this repository:

- Read the README once for orientation, then prefer direct file reads.
- Start with `rg` to locate symbols or tests instead of opening large files blindly.
- Read only the files on the execution path of the requested change.
- Prefer targeted test runs over the full suite while iterating.
- Do not paste large fixture contents into the conversation unless the user explicitly asks.
- Do not summarize files the user did not ask about unless the summary affects the decision.
- Keep plans short and concrete; avoid long speculative option lists.

Good default sequence:

1. Identify the touched module.
2. Read the corresponding test file.
3. Read the implementation file.
4. Make the smallest viable change.
5. Run the narrowest relevant test.
6. Show or summarize the focused diff for review when requested.
7. Commit that scoped change before starting another task.
8. Broaden validation only if needed.

## Change Heuristics

### Parser changes

- Start in `tests/test_parser.py` and the smallest relevant fixture.
- Prefer adding or tightening extraction rules instead of rewriting parser flow.
- Avoid introducing heuristics that are overly tailored to one fixture if they may damage other fixture families.
- If parsing becomes uncertain, add or preserve parser warnings rather than silently guessing.

### Scoring or recommendation changes

- Inspect `tests/test_scoring.py`, `tests/test_comparison.py`, and the scoring/comparison modules together.
- Keep scoring explainable. A future reader should be able to explain why a job got its score.
- Preserve reason and risk output quality; these are product behavior, not debug noise.
- Treat `src/find_jobs/scoring/engine.py` as the stable orchestration entrypoint and keep lower-level scoring rules in the dedicated `fit`, `skills`, or `interview` modules.
- If a scoring module starts to feel crowded, split by concern inside the scoring package rather than rebuilding the scoring flow wholesale.

### API or CLI changes

- Keep `api.py` and `cli.py` thin wrappers over domain logic.
- Do not duplicate scoring or parsing logic in transport layers.
- Prefer response-shape stability unless the user explicitly wants a contract change.

### Extension changes

- The extension is a client only. The backend is the source of truth.
- Avoid moving evaluation logic into browser code.
- Preserve the local endpoint contract unless the backend change is intentional and tested.

## Test Strategy

Use the narrowest command that validates the change:

```bash
uv run pytest tests/test_parser.py
uv run pytest tests/test_scoring.py
uv run pytest tests/test_api.py
```

Use the full suite when:

- shared models changed
- multiple layers changed
- a targeted failure suggests cross-module regressions

## What To Avoid

- sweeping refactors without a failing test or explicit user request
- reformatting unrelated files
- changing fixture text unless the user explicitly wants fixture updates
- broad dependency additions for simple rule-based tasks
- turning a deterministic rule into an opaque heuristic without strong justification

## Definition of Done

A task is usually complete when:

- the requested behavior is implemented
- the relevant tests pass
- the diff is limited to the necessary files
- the final explanation references outcomes, not internal chain-of-thought

## If Context Is Missing

If the request is ambiguous, prefer these sources in order:

1. existing tests
2. adjacent implementation
3. README
4. ask the user a narrow question only if the ambiguity would change the design materially

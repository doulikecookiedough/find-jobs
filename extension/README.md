# Chrome Extension MVP

This extension is the browser-facing client for the local `find-jobs` FastAPI service.

## Local Setup

From the project root, start the API:

```bash
uv run uvicorn find_jobs.api:app --host 127.0.0.1 --port 8000 --reload
```

Then load the extension:

1. Open `chrome://extensions`.
2. Enable `Developer mode`.
3. Click `Load unpacked`.
4. Select the `extension/` directory in this repository.
5. Open a job posting page.
6. Click the `find-jobs` extension.
7. Click `Evaluate Job`.

## MVP Contract

The extension:

- reads visible text from the active tab
- sends that text to `POST http://127.0.0.1:8000/evaluate-text`
- renders the score, recommendation, reasons, risks, and parser warnings

The extension does not own scoring logic. It is only responsible for page extraction and display. The Python backend remains the source of truth for parsing and scoring.

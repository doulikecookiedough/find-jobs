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
6. Click the `find-jobs` extension to open the side panel.
7. Click `Evaluate Job`.
8. Expand `Preview extracted text` if the score looks wrong or the parser misses important fields.

## MVP Contract

The extension:

- reads visible text from the active tab
- sends that text to `POST http://127.0.0.1:8000/evaluate-text`
- renders the score, recommendation, reasons, risks, and parser warnings

The extension does not own scoring logic. It is only responsible for page extraction and display. The Python backend remains the source of truth for parsing and scoring.

## Popup Limitation

Chrome extension popups are temporary. The popup closes when focus returns to the browser page, which means it has to be reopened when clicking through multiple LinkedIn job postings.

This is expected Chrome behavior, not a bug in the extension.

## Side Panel

The extension now uses a Chrome side panel as the primary UI. It keeps the same core workflow as the popup, but it remains open beside the page while reviewing multiple jobs.

The expected testing process is:

1. Start the local FastAPI service.
2. Reload the unpacked extension in `chrome://extensions`.
3. Open LinkedIn jobs.
4. Click the `find-jobs` extension to open the side panel once.
5. Click through job postings in LinkedIn.
6. Click `Evaluate Job` in the side panel for each posting.
7. Use `Preview extracted text` to verify what was sent to the parser.

The side panel should still call the same local API endpoint:

```text
POST http://127.0.0.1:8000/evaluate-text
```

Keeping the backend endpoint unchanged makes the side panel a UI improvement rather than a scoring-system rewrite.

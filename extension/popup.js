const API_URL = "http://127.0.0.1:8000/evaluate-text";

const evaluateButton = document.querySelector("#evaluate-button");
const statusElement = document.querySelector("#status");
const resultElement = document.querySelector("#result");
const extractedPreviewElement = document.querySelector("#extracted-preview");
const extractedTextElement = document.querySelector("#extracted-text");

evaluateButton.addEventListener("click", async () => {
  setLoading(true);
  resultElement.hidden = true;
  resultElement.replaceChildren();
  resetExtractedPreview();

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) {
      throw new Error("Could not find the active browser tab.");
    }

    const injectionResults = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractVisibleJobText,
    });
    const result = injectionResults?.[0]?.result;

    if (result?.error) {
      throw new Error(result.error);
    }

    if (!result?.jobText?.trim()) {
      throw new Error(`Could not extract readable job text from this page. Source: ${result?.source ?? "unknown"}.`);
    }

    renderExtractedPreview(result.jobText);
    const evaluation = await evaluateJobText(result.jobText);
    renderEvaluation(evaluation);
    statusElement.textContent = `Evaluation complete. Extracted ${result.characterCount} characters from ${result.source}.`;
  } catch (error) {
    statusElement.textContent = error.message;
  } finally {
    setLoading(false);
  }
});

function extractVisibleJobText() {
  function textFromSelector(selector) {
    const element = document.querySelector(selector);
    return (element?.innerText || element?.textContent || "").trim();
  }

  function normalizeWhitespace(text) {
    return text
      .replace(/\u00a0/g, " ")
      .replace(/[ \t]+\n/g, "\n")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  const root = document.querySelector("main") ?? document.body ?? document.documentElement;
  if (!root) {
    return { jobText: "", source: "no document body", characterCount: 0 };
  }

  const title = textFromSelector("h1") || document.title || "";
  const company = textFromSelector(".job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name");
  const location = textFromSelector(".job-details-jobs-unified-top-card__primary-description-container, .jobs-unified-top-card__bullet");
  const description = textFromSelector(
    ".jobs-description__content, .jobs-box__html-content, .jobs-description-content__text, .jobs-description, [class*='jobs-description']",
  );
  const fallbackText = root.innerText || root.textContent || "";
  const source = description ? "LinkedIn job description selectors" : "main/body fallback text";
  const jobText = normalizeWhitespace([title, company, location, description || fallbackText]
    .filter(Boolean)
    .join("\n\n")
    .trim());

  return {
    jobText,
    source,
    characterCount: jobText.length,
  };
}

function resetExtractedPreview() {
  extractedPreviewElement.hidden = true;
  extractedPreviewElement.open = false;
  extractedTextElement.textContent = "";
}

function renderExtractedPreview(jobText) {
  const previewLength = 1200;
  const previewText = jobText.length > previewLength
    ? `${jobText.slice(0, previewLength)}\n\n[Preview truncated at ${previewLength} characters]`
    : jobText;

  extractedPreviewElement.hidden = false;
  extractedTextElement.textContent = previewText;
}

async function evaluateJobText(jobText) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "text/plain" },
    body: jobText,
  });

  if (!response.ok) {
    throw new Error(`Evaluation failed with status ${response.status}. Is the local API running?`);
  }

  return response.json();
}

function renderEvaluation(evaluation) {
  resultElement.hidden = false;
  resultElement.append(
    scoreBlock(evaluation),
    listBlock("Reasons", evaluation.reasons),
    listBlock("Risks", evaluation.risks),
    listBlock("Parser Warnings", evaluation.parser_warnings),
  );
}

function scoreBlock(evaluation) {
  const container = document.createElement("section");
  const score = document.createElement("div");
  const scoreValue = document.createElement("strong");
  const scoreLabel = document.createElement("span");
  const meta = document.createElement("p");

  score.className = "score";
  scoreValue.textContent = evaluation.fit_score;
  scoreLabel.textContent = `${evaluation.recommendation} / ${evaluation.priority}`;
  meta.className = "meta";
  meta.textContent = `${evaluation.company ?? "Unknown company"} | ${evaluation.title ?? "Unknown title"}`;

  score.append(scoreValue, scoreLabel);
  container.append(score, meta);
  return container;
}

function listBlock(title, items) {
  const section = document.createElement("section");
  const heading = document.createElement("h2");
  const list = document.createElement("ul");

  heading.textContent = title;
  section.append(heading);

  for (const item of items ?? []) {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    list.append(listItem);
  }

  if (!list.children.length) {
    const listItem = document.createElement("li");
    listItem.textContent = "None";
    list.append(listItem);
  }

  section.append(list);
  return section;
}

function setLoading(isLoading) {
  evaluateButton.disabled = isLoading;
  evaluateButton.textContent = isLoading ? "Evaluating..." : "Evaluate Job";
  if (isLoading) {
    statusElement.textContent = "Reading this page and calling the local API...";
  }
}

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
    listBlock("Screening Risks", evaluation.risks),
    listBlock("Parser Warnings", evaluation.parser_warnings),
  );
}

function scoreBlock(evaluation) {
  const container = document.createElement("section");
  const score = document.createElement("div");
  const scoreValue = document.createElement("strong");
  const scoreLabel = document.createElement("span");
  const meta = document.createElement("p");
  const metrics = document.createElement("div");
  const scoreHeader = document.createElement("div");

  score.className = "score";
  scoreHeader.className = "score-header";
  scoreValue.textContent = evaluation.fit_score;
  scoreLabel.textContent = `${evaluation.recommendation} / ${evaluation.priority}`;
  meta.className = "meta";
  meta.textContent = `${evaluation.company ?? "Unknown company"} | ${evaluation.title ?? "Unknown title"}`;
  metrics.className = "metrics";

  scoreHeader.append(
    document.createTextNode("Fit"),
    infoBadge("Overall application-priority score. This blends level match, stack overlap, domain fit, role fit, and competition realism."),
  );
  metrics.append(
    metricCard(
      "Skills",
      `${evaluation.skills_alignment}%`,
      "Technical overlap score. This focuses on known stack, strengths, and domain signals rather than level realism.",
    ),
    metricCard(
      "Interview",
      `${evaluation.interview_probability_min}-${evaluation.interview_probability_max}%`,
      "Cold-application interview likelihood estimate, not your odds of passing once you are already in the interview loop.",
    ),
  );

  score.append(scoreHeader, scoreValue, scoreLabel);
  container.append(score, meta, metrics);
  return container;
}

function metricCard(label, value, tooltip) {
  const card = document.createElement("div");
  const heading = document.createElement("div");
  const headingLabel = document.createElement("span");
  const metricValue = document.createElement("strong");

  card.className = "metric-card";
  heading.className = "metric-heading";
  headingLabel.textContent = label;
  metricValue.textContent = value;
  heading.append(headingLabel, infoBadge(tooltip));
  card.append(heading, metricValue);
  return card;
}

function infoBadge(text) {
  const wrapper = document.createElement("span");
  const badge = document.createElement("button");
  const tooltip = document.createElement("span");

  wrapper.className = "tooltip";
  badge.type = "button";
  badge.className = "info-badge";
  badge.textContent = "i";
  badge.setAttribute("aria-label", text);
  tooltip.className = "tooltip-panel";
  tooltip.textContent = text;

  wrapper.append(badge, tooltip);
  return wrapper;
}

function listBlock(title, items) {
  const section = document.createElement("section");
  const headingRow = document.createElement("div");
  const heading = document.createElement("h2");
  const list = document.createElement("ul");

  heading.textContent = title;
  headingRow.className = "section-heading";
  headingRow.append(heading);

  if (title === "Screening Risks") {
    headingRow.append(
      infoBadge("Specific reasons a hiring team may screen you out early, such as direct stack mismatch, seniority mismatch, or avoid-role signals."),
    );
  }

  section.append(headingRow);

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

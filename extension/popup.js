const API_URL = "http://127.0.0.1:8000/evaluate-text";

const evaluateButton = document.querySelector("#evaluate-button");
const statusElement = document.querySelector("#status");
const resultElement = document.querySelector("#result");

evaluateButton.addEventListener("click", async () => {
  setLoading(true);
  resultElement.hidden = true;
  resultElement.replaceChildren();

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab?.id) {
      throw new Error("Could not find the active browser tab.");
    }

    const [{ result }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: extractVisibleJobText,
    });

    if (!result?.jobText?.trim()) {
      throw new Error("Could not extract readable job text from this page.");
    }

    const evaluation = await evaluateJobText(result.jobText);
    renderEvaluation(evaluation);
    statusElement.textContent = "Evaluation complete.";
  } catch (error) {
    statusElement.textContent = error.message;
  } finally {
    setLoading(false);
  }
});

function extractVisibleJobText() {
  const title = document.querySelector("h1")?.innerText ?? document.title;
  const bodyText = document.body?.innerText ?? "";
  const jobText = [title, bodyText].filter(Boolean).join("\n\n");
  return { jobText };
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

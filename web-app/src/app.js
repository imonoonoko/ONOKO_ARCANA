(() => {
const { CARD_BACK, cards, spreads } = window.OnokoArcanaData;

const historyKey = "onoko-arcana:desktop:history:v1";
const learningKey = "onoko-arcana:desktop:learning:v1";
const settingsKey = "onoko-arcana:desktop:settings:v1";
const appVersion = "v0.1.3";
const latestReleaseUrl = "https://github.com/imonoonoko/ONOKO_ARCANA/releases/latest";
const projectRepositoryUrl = "https://github.com/imonoonoko/ONOKO_ARCANA";
const securityPolicyUrl = "https://github.com/imonoonoko/ONOKO_ARCANA/security/policy";
const assetLicenseUrl = "https://github.com/imonoonoko/ONOKO_ARCANA/blob/main/docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md";
const maxHistoryItems = 48;
const maxLearningAttempts = 128;
const learningPromptTypes = ["keyword_recall", "slot_interpretation"];
const cardIndex = new Map(cards.map((card, index) => [card.id, { card, index }]));
const spreadIndex = new Map(spreads.map((spread) => [spread.id, spread]));
let historyReadFailed = false;
let learningReadFailed = false;

function getCard(cardId) {
  return cardIndex.get(cardId)?.card || null;
}

function getCardIndex(cardId) {
  return cardIndex.get(cardId)?.index ?? -1;
}

function getSpread(spreadId) {
  return spreadIndex.get(spreadId) || null;
}

function blankSlotDrill(status = "") {
  return {
    key: null,
    cardId: null,
    slotKey: null,
    orientation: "upright",
    answer: "",
    revealed: false,
    savedConfidence: null,
    status
  };
}

const state = {
  spreadId: "one_card",
  drawn: [],
  revealedCount: 0,
  selectedIndex: -1,
  notes: {},
  restoredAt: null,
  reviewedHistoryKey: null,
  afterSaveKey: null,
  historyCardFilter: null,
  inspectorTab: "history",
  studySheetOpen: false,
  studySheetCardId: null,
  settingsOpen: false,
  settingsStatus: "",
  settings: {
    compactLearningPanel: false
  },
  recallPractice: {
    cardId: null,
    orientation: "upright",
    answer: "",
    revealed: false,
    savedConfidence: null,
    status: ""
  },
  slotDrill: blankSlotDrill()
};

const els = {
  questionInput: document.getElementById("questionInput"),
  spreadControls: document.getElementById("spreadControls"),
  spreadTitle: document.getElementById("spreadTitle"),
  spreadDescription: document.getElementById("spreadDescription"),
  spreadBoard: document.getElementById("spreadBoard"),
  drawButton: document.getElementById("drawButton"),
  revealButton: document.getElementById("revealButton"),
  saveReadingButton: document.getElementById("saveReadingButton"),
  resetButton: document.getElementById("resetButton"),
  progressTrack: document.getElementById("progressTrack"),
  statusLine: document.getElementById("statusLine"),
  selectedCard: document.getElementById("selectedCard"),
  noteInput: document.getElementById("noteInput"),
  noteStatus: document.getElementById("noteStatus"),
  cardStudySheetPanel: document.getElementById("cardStudySheetPanel"),
  toggleStudySheetButton: document.getElementById("toggleStudySheetButton"),
  studySheetPanel: document.getElementById("studySheetPanel"),
  inspectorTabs: Array.from(document.querySelectorAll("[data-inspector-tab]")),
  inspectorPanels: Array.from(document.querySelectorAll("[data-inspector-panel]")),
  studyPanel: document.getElementById("studyTabPanel"),
  historyList: document.getElementById("historyList"),
  historyReview: document.getElementById("historyReview"),
  studyLens: document.getElementById("studyLens"),
  historyFilterBar: document.getElementById("historyFilterBar"),
  historySection: document.querySelector(".history-section"),
  openSettingsButton: document.getElementById("openSettingsButton"),
  settingsDialog: document.getElementById("settingsDialog"),
  closeSettingsButton: document.getElementById("closeSettingsButton"),
  settingsStatus: document.getElementById("settingsStatus"),
  settingsHistoryCount: document.getElementById("settingsHistoryCount"),
  settingsHistoryUpdated: document.getElementById("settingsHistoryUpdated"),
  settingsLearningCount: document.getElementById("settingsLearningCount"),
  settingsLearningUpdated: document.getElementById("settingsLearningUpdated"),
  settingsImportHistoryButton: document.getElementById("settingsImportHistoryButton"),
  settingsExportHistoryButton: document.getElementById("settingsExportHistoryButton"),
  settingsClearHistoryButton: document.getElementById("settingsClearHistoryButton"),
  importLearningButton: document.getElementById("importLearningButton"),
  importLearningInput: document.getElementById("importLearningInput"),
  exportLearningButton: document.getElementById("exportLearningButton"),
  clearLearningButton: document.getElementById("clearLearningButton"),
  compactLearningToggle: document.getElementById("compactLearningToggle"),
  settingsAppVersion: document.getElementById("settingsAppVersion"),
  settingsReleaseWarning: document.getElementById("settingsReleaseWarning"),
  settingsBackupCue: document.getElementById("settingsBackupCue"),
  settingsLatestReleaseLink: document.getElementById("settingsLatestReleaseLink"),
  settingsProjectLink: document.getElementById("settingsProjectLink"),
  settingsSecurityLink: document.getElementById("settingsSecurityLink"),
  settingsLicenseLink: document.getElementById("settingsLicenseLink"),
  settingsLicenseCue: document.getElementById("settingsLicenseCue"),
  settingsLocalKeys: document.getElementById("settingsLocalKeys"),
  importHistoryButton: document.getElementById("importHistoryButton"),
  importHistoryInput: document.getElementById("importHistoryInput"),
  exportHistoryButton: document.getElementById("exportHistoryButton"),
  clearHistoryButton: document.getElementById("clearHistoryButton"),
  statCards: document.getElementById("statCards"),
  statRevealed: document.getElementById("statRevealed"),
  statSaved: document.getElementById("statSaved")
};

const inspectorTabIds = ["card", "study", "history"];

function validInspectorTab(tabId) {
  return inspectorTabIds.includes(tabId);
}

function renderInspectorTabs() {
  const activeTab = validInspectorTab(state.inspectorTab) ? state.inspectorTab : "card";
  state.inspectorTab = activeTab;
  els.inspectorTabs.forEach((button) => {
    const selected = button.dataset.inspectorTab === activeTab;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-selected", selected ? "true" : "false");
    button.tabIndex = selected ? 0 : -1;
  });
  els.inspectorPanels.forEach((panel) => {
    const selected = panel.dataset.inspectorPanel === activeTab;
    panel.classList.toggle("is-active", selected);
    panel.hidden = !selected;
  });
}

function setInspectorTab(tabId, options = {}) {
  if (!validInspectorTab(tabId)) return;
  state.inspectorTab = tabId;
  renderInspectorTabs();
  if (options.focus) {
    const button = els.inspectorTabs.find((candidate) => candidate.dataset.inspectorTab === tabId);
    button?.focus();
  }
}

function moveInspectorTab(currentTab, offset) {
  const index = inspectorTabIds.indexOf(currentTab);
  if (index < 0) return;
  const next = inspectorTabIds[(index + offset + inspectorTabIds.length) % inspectorTabIds.length];
  setInspectorTab(next, { focus: true });
}

function currentSpread() {
  return getSpread(state.spreadId) || spreads[0];
}

function readHistory() {
  try {
    const raw = localStorage.getItem(historyKey);
    if (!raw) {
      historyReadFailed = false;
      return [];
    }
    const history = JSON.parse(raw);
    historyReadFailed = !Array.isArray(history);
    return Array.isArray(history) ? history : [];
  } catch {
    historyReadFailed = true;
    return [];
  }
}

function writeHistory(history) {
  try {
    localStorage.setItem(historyKey, JSON.stringify(history.slice(0, maxHistoryItems)));
    historyReadFailed = false;
    return true;
  } catch {
    return false;
  }
}

function blankLearningState() {
  return {
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    attempts: []
  };
}

function validLearningAttempt(attempt) {
  return Boolean(
    attempt &&
    typeof attempt === "object" &&
    typeof attempt.attemptedAt === "string" &&
    typeof attempt.cardId === "string" &&
    getCard(attempt.cardId) &&
    (attempt.orientation === "upright" || attempt.orientation === "reversed") &&
    learningPromptTypes.includes(attempt.promptType) &&
    typeof attempt.answer === "string" &&
    ["hard", "ok", "easy"].includes(attempt.confidence) &&
    (!("slotKey" in attempt) || typeof attempt.slotKey === "string") &&
    (!("slotLabel" in attempt) || typeof attempt.slotLabel === "string") &&
    (!("slotPrompt" in attempt) || typeof attempt.slotPrompt === "string") &&
    (!("spreadId" in attempt) || typeof attempt.spreadId === "string") &&
    (!("spreadLabel" in attempt) || typeof attempt.spreadLabel === "string")
  );
}

function readLearningState() {
  try {
    const raw = localStorage.getItem(learningKey);
    if (!raw) {
      learningReadFailed = false;
      return blankLearningState();
    }
    const payload = JSON.parse(raw);
    if (!payload || typeof payload !== "object" || !Array.isArray(payload.attempts)) {
      learningReadFailed = true;
      return blankLearningState();
    }
    const attempts = payload.attempts.filter(validLearningAttempt).slice(0, maxLearningAttempts);
    learningReadFailed = payload.attempts.length !== attempts.length;
    return {
      app: "ONOKO_ARCANA",
      schemaVersion: 1,
      attempts
    };
  } catch {
    learningReadFailed = true;
    return blankLearningState();
  }
}

function writeLearningState(learningState) {
  try {
    localStorage.setItem(learningKey, JSON.stringify({
      app: "ONOKO_ARCANA",
      schemaVersion: 1,
      attempts: learningState.attempts.slice(0, maxLearningAttempts)
    }));
    learningReadFailed = false;
    return true;
  } catch {
    return false;
  }
}

function blankSettings() {
  return {
    compactLearningPanel: false
  };
}

function readSettings() {
  try {
    const raw = localStorage.getItem(settingsKey);
    if (!raw) return blankSettings();
    const payload = JSON.parse(raw);
    if (!payload || typeof payload !== "object") return blankSettings();
    return {
      compactLearningPanel: payload.compactLearningPanel === true
    };
  } catch {
    return blankSettings();
  }
}

function writeSettings(settings) {
  try {
    localStorage.setItem(settingsKey, JSON.stringify({
      app: "ONOKO_ARCANA",
      schemaVersion: 1,
      compactLearningPanel: settings.compactLearningPanel === true
    }));
    return true;
  } catch {
    return false;
  }
}

function applySettings() {
  document.body.classList.toggle("is-compact-learning", state.settings.compactLearningPanel === true);
  if (els.compactLearningToggle) {
    els.compactLearningToggle.checked = state.settings.compactLearningPanel === true;
  }
}

function learningAttemptIdentity(attempt) {
  return [
    attempt.attemptedAt || "",
    attempt.cardId || "",
    attempt.orientation || "",
    attempt.promptType || "",
    attempt.spreadId || "",
    attempt.slotKey || "",
    attempt.answer || "",
    attempt.confidence || ""
  ].join("||");
}

function importedLearningFromPayload(payload) {
  if (!payload || typeof payload !== "object") {
    throw new Error("学習JSONの形式が違います。");
  }
  if ("app" in payload && payload.app !== "ONOKO_ARCANA") {
    throw new Error("ONOKO ARCANA用の学習ファイルではありません。");
  }
  const source = Array.isArray(payload.attempts)
    ? payload
    : payload.learning;
  if (!source || typeof source !== "object" || !Array.isArray(source.attempts)) {
    throw new Error("学習データが見つかりません。");
  }
  const valid = [];
  source.attempts.forEach((attempt) => {
    if (!validLearningAttempt(attempt)) return;
    const card = getCard(attempt.cardId);
    const normalized = {
      attemptedAt: attempt.attemptedAt,
      cardId: attempt.cardId,
      cardLabel: typeof attempt.cardLabel === "string" && attempt.cardLabel.trim()
        ? attempt.cardLabel
        : cardLabel(card),
      orientation: attempt.orientation,
      promptType: attempt.promptType || "keyword_recall",
      answer: attempt.answer,
      confidence: attempt.confidence
    };
    ["spreadId", "spreadLabel", "slotKey", "slotLabel", "slotPrompt"].forEach((field) => {
      if (typeof attempt[field] === "string") normalized[field] = attempt[field];
    });
    valid.push(normalized);
  });
  return {
    attempts: valid,
    skippedInvalid: source.attempts.length - valid.length
  };
}

function mergeImportedLearning(imported) {
  const current = readLearningState();
  const seen = new Set(current.attempts.map(learningAttemptIdentity));
  const additions = [];

  imported.attempts.forEach((attempt) => {
    const key = learningAttemptIdentity(attempt);
    if (seen.has(key)) return;
    seen.add(key);
    additions.push(attempt);
  });

  const nextState = {
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    attempts: [...additions, ...current.attempts].slice(0, maxLearningAttempts)
  };
  const storageFailed = additions.length ? !writeLearningState(nextState) : false;

  return {
    added: additions.length,
    skippedInvalid: imported.skippedInvalid,
    skippedDuplicate: imported.attempts.length - additions.length,
    storageFailed,
    total: readLearningState().attempts.length
  };
}

function readingIdentity(item) {
  const cards = Array.isArray(item.cards)
    ? item.cards.map((card) => [
      card.cardId,
      card.slotKey,
      card.reversed ? "R" : "U",
      card.note || ""
    ].join(":")).join("|")
    : "";
  return [
    item.savedAt || "",
    item.spreadId || "",
    item.question || "",
    item.summary || "",
    cards
  ].join("||");
}

function validImportedReading(item) {
  if (!item || typeof item !== "object") return false;
  if (typeof item.savedAt !== "string" || !item.savedAt.trim()) return false;
  if (typeof item.spreadLabel !== "string" || !item.spreadLabel.trim()) return false;
  if (typeof item.summary !== "string" || !item.summary.trim()) return false;
  const spread = getSpread(item.spreadId);
  if (!spread) return false;
  if (!Array.isArray(item.cards) || item.cards.length === 0 || item.cards.length > spread.slots.length) return false;
  return item.cards.every((entry) => (
    entry &&
    typeof entry === "object" &&
    typeof entry.cardId === "string" &&
    getCard(entry.cardId) &&
    typeof entry.reversed === "boolean" &&
    typeof entry.slotKey === "string" &&
    spread.slots.some((slot) => slot.key === entry.slotKey) &&
    (!("note" in entry) || typeof entry.note === "string")
  ));
}

function importedHistoryFromPayload(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload || typeof payload !== "object") {
    throw new Error("履歴JSONの形式が違います。");
  }
  if ("app" in payload && payload.app !== "ONOKO_ARCANA") {
    throw new Error("ONOKO ARCANA用の履歴ファイルではありません。");
  }
  if ("schemaVersion" in payload && payload.schemaVersion !== 1) {
    throw new Error("対応していない履歴形式です。");
  }
  if (!Array.isArray(payload.history)) {
    throw new Error("履歴データが見つかりません。");
  }
  return payload.history;
}

function mergeImportedHistory(imported) {
  const current = readHistory();
  const seen = new Set(current.map(readingIdentity));
  const valid = imported.filter(validImportedReading);
  const additions = [];

  valid.forEach((item) => {
    const key = readingIdentity(item);
    if (seen.has(key)) return;
    seen.add(key);
    additions.push(item);
  });

  const storageFailed = additions.length ? !writeHistory([...additions, ...current]) : false;

  return {
    added: additions.length,
    skippedInvalid: imported.length - valid.length,
    skippedDuplicate: valid.length - additions.length,
    storageFailed,
    total: readHistory().length
  };
}

function shuffleDeck() {
  const pool = [...cards];
  for (let index = pool.length - 1; index > 0; index -= 1) {
    const swap = Math.floor(Math.random() * (index + 1));
    [pool[index], pool[swap]] = [pool[swap], pool[index]];
  }
  return pool;
}

function drawSpread() {
  const spread = currentSpread();
  state.drawn = shuffleDeck()
    .slice(0, spread.slots.length)
    .map((card) => ({ ...card, reversed: Math.random() < 0.32 }));
  state.revealedCount = 0;
  state.selectedIndex = -1;
  state.notes = {};
  state.restoredAt = null;
  state.reviewedHistoryKey = null;
  state.afterSaveKey = null;
  state.studySheetOpen = false;
  state.studySheetCardId = null;
  state.inspectorTab = "card";
  state.slotDrill = blankSlotDrill();
  els.noteStatus.textContent = "";
  render();
}

function revealNext() {
  if (!state.drawn.length) drawSpread();
  if (state.revealedCount >= state.drawn.length) return;
  state.revealedCount += 1;
  state.selectedIndex = state.revealedCount - 1;
  state.inspectorTab = "card";
  els.noteStatus.textContent = "自分の読みを記録";
  render();
}

function resetTable() {
  state.drawn = [];
  state.revealedCount = 0;
  state.selectedIndex = -1;
  state.notes = {};
  state.restoredAt = null;
  state.reviewedHistoryKey = null;
  state.afterSaveKey = null;
  state.studySheetOpen = false;
  state.studySheetCardId = null;
  state.inspectorTab = "card";
  state.slotDrill = blankSlotDrill();
  els.noteStatus.textContent = "";
  render();
}

function slotIsRevealed(index) {
  return index >= 0 && index < state.revealedCount;
}

function selectedSlot() {
  const spread = currentSpread();
  if (!slotIsRevealed(state.selectedIndex)) return null;
  return {
    index: state.selectedIndex,
    slot: spread.slots[state.selectedIndex],
    card: state.drawn[state.selectedIndex]
  };
}

function slotNoteKey(slot, index) {
  return `${index + 1}:${slot.key}`;
}

function normalizeReadingNotes(item, spread) {
  const normalized = {};
  const sourceNotes = item && item.notes && typeof item.notes === "object" && !Array.isArray(item.notes)
    ? item.notes
    : {};

  Object.entries(sourceNotes).forEach(([key, value]) => {
    if (typeof value === "string") normalized[key] = value;
  });

  if (!item || !Array.isArray(item.cards)) return normalized;

  item.cards.forEach((entry, index) => {
    const slot = spread.slots[index] || spread.slots.find((candidate) => candidate.key === entry.slotKey);
    if (!slot) return;
    const key = slotNoteKey(slot, index);
    const legacyKeys = [
      key,
      `${entry.slotKey}-${index}`,
      `${entry.slotKey}:${index}`,
      `${index}:${entry.slotKey}`
    ];
    const legacyNote = legacyKeys
      .map((candidateKey) => sourceNotes[candidateKey])
      .find((value) => typeof value === "string");
    if (typeof legacyNote === "string") {
      normalized[key] = legacyNote;
      return;
    }
    if (typeof entry.note === "string") normalized[key] = entry.note;
  });

  return normalized;
}

function selectedNote() {
  const selected = selectedSlot();
  if (!selected) return "";
  return state.notes[slotNoteKey(selected.slot, selected.index)] || "";
}

function escapeText(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function cardLabel(card) {
  return `${card.displayNumber} ${card.japaneseName}`;
}

function orientationLabel(orientation) {
  return orientation === "reversed" ? "逆位置" : "正位置";
}

function recallKeywords(card, orientation) {
  return orientation === "reversed" ? card.reversedKeywords : card.uprightKeywords;
}

function nextRecallCardId(currentCardId) {
  const currentIndex = getCardIndex(currentCardId);
  const nextIndex = currentIndex >= 0 ? (currentIndex + 1) % cards.length : 0;
  return cards[nextIndex].id;
}

function confidenceIntervalDays(confidence) {
  if (confidence === "hard") return 0;
  if (confidence === "ok") return 1;
  if (confidence === "easy") return 3;
  return 1;
}

function validDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function dueDateForAttempt(attempt) {
  const attemptedAt = validDate(attempt.attemptedAt);
  if (!attemptedAt) return null;
  return new Date(attemptedAt.getTime() + confidenceIntervalDays(attempt.confidence) * 86400000);
}

function learningDueSummary(learningState, now = new Date()) {
  const latestByPrompt = new Map();
  learningState.attempts.forEach((attempt) => {
    const attemptedAt = validDate(attempt.attemptedAt);
    const card = getCard(attempt.cardId);
    if (!attemptedAt || !card) return;
    const promptKey = [card.id, attempt.orientation, attempt.promptType].join("||");
    const current = latestByPrompt.get(promptKey);
    if (!current || attemptedAt > current.attemptedAt) {
      latestByPrompt.set(promptKey, { attempt, attemptedAt, card });
    }
  });

  const items = [...latestByPrompt.values()].map((item) => {
    const dueAt = dueDateForAttempt(item.attempt);
    return { ...item, dueAt };
  }).filter((item) => item.dueAt);
  const sortItems = (a, b) => a.dueAt - b.dueAt || a.card.number.localeCompare(b.card.number);
  const sortedItems = items.sort(sortItems);
  const due = [];
  const upcoming = [];
  let hardCount = 0;

  sortedItems.forEach((item) => {
    if (item.attempt.confidence === "hard") hardCount += 1;
    if (item.dueAt <= now) {
      due.push(item);
    } else {
      upcoming.push(item);
    }
  });

  return {
    due,
    upcoming,
    hardCount,
    totalTracked: items.length
  };
}

function shortDateTimeCopy(date) {
  return date.toLocaleString("ja-JP", {
    month: "numeric",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
}

function cardForHistoryEntry(entry) {
  if (!entry || typeof entry.cardId !== "string") return null;
  return getCard(entry.cardId);
}

function historyItemHasCard(item, cardId) {
  return Boolean(item && Array.isArray(item.cards) && item.cards.some((entry) => entry.cardId === cardId));
}

function historyRowsForFilter(history, cardId) {
  const rows = [];
  history.forEach((item, index) => {
    if (cardId && !historyItemHasCard(item, cardId)) return;
    rows.push({ item, index });
  });
  return rows;
}

function renderSpreadMini(spread) {
  return `
    <span class="spread-mini" aria-hidden="true">
      ${spread.slots.map((slot, index) => `
        <span class="spread-mini-slot ${index === 0 ? "is-first" : ""}" style="--x:${slot.x}%; --y:${slot.y}%; --rot:${slot.rot}deg;"></span>
      `).join("")}
      <span class="spread-mini-count">${spread.slots.length}</span>
    </span>
  `;
}

function renderSpreadControls() {
  els.spreadControls.innerHTML = spreads.map((spread) => `
    <button class="spread-choice ${spread.id === state.spreadId ? "is-active" : ""}" type="button" data-spread-id="${spread.id}">
      ${renderSpreadMini(spread)}
      <span class="spread-choice-copy">
        <strong>${escapeText(spread.label)}</strong>
        <span>${escapeText(spread.description)}</span>
      </span>
    </button>
  `).join("");

  els.spreadControls.querySelectorAll("[data-spread-id]").forEach((button) => {
    button.addEventListener("click", () => {
      if (state.spreadId === button.dataset.spreadId) return;
      state.spreadId = button.dataset.spreadId;
      resetTable();
    });
  });
}

function boardTextMode(spread) {
  if (spread.slots.length <= 3) return "inscription";
  return "marker";
}

function renderBoard() {
  const spread = currentSpread();
  const textMode = boardTextMode(spread);
  const dense = textMode === "marker";
  els.spreadBoard.className = `spread-board layout-${spread.id} mode-${textMode} ${dense ? "is-dense-board" : ""}`;
  els.spreadBoard.innerHTML = spread.slots.map((slot, index) => {
    const card = state.drawn[index];
    const revealed = slotIsRevealed(index);
    const selected = revealed && index === state.selectedIndex;
    const image = card && revealed ? card.image : CARD_BACK;
    const slotClasses = [
      "slot",
      card ? "is-filled" : "",
      revealed ? "is-revealed" : "",
      selected ? "is-selected" : ""
    ].filter(Boolean).join(" ");
    const classes = [
      "arcana-card",
      !card ? "is-empty" : "",
      card && !revealed ? "is-hidden" : "",
      card && revealed && card.reversed ? "is-reversed" : "",
      selected ? "is-selected" : ""
    ].filter(Boolean).join(" ");
    const topLabel = card && revealed ? `${card.displayNumber} ${card.japaneseName}` : card ? "カード裏面" : "空きスロット";
    const orientationShort = card && revealed ? (card.reversed ? "逆" : "正") : "";
    const cardTableCaption = card && revealed && textMode === "inscription" ? `
        <div class="card-table-caption">
          <b>${escapeText(`${card.displayNumber} ${card.japaneseName}`)}</b>
          <span>${card.reversed ? "逆位置" : "正位置"} / ${escapeText(slot.label)}</span>
        </div>
        ` : "";
    const cardMarker = card && revealed && textMode === "marker" ? `
          <span class="card-marker" aria-hidden="true">
            <span>${index + 1}</span>
            <small>${orientationShort}</small>
          </span>
        ` : "";
    const slotLabelMarkup = dense ? "" : `
        <div class="slot-label" title="${index + 1}. ${escapeText(slot.label)}">
          <span class="slot-label-index">${index + 1}</span>
          <span class="slot-label-text">${escapeText(slot.label)}</span>
        </div>
      `;
    return `
      <div class="${slotClasses}" style="--x:${slot.x}%; --y:${slot.y}%; --rot:${slot.rot}deg; --counter-rot:${-slot.rot}deg;">
        ${slotLabelMarkup}
        <button class="${classes}" type="button" data-slot-index="${index}" ${!revealed ? "aria-disabled='true' tabindex='-1'" : ""}>
          ${card ? `<img class="${card.reversed && revealed ? "reversed" : ""}" src="${image}" alt="${escapeText(topLabel)}">` : "<span class='empty-mark'></span>"}
          ${cardMarker}
        </button>
        ${cardTableCaption}
      </div>
    `;
  }).join("");

  els.spreadBoard.querySelectorAll("[data-slot-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.slotIndex);
      if (!slotIsRevealed(index)) return;
      state.selectedIndex = index;
      state.inspectorTab = "card";
      els.noteStatus.textContent = selectedNote() ? "記録済み" : "自分の読みを記録";
      render();
    });
  });
}

function renderProgress() {
  const spread = currentSpread();
  els.progressTrack.innerHTML = spread.slots.map((slot, index) => {
    const revealed = slotIsRevealed(index);
    const selected = revealed && index === state.selectedIndex;
    return `
      <button class="progress-dot ${revealed ? "is-revealed" : ""} ${selected ? "is-selected" : ""}" type="button" data-progress-index="${index}">
        <span class="progress-gem" aria-hidden="true"></span>
        <span>${index + 1}. ${escapeText(slot.label)}</span>
      </button>
    `;
  }).join("");

  els.progressTrack.querySelectorAll("[data-progress-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.progressIndex);
      if (!slotIsRevealed(index)) return;
      state.selectedIndex = index;
      state.inspectorTab = "card";
      render();
    });
  });
}

function activeStudySheetContext() {
  const selected = selectedSlot();
  const explicitCard = state.studySheetCardId
    ? getCard(state.studySheetCardId)
    : null;
  const card = explicitCard || selected?.card || null;
  const selectedMatches = Boolean(card && selected?.card?.id === card.id);
  return {
    card,
    selected,
    selectedMatches,
    orientationText: selectedMatches ? (selected.card.reversed ? "逆位置" : "正位置") : "正逆比較"
  };
}

function selectedStudySheetContext() {
  const selected = selectedSlot();
  if (!selected) {
    return {
      card: null,
      selected: null,
      selectedMatches: false,
      orientationText: "正逆比較"
    };
  }
  return {
    card: selected.card,
    selected,
    selectedMatches: true,
    orientationText: selected.card.reversed ? "逆位置" : "正位置"
  };
}

function slotDrillKey(card, selected) {
  if (!card || !selected) return "";
  const orientation = selected.card.reversed ? "reversed" : "upright";
  return [currentSpread().id, selected.slot.key, card.id, orientation].join("||");
}

function ensureSlotDrillContext(card, selected, selectedMatches) {
  if (!selectedMatches || !selected) return null;
  const key = slotDrillKey(card, selected);
  const orientation = selected.card.reversed ? "reversed" : "upright";
  if (state.slotDrill.key !== key) {
    state.slotDrill = {
      ...blankSlotDrill(),
      key,
      cardId: card.id,
      slotKey: selected.slot.key,
      orientation
    };
  }
  return state.slotDrill;
}

function renderStudyDetailList(items, className) {
  if (!Array.isArray(items) || !items.length) return "";
  return `
    <ul class="${className}">
      ${items.map((item) => `<li>${escapeText(item)}</li>`).join("")}
    </ul>
  `;
}

function revealSlotDrillGuide() {
  if (!state.slotDrill.answer.trim()) return;
  state.slotDrill.revealed = true;
  state.slotDrill.savedConfidence = null;
  state.slotDrill.status = "解説を見て、自分の解釈と比べます。";
  renderStudySheets();
}

function saveSlotInterpretationAttempt(confidence, context = activeStudySheetContext()) {
  if (!["hard", "ok", "easy"].includes(confidence)) return;
  const { card, selected, selectedMatches } = context;
  const answer = state.slotDrill.answer.trim();
  if (!card || !selected || !selectedMatches || !answer || !state.slotDrill.revealed) return;
  const spread = currentSpread();
  const orientation = selected.card.reversed ? "reversed" : "upright";
  const learningState = readLearningState();
  learningState.attempts.unshift({
    attemptedAt: new Date().toISOString(),
    cardId: card.id,
    cardLabel: cardLabel(card),
    orientation,
    promptType: "slot_interpretation",
    answer,
    confidence,
    spreadId: spread.id,
    spreadLabel: spread.label,
    slotKey: selected.slot.key,
    slotLabel: selected.slot.label,
    slotPrompt: selected.slot.prompt || ""
  });
  if (!writeLearningState(learningState)) {
    state.slotDrill.status = "スロット練習を保存できません。ブラウザの保存設定を確認してください。";
    renderStudySheets();
    return;
  }
  state.slotDrill = {
    ...blankSlotDrill(`スロット練習を保存しました / ${confidence}`),
    key: slotDrillKey(card, selected),
    cardId: card.id,
    slotKey: selected.slot.key,
    orientation
  };
  render();
}

function renderSlotInterpretationDrill(card, selected, selectedMatches, prefix = "study") {
  if (!selectedMatches || !selected) {
    return `
      <section class="slot-drill-card is-disabled" data-slot-drill>
        <div class="slot-drill-head">
          <strong>スロット練習</strong>
          <span>卓上選択時</span>
        </div>
        <p>卓でこのカードを選ぶと、スプレッド位置と正逆込みの解釈練習を開けます。</p>
      </section>
    `;
  }

  const drill = ensureSlotDrillContext(card, selected, selectedMatches);
  const orientationText = selected.card.reversed ? "逆位置" : "正位置";
  const keywords = selected.card.reversed ? card.reversedKeywords : card.uprightKeywords;
  const canReveal = drill.answer.trim().length > 0;
  const answerId = `${prefix}SlotDrillAnswer`;
  return `
    <section class="slot-drill-card is-active" data-slot-drill data-slot-drill-key="${escapeText(drill.key)}">
      <div class="slot-drill-head">
        <strong>スロット練習</strong>
        <span>${escapeText(selected.slot.label)} / ${escapeText(orientationText)}</span>
      </div>
      <p>この位置だから意味はどう変わる？ 解説を見る前に一文で書きます。</p>
      <label class="slot-drill-answer-label" for="${escapeText(answerId)}">自分のスロット解釈</label>
      <textarea id="${escapeText(answerId)}" class="text-field slot-drill-answer" rows="3" placeholder="例: この位置では、カードの性質が課題や助言としてどう出るかを書く" data-slot-drill-answer>${escapeText(drill.answer)}</textarea>
      <div class="slot-drill-action-row">
        <button class="button compact" type="button" data-slot-drill-reveal ${canReveal ? "" : "disabled"}>解説を見る</button>
      </div>
      ${drill.revealed ? `
        <div class="slot-drill-guide" data-slot-drill-guide>
          <div>
            <b>スロット</b>
            <span>${escapeText(selected.slot.prompt)}</span>
          </div>
          <div>
            <b>${escapeText(orientationText)}</b>
            <span>${escapeText(keywords.join(" / "))}。${escapeText(card.studyFocus)}</span>
          </div>
        </div>
        <div class="slot-drill-confidence" role="group" aria-label="スロット解釈の手応え">
          <button type="button" data-slot-drill-confidence="hard" class="${drill.savedConfidence === "hard" ? "is-active" : ""}">hard</button>
          <button type="button" data-slot-drill-confidence="ok" class="${drill.savedConfidence === "ok" ? "is-active" : ""}">ok</button>
          <button type="button" data-slot-drill-confidence="easy" class="${drill.savedConfidence === "easy" ? "is-active" : ""}">easy</button>
        </div>
      ` : ""}
      ${drill.status ? `<p class="slot-drill-status">${escapeText(drill.status)}</p>` : ""}
    </section>
  `;
}

function bindStudySheetActions(container, contextProvider = activeStudySheetContext) {
  container?.querySelector("[data-study-sheet-recall]")?.addEventListener("click", (event) => {
    const cardId = event.currentTarget.dataset.studySheetRecall;
    beginRecallPractice(cardId);
  });
  container?.querySelector("[data-study-sheet-filter]")?.addEventListener("click", (event) => {
    const cardId = event.currentTarget.dataset.studySheetFilter;
    selectHistoryCardFilter(cardId);
  });
  container?.querySelector("[data-slot-drill-reveal]")?.addEventListener("click", revealSlotDrillGuide);
  container?.querySelectorAll("[data-slot-drill-confidence]").forEach((button) => {
    button.addEventListener("click", () => saveSlotInterpretationAttempt(button.dataset.slotDrillConfidence, contextProvider()));
  });
  const slotAnswer = container?.querySelector("[data-slot-drill-answer]");
  slotAnswer?.addEventListener("input", () => {
    state.slotDrill.answer = slotAnswer.value;
    state.slotDrill.savedConfidence = null;
    state.slotDrill.status = "";
    const revealButton = container?.querySelector("[data-slot-drill-reveal]");
    if (revealButton) revealButton.disabled = !slotAnswer.value.trim();
  });
}

function renderStudySheetMarkup(context, options = {}) {
  const { card, selected, selectedMatches, orientationText } = context;
  const {
    open = true,
    prefix = "study",
    emptyCopy = "カードをめくるか、学習レンズからカードを選ぶと学習シートを開けます。",
    collapsedCopy = "正逆キーワード、象徴、誤読しやすい点、内省質問を必要な時だけ開きます。"
  } = options;
  if (!card) {
    return `<p class="empty">${escapeText(emptyCopy)}</p>`;
  }

  const details = card.studyDetails || {};
  const activeKeywords = selectedMatches && selected.card.reversed
    ? card.reversedKeywords
    : card.uprightKeywords;
  const contextCopy = selectedMatches && selected
    ? `${selected.index + 1}. ${selected.slot.label} / ${orientationText}`
    : "学習レンズから選択";

  if (!open) {
    return `<p class="empty">${escapeText(collapsedCopy)}</p>`;
  }

  return `
    <article class="card-study-sheet" data-study-sheet-open data-study-sheet-source="${escapeText(prefix)}" data-study-sheet-card-id="${escapeText(card.id)}">
      <header class="study-sheet-head">
        <div>
          <b>${escapeText(cardLabel(card))}</b>
          <span>${escapeText(contextCopy)}</span>
        </div>
        <span class="study-sheet-orientation">${escapeText(orientationText)}</span>
      </header>
      <div class="study-detail-grid">
        <section>
          <strong>正位置</strong>
          <p>${escapeText(card.uprightKeywords.join(" / "))}</p>
        </section>
        <section>
          <strong>逆位置</strong>
          <p>${escapeText(card.reversedKeywords.join(" / "))}</p>
        </section>
      </div>
      <div class="study-focus-box">
        <b>今回の焦点</b>
        <span>${escapeText(activeKeywords.join(" / "))}。${escapeText(card.studyFocus)}</span>
      </div>
      <section class="study-symbols">
        <strong>象徴</strong>
        <div class="symbol-chip-row">
          ${(details.symbols || []).map((symbol) => `<span class="symbol-chip">${escapeText(symbol)}</span>`).join("")}
        </div>
      </section>
      <section>
        <strong>誤読しやすい点</strong>
        ${renderStudyDetailList(details.commonMisreads, "study-caution-list")}
      </section>
      <section>
        <strong>内省質問</strong>
        ${renderStudyDetailList(details.reflectionQuestions, "study-reflection-list")}
      </section>
      ${renderSlotInterpretationDrill(card, selected, selectedMatches, prefix)}
      <div class="study-sheet-actions">
        <button class="button compact" type="button" data-study-sheet-recall="${escapeText(card.id)}">想起練習</button>
        <button class="button compact quiet" type="button" data-study-sheet-filter="${escapeText(card.id)}">過去の読み</button>
      </div>
    </article>
  `;
}

function renderCardStudySheet() {
  if (!els.cardStudySheetPanel) return;
  els.cardStudySheetPanel.innerHTML = renderStudySheetMarkup(selectedStudySheetContext(), {
    open: true,
    prefix: "card",
    emptyCopy: "カードをめくると、自分の読みの横で学習シートを確認できます。"
  });
  bindStudySheetActions(els.cardStudySheetPanel, selectedStudySheetContext);
}

function openStudySheet(cardId) {
  const card = getCard(cardId);
  if (!card) return;
  state.studySheetCardId = card.id;
  state.studySheetOpen = true;
  state.inspectorTab = "study";
  render();
}

function toggleStudySheet() {
  const { card } = activeStudySheetContext();
  if (!card) return;
  state.studySheetOpen = !state.studySheetOpen;
  state.inspectorTab = "study";
  render();
}

function renderStudySheet() {
  if (!els.studySheetPanel || !els.toggleStudySheetButton) return;
  const context = activeStudySheetContext();
  const { card } = context;
  if (!card) {
    els.toggleStudySheetButton.disabled = true;
    els.toggleStudySheetButton.textContent = "学習シート";
    els.toggleStudySheetButton.setAttribute("aria-expanded", "false");
    els.studySheetPanel.innerHTML = renderStudySheetMarkup(context);
    return;
  }
  els.toggleStudySheetButton.disabled = false;
  els.toggleStudySheetButton.textContent = state.studySheetOpen ? "閉じる" : "学習シート";
  els.toggleStudySheetButton.setAttribute("aria-expanded", state.studySheetOpen ? "true" : "false");
  els.studySheetPanel.innerHTML = renderStudySheetMarkup(context, {
    open: state.studySheetOpen,
    prefix: "study"
  });
  bindStudySheetActions(els.studySheetPanel, activeStudySheetContext);
}

function renderStudySheets() {
  renderCardStudySheet();
  renderStudySheet();
}

function renderInspector() {
  const selected = selectedSlot();
  if (!selected) {
    els.selectedCard.innerHTML = `
      <img src="${CARD_BACK}" alt="カード裏面">
      <div class="selected-copy">
        <h2>未選択</h2>
        <p>カードをめくると、選択中の読みが表示されます。</p>
        <div class="badge-row"><span class="badge gold">${escapeText(currentSpread().label)}</span></div>
      </div>
    `;
    els.noteInput.value = "";
    els.noteInput.disabled = true;
    renderStudySheets();
    return;
  }

  const { index, slot, card } = selected;
  const orientationText = card.reversed ? "逆位置" : "正位置";
  const activeKeywords = card.reversed ? card.reversedKeywords : card.uprightKeywords;
  const note = selectedNote();
  els.selectedCard.innerHTML = `
    <img class="${card.reversed ? "reversed" : ""}" src="${card.image}" alt="${escapeText(`${card.displayNumber} ${card.japaneseName}`)}">
    <div class="selected-copy">
      <h2>${escapeText(`${card.displayNumber} ${card.japaneseName}`)}</h2>
      <p>${escapeText(card.englishName)}</p>
      <div class="badge-row">
        <span class="badge gold">${index + 1}. ${escapeText(slot.label)}</span>
        <span class="badge">${escapeText(card.displayNumber)}</span>
        <span class="badge">${orientationText}</span>
      </div>
      <p class="keyword-preview"><b>キーワード</b>${escapeText(activeKeywords.join(" / "))}</p>
    </div>
  `;
  els.noteInput.disabled = false;
  els.noteInput.value = note;
  renderStudySheets();
}

function renderFirstLaunchGuide(history) {
  if (history.length || state.drawn.length) return "";
  return `
    <section class="first-launch-guide" data-first-launch-guide>
      <div class="first-launch-head">
        <strong>はじめの一巡</strong>
        <span>学習シートを見ながら読む</span>
      </div>
      <ol class="first-launch-steps">
        <li><b>1</b><span>問いを書く</span></li>
        <li><b>2</b><span>スプレッドを選ぶ</span></li>
        <li><b>3</b><span>カードを引いて自分の読みを書く</span></li>
        <li><b>4</b><span>学習シートを見ながら保存し、後で復習する</span></li>
      </ol>
      <div class="first-launch-actions">
        <button class="button compact" type="button" data-first-launch-focus-question>問いへ</button>
        <button class="button compact quiet" type="button" data-first-launch-one-card>一枚引きで始める</button>
      </div>
    </section>
  `;
}

function firstHistoryCardId(item) {
  const entry = Array.isArray(item?.cards)
    ? item.cards.find((candidate) => candidate && getCard(candidate.cardId))
    : null;
  return entry?.cardId || cards[0].id;
}

function renderAfterSaveActions(item) {
  const key = readingIdentity(item);
  if (state.afterSaveKey !== key) return "";
  return `
    <div class="after-save-actions" data-after-save-actions>
      <div>
        <strong>保存しました</strong>
        <span>今の読みを復習するか、次の問いへ進めます。</span>
      </div>
      <div class="after-save-buttons">
        <button class="button compact" type="button" data-after-save-practice="${escapeText(firstHistoryCardId(item))}">想起練習</button>
        <button class="button compact quiet" type="button" data-after-save-next>次の問い</button>
      </div>
    </div>
  `;
}

function focusQuestionFromGuide() {
  state.inspectorTab = "card";
  renderInspectorTabs();
  els.questionInput.focus();
}

function startOneCardFromGuide() {
  state.spreadId = "one_card";
  resetTable();
  window.requestAnimationFrame(() => els.questionInput.focus());
}

function startNextQuestion() {
  state.afterSaveKey = null;
  els.questionInput.value = "";
  resetTable();
  els.noteStatus.textContent = "次の問いを入力";
  window.requestAnimationFrame(() => els.questionInput.focus());
}

function bindHistoryReviewActions() {
  els.historyReview.querySelector("[data-first-launch-focus-question]")?.addEventListener("click", focusQuestionFromGuide);
  els.historyReview.querySelector("[data-first-launch-one-card]")?.addEventListener("click", startOneCardFromGuide);
  els.historyReview.querySelector("[data-after-save-next]")?.addEventListener("click", startNextQuestion);
  els.historyReview.querySelector("[data-after-save-practice]")?.addEventListener("click", (event) => {
    const button = event.currentTarget;
    beginRecallPractice(button.dataset.afterSavePractice);
  });
}

function renderHistoryReview(history) {
  if (!els.historyReview) return;
  const item = history.find((candidate) => readingIdentity(candidate) === state.reviewedHistoryKey);
  if (!item) {
    if (state.reviewedHistoryKey) state.reviewedHistoryKey = null;
    els.historyReview.innerHTML = `
      <div class="history-review-empty">
        <b>復習ノート</b>
        <span>履歴を選ぶと、問い、カード、保存メモをここで読み返せます。</span>
        ${renderFirstLaunchGuide(history)}
      </div>
    `;
    bindHistoryReviewActions();
    return;
  }

  const spread = getSpread(item.spreadId);
  const cardRows = item.cards.map((entry, index) => {
    const note = typeof entry.note === "string" ? entry.note.trim() : "";
    const orientation = entry.reversed ? "逆位置" : "正位置";
    const card = cardForHistoryEntry(entry);
    const slot = spread?.slots.find((candidate) => candidate.key === entry.slotKey);
    const isFilterMatch = Boolean(state.historyCardFilter && entry.cardId === state.historyCardFilter && card);
    const activeKeywords = card
      ? (entry.reversed ? card.reversedKeywords : card.uprightKeywords)
      : [];
    const displayNumber = entry.displayNumber || entry.number || card?.displayNumber || card?.number || "";
    const japaneseName = entry.japaneseName || entry.cardName || card?.japaneseName || entry.cardId;
    return `
      <li class="review-card-row ${isFilterMatch ? "is-filter-match" : ""}">
        <b>${index + 1}. ${escapeText(entry.slotLabel || entry.slotKey)}</b>
        <span>${escapeText(`${displayNumber} ${japaneseName}`.trim())} / ${orientation}</span>
        ${note ? `<em>${escapeText(note)}</em>` : "<em>メモなし</em>"}
        ${isFilterMatch ? `
          <div class="review-learning-compare">
            <div>
              <strong>自分の読み</strong>
              <span>${note ? escapeText(note) : "まだメモなし"}</span>
            </div>
            <div>
              <strong>学習シート</strong>
              <span>${escapeText(activeKeywords.join(" / "))}${card.studyFocus ? `。${escapeText(card.studyFocus)}` : ""}</span>
            </div>
            ${slot?.prompt ? `
              <div>
                <strong>スロット</strong>
                <span>${escapeText(slot.prompt)}</span>
              </div>
            ` : ""}
          </div>
        ` : ""}
      </li>
    `;
  }).join("");

  els.historyReview.innerHTML = `
    <article class="history-review-card" data-review-active="true">
      <div class="review-head">
        <b>復習ノート</b>
        <span>${escapeText(item.savedAt)}</span>
      </div>
      ${renderAfterSaveActions(item)}
      ${item.question ? `<p class="review-question">${escapeText(item.question)}</p>` : ""}
      <ol class="review-card-list">
        ${cardRows}
      </ol>
    </article>
  `;
  bindHistoryReviewActions();
}

function studyStats(history) {
  const byCard = new Map();
  let notedCards = 0;

  history.forEach((item) => {
    if (!item || !Array.isArray(item.cards)) return;
    item.cards.forEach((entry) => {
      if (!entry || typeof entry.cardId !== "string") return;
      const card = getCard(entry.cardId);
      if (!card) return;
      const current = byCard.get(card.id) || {
        card,
        count: 0,
        noted: 0,
        latestNote: "",
        latestOrientation: ""
      };
      const note = typeof entry.note === "string" ? entry.note.trim() : "";
      current.count += 1;
      if (note) {
        current.noted += 1;
        current.latestNote = note;
        notedCards += 1;
      }
      if (!current.latestOrientation) current.latestOrientation = entry.reversed ? "逆位置" : "正位置";
      byCard.set(card.id, current);
    });
  });

  const seenCards = [...byCard.values()].sort((a, b) => {
    if (b.count !== a.count) return b.count - a.count;
    return a.card.number.localeCompare(b.card.number);
  });
  const unseenCards = cards.filter((card) => !byCard.has(card.id));
  return {
    readings: history.length,
    seenCount: byCard.size,
    notedCards,
    unseenCount: unseenCards.length,
    topCards: seenCards.slice(0, 3),
    recentFocus: seenCards.find((entry) => entry.latestNote) || seenCards[0] || null,
    nextCards: unseenCards.slice(0, 3)
  };
}

function recommendedRecallCard(stats) {
  if (state.historyCardFilter) {
    const filteredCard = getCard(state.historyCardFilter);
    if (filteredCard) return filteredCard;
  }
  if (stats.recentFocus?.card) return stats.recentFocus.card;
  if (stats.nextCards[0]) return stats.nextCards[0];
  return cards[0];
}

function renderDueReviewCue(dueSummary) {
  if (!dueSummary.totalTracked) return "";
  if (dueSummary.due.length) {
    const dueButtons = dueSummary.due.slice(0, 3).map((item) => `
      <button class="study-chip due-chip" type="button" data-recall-start="${escapeText(item.card.id)}">
        ${escapeText(cardLabel(item.card))} / ${escapeText(item.attempt.confidence)}
      </button>
    `).join("");
    return `
      <div class="due-review-cue" data-due-review-cue>
        <div>
          <strong>次に復習</strong>
          <span><b>${dueSummary.due.length}</b>枚が復習時期です</span>
        </div>
        <div class="study-chip-row">${dueButtons}</div>
      </div>
    `;
  }
  const next = dueSummary.upcoming[0];
  if (!next) {
    return `
      <div class="due-review-cue is-quiet" data-due-review-cue>
        <div>
          <strong>次に復習</strong>
          <span>次の練習後に予定が出ます</span>
        </div>
      </div>
    `;
  }
  return `
    <div class="due-review-cue is-quiet" data-due-review-cue>
      <div>
        <strong>次に復習</strong>
        <span>${escapeText(cardLabel(next.card))} / ${escapeText(shortDateTimeCopy(next.dueAt))}</span>
      </div>
    </div>
  `;
}

function beginRecallPractice(cardId) {
  const card = getCard(cardId) || cards[0];
  state.inspectorTab = "study";
  state.recallPractice = {
    cardId: card.id,
    orientation: "upright",
    answer: "",
    revealed: false,
    savedConfidence: null,
    status: ""
  };
  renderHistory();
}

function setRecallOrientation(orientation) {
  if (orientation !== "upright" && orientation !== "reversed") return;
  state.recallPractice.orientation = orientation;
  state.recallPractice.revealed = false;
  state.recallPractice.savedConfidence = null;
  state.recallPractice.status = "";
  renderHistory();
}

function revealRecallGuide() {
  if (!state.recallPractice.answer.trim()) return;
  state.recallPractice.revealed = true;
  state.recallPractice.savedConfidence = null;
  state.recallPractice.status = "学習シートを見て、自分の想起と比べます。";
  renderHistory();
}

function saveRecallAttempt(confidence) {
  if (!["hard", "ok", "easy"].includes(confidence)) return;
  const card = getCard(state.recallPractice.cardId);
  const answer = state.recallPractice.answer.trim();
  if (!card || !answer || !state.recallPractice.revealed) return;
  const learningState = readLearningState();
  learningState.attempts.unshift({
    attemptedAt: new Date().toISOString(),
    cardId: card.id,
    cardLabel: cardLabel(card),
    orientation: state.recallPractice.orientation,
    promptType: "keyword_recall",
    answer,
    confidence
  });
  if (!writeLearningState(learningState)) {
    state.recallPractice.status = "練習結果を保存できません。ブラウザの保存設定を確認してください。";
    renderHistory();
    return;
  }
  state.recallPractice = {
    cardId: null,
    orientation: "upright",
    answer: "",
    revealed: false,
    savedConfidence: null,
    status: `練習結果を保存しました / ${confidence}`
  };
  renderHistory();
}

function renderRecallPractice(stats, learningState) {
  const suggestedCard = recommendedRecallCard(stats);
  const activeCard = state.recallPractice.cardId
    ? getCard(state.recallPractice.cardId)
    : null;
  const latestAttempt = learningState.attempts[0];
  const latestCopy = state.recallPractice.status || (latestAttempt
    ? `${latestAttempt.cardLabel || latestAttempt.cardId} / ${orientationLabel(latestAttempt.orientation)} / ${latestAttempt.confidence}`
    : "まだ練習記録はありません");

  if (!activeCard) {
    return `
      <section class="recall-practice-card" data-recall-practice>
        <div class="recall-head">
          <strong>想起練習</strong>
          <span>${learningState.attempts.length} 回</span>
        </div>
        <p>学習シートを見る前に、カードのキーワードを自分で思い出します。</p>
        <div class="recall-meta">${learningReadFailed ? "学習データを一部読めませんでした。" : escapeText(latestCopy)}</div>
        <button class="button compact recall-start" type="button" data-recall-start="${escapeText(suggestedCard.id)}">
          ${escapeText(cardLabel(suggestedCard))} で練習
        </button>
      </section>
    `;
  }

  const orientation = state.recallPractice.orientation;
  const keywords = recallKeywords(activeCard, orientation);
  const answer = state.recallPractice.answer;
  const canReveal = answer.trim().length > 0;
  return `
    <section class="recall-practice-card is-active" data-recall-practice>
      <div class="recall-head">
        <strong>想起練習</strong>
        <span>${escapeText(cardLabel(activeCard))}</span>
      </div>
      <div class="recall-mode-row" role="group" aria-label="想起する向き">
        <button class="recall-mode ${orientation === "upright" ? "is-active" : ""}" type="button" data-recall-orientation="upright">正位置</button>
        <button class="recall-mode ${orientation === "reversed" ? "is-active" : ""}" type="button" data-recall-orientation="reversed">逆位置</button>
      </div>
      <label class="recall-answer-label" for="recallAnswer">学習シートを見る前に思い出す</label>
      <textarea id="recallAnswer" class="text-field recall-answer" rows="3" placeholder="覚えているキーワードや読みの傾向を書く">${escapeText(answer)}</textarea>
      <div class="recall-action-row">
        <button class="button compact" type="button" data-recall-reveal ${canReveal ? "" : "disabled"}>答え合わせ</button>
        <button class="button compact quiet" type="button" data-recall-next="${escapeText(nextRecallCardId(activeCard.id))}">別カード</button>
      </div>
      ${state.recallPractice.revealed ? `
        <div class="recall-guide" data-recall-guide>
          <b>${orientationLabel(orientation)} 学習シート</b>
          <span>${escapeText(keywords.join(" / "))}。${escapeText(activeCard.studyFocus)}</span>
        </div>
        <div class="recall-confidence" role="group" aria-label="想起の手応え">
          <button type="button" data-recall-confidence="hard" class="${state.recallPractice.savedConfidence === "hard" ? "is-active" : ""}">hard</button>
          <button type="button" data-recall-confidence="ok" class="${state.recallPractice.savedConfidence === "ok" ? "is-active" : ""}">ok</button>
          <button type="button" data-recall-confidence="easy" class="${state.recallPractice.savedConfidence === "easy" ? "is-active" : ""}">easy</button>
        </div>
      ` : ""}
      ${state.recallPractice.status ? `<p class="recall-status">${escapeText(state.recallPractice.status)}</p>` : ""}
    </section>
  `;
}

function bindStudyLensActions() {
  els.studyLens.querySelectorAll("[data-study-card-id]").forEach((button) => {
    button.addEventListener("click", () => selectHistoryCardFilter(button.dataset.studyCardId));
  });
  els.studyLens.querySelectorAll("[data-study-sheet-card-id]").forEach((button) => {
    button.addEventListener("click", () => openStudySheet(button.dataset.studySheetCardId));
  });
  els.studyLens.querySelectorAll("[data-recall-start], [data-recall-next]").forEach((button) => {
    button.addEventListener("click", () => beginRecallPractice(button.dataset.recallStart || button.dataset.recallNext));
  });
  els.studyLens.querySelectorAll("[data-recall-orientation]").forEach((button) => {
    button.addEventListener("click", () => setRecallOrientation(button.dataset.recallOrientation));
  });
  els.studyLens.querySelector("[data-recall-reveal]")?.addEventListener("click", revealRecallGuide);
  els.studyLens.querySelectorAll("[data-recall-confidence]").forEach((button) => {
    button.addEventListener("click", () => saveRecallAttempt(button.dataset.recallConfidence));
  });
  const answerField = els.studyLens.querySelector("#recallAnswer");
  answerField?.addEventListener("input", () => {
    state.recallPractice.answer = answerField.value;
    state.recallPractice.savedConfidence = null;
    state.recallPractice.status = "";
    const revealButton = els.studyLens.querySelector("[data-recall-reveal]");
    if (revealButton) revealButton.disabled = !answerField.value.trim();
  });
}

function renderStudyLens(history) {
  if (!els.studyLens) return;
  const stats = studyStats(history);
  const learningState = readLearningState();
  const dueSummary = learningDueSummary(learningState);
  if (!history.length) {
    els.studyLens.innerHTML = `
      <article class="study-lens-card">
        <div class="study-lens-head">
          <b>学習レンズ</b>
          <span>0 / ${cards.length}</span>
        </div>
        <p class="study-lens-empty">保存した読みから、よく出るカード、未復習カード、次の学習候補をここに集めます。</p>
        ${renderDueReviewCue(dueSummary)}
        ${renderRecallPractice(stats, learningState)}
      </article>
    `;
    bindStudyLensActions();
    return;
  }

  const topCards = stats.topCards.length
    ? stats.topCards.map((entry) => `
        <li>
          <div class="study-card-action-row">
            <button class="study-card-button ${state.historyCardFilter === entry.card.id ? "is-active" : ""}" type="button" data-study-card-id="${escapeText(entry.card.id)}">
              <b>${escapeText(cardLabel(entry.card))}</b>
            </button>
            <button class="study-sheet-link ${state.studySheetOpen && state.studySheetCardId === entry.card.id ? "is-active" : ""}" type="button" data-study-sheet-card-id="${escapeText(entry.card.id)}">
              シート
            </button>
          </div>
          <span>${entry.count}回 / メモ${entry.noted}回</span>
        </li>
      `).join("")
    : "<li><span>まだカード履歴がありません</span></li>";
  const nextCards = stats.nextCards.length
    ? stats.nextCards.map((card) => `
        <span class="study-chip-pair">
          <button class="study-chip ${state.historyCardFilter === card.id ? "is-active" : ""}" type="button" data-study-card-id="${escapeText(card.id)}">
            ${escapeText(cardLabel(card))}
          </button>
          <button class="study-sheet-link ${state.studySheetOpen && state.studySheetCardId === card.id ? "is-active" : ""}" type="button" data-study-sheet-card-id="${escapeText(card.id)}">
            シート
          </button>
        </span>
      `).join("")
    : "<span class=\"study-chip\">大アルカナ一巡済み</span>";
  const focus = stats.recentFocus ? stats.recentFocus.card : null;

  els.studyLens.innerHTML = `
    <article class="study-lens-card">
      <div class="study-lens-head">
        <b>学習レンズ</b>
        <span>${stats.seenCount} / ${cards.length}</span>
      </div>
      <div class="study-meter" aria-label="大アルカナ学習範囲">
        <span style="--progress:${Math.round((stats.seenCount / cards.length) * 100)}%"></span>
      </div>
      <div class="study-stat-row">
        <span><b>${stats.readings}</b>保存</span>
        <span><b>${stats.notedCards}</b>メモ</span>
        <span><b>${stats.unseenCount}</b>未出</span>
        <span data-due-count><b>${dueSummary.due.length}</b>復習</span>
      </div>
      <div class="study-lens-grid">
        <section>
          <strong>よく出るカード</strong>
          <ol>${topCards}</ol>
        </section>
        <section>
          <strong>次の観測候補</strong>
          <div class="study-chip-row">${nextCards}</div>
        </section>
      </div>
      ${focus ? `
        <p class="study-focus-line">
          <button class="study-card-button focus-link ${state.historyCardFilter === focus.id ? "is-active" : ""}" type="button" data-study-card-id="${escapeText(focus.id)}">
            <b>${escapeText(cardLabel(focus))}</b>
          </button>
          <button class="study-sheet-link ${state.studySheetOpen && state.studySheetCardId === focus.id ? "is-active" : ""}" type="button" data-study-sheet-card-id="${escapeText(focus.id)}">
            シート
          </button>
          <span>${escapeText(focus.studyFocus)}</span>
        </p>
      ` : ""}
      ${renderDueReviewCue(dueSummary)}
      ${renderRecallPractice(stats, learningState)}
    </article>
  `;
  bindStudyLensActions();
}

function renderHistoryFilterBar(card, matchCount) {
  if (!card) return "";
  return `
    <div class="history-filter-bar" role="status">
      <span>
        <b>カード別復習</b>
        ${escapeText(cardLabel(card))} / ${matchCount}件
      </span>
      <button class="history-filter-clear" type="button" data-clear-history-filter>全履歴</button>
    </div>
  `;
}

function bindHistoryFilterClear() {
  els.historyFilterBar?.querySelector("[data-clear-history-filter]")?.addEventListener("click", () => {
    state.historyCardFilter = null;
    state.reviewedHistoryKey = null;
    state.inspectorTab = "history";
    renderHistory();
  });
}

function latestHistoryCopy(history) {
  const latest = history[0];
  return latest?.savedAt ? `最新 ${latest.savedAt}` : "未保存";
}

function latestLearningCopy(learningState) {
  const latest = learningState.attempts[0];
  if (!latest) return "未練習";
  const attemptedAt = latest.attemptedAt ? new Date(latest.attemptedAt) : null;
  const dateCopy = attemptedAt && !Number.isNaN(attemptedAt.getTime())
    ? attemptedAt.toLocaleString("ja-JP")
    : latest.attemptedAt;
  return `${latest.cardLabel || latest.cardId} / ${latest.confidence} / ${dateCopy}`;
}

function renderSettings(history = readHistory(), learningState = readLearningState()) {
  if (!els.settingsDialog) return;
  if (els.settingsDialog.hidden !== !state.settingsOpen) {
    els.settingsDialog.hidden = !state.settingsOpen;
  }
  if (els.settingsStatus) els.settingsStatus.textContent = state.settingsStatus;
  if (els.settingsHistoryCount) els.settingsHistoryCount.textContent = String(history.length);
  if (els.settingsHistoryUpdated) els.settingsHistoryUpdated.textContent = latestHistoryCopy(history);
  if (els.settingsLearningCount) els.settingsLearningCount.textContent = String(learningState.attempts.length);
  if (els.settingsLearningUpdated) els.settingsLearningUpdated.textContent = latestLearningCopy(learningState);
  if (els.settingsExportHistoryButton) els.settingsExportHistoryButton.disabled = history.length === 0;
  if (els.settingsClearHistoryButton) els.settingsClearHistoryButton.disabled = history.length === 0;
  if (els.exportLearningButton) els.exportLearningButton.disabled = learningState.attempts.length === 0;
  if (els.clearLearningButton) els.clearLearningButton.disabled = learningState.attempts.length === 0;
  if (els.settingsAppVersion) els.settingsAppVersion.textContent = appVersion;
  if (els.settingsLatestReleaseLink) els.settingsLatestReleaseLink.href = latestReleaseUrl;
  if (els.settingsProjectLink) els.settingsProjectLink.href = projectRepositoryUrl;
  if (els.settingsSecurityLink) els.settingsSecurityLink.href = securityPolicyUrl;
  if (els.settingsLicenseLink) els.settingsLicenseLink.href = assetLicenseUrl;
  if (els.settingsLocalKeys) {
    els.settingsLocalKeys.textContent = `${historyKey} / ${learningKey} / ${settingsKey}`;
  }
  applySettings();
}

function openSettings() {
  state.settingsOpen = true;
  renderSettings();
  window.requestAnimationFrame(() => els.closeSettingsButton?.focus());
}

function closeSettings() {
  state.settingsOpen = false;
  renderSettings();
  els.openSettingsButton?.focus();
}

function selectHistoryCardFilter(cardId) {
  const card = getCard(cardId);
  if (!card) return;
  const history = readHistory();
  state.historyCardFilter = card.id;
  const firstMatch = history.find((item) => historyItemHasCard(item, card.id));
  state.reviewedHistoryKey = firstMatch ? readingIdentity(firstMatch) : null;
  state.inspectorTab = "history";
  renderHistory();
}

function renderHistory() {
  const history = readHistory();
  const learningState = readLearningState();
  els.statSaved.textContent = String(history.length);
  els.exportHistoryButton.disabled = history.length === 0;
  els.clearHistoryButton.disabled = history.length === 0;
  renderSettings(history, learningState);
  renderStudyLens(history);
  els.historySection?.classList.toggle("is-empty-history", !historyReadFailed && history.length === 0);

  let activeFilterCard = state.historyCardFilter
    ? getCard(state.historyCardFilter)
    : null;
  if (state.historyCardFilter && !activeFilterCard) {
    state.historyCardFilter = null;
    activeFilterCard = null;
  }
  const visibleRows = historyRowsForFilter(history, activeFilterCard?.id || null);
  const visibleHistory = visibleRows.map(({ item }) => item);
  if (state.reviewedHistoryKey && !visibleHistory.some((item) => readingIdentity(item) === state.reviewedHistoryKey)) {
    state.reviewedHistoryKey = null;
  }
  if (els.historyFilterBar) {
    els.historyFilterBar.innerHTML = renderHistoryFilterBar(activeFilterCard, visibleRows.length);
    bindHistoryFilterClear();
  }
  els.historySection?.classList.toggle("is-filtered", Boolean(activeFilterCard));
  els.historySection?.classList.toggle("is-recall-active", Boolean(state.recallPractice.cardId));
  els.studyPanel?.classList.toggle("is-filtered", Boolean(activeFilterCard));
  els.studyPanel?.classList.toggle("is-recall-active", Boolean(state.recallPractice.cardId));
  renderInspectorTabs();

  if (historyReadFailed) {
    if (els.historyFilterBar) els.historyFilterBar.innerHTML = "";
    els.historySection?.classList.remove("is-filtered");
    els.historySection?.classList.remove("is-recall-active");
    els.studyPanel?.classList.remove("is-filtered");
    els.historyList.innerHTML = `
      <p class="empty error-state">
        履歴データを読めません。書き出し済みJSONがある場合は「読み込み」から復元してください。
      </p>`;
    renderHistoryReview(history);
    return;
  }
  if (!history.length) {
    state.historyCardFilter = null;
    if (els.historyFilterBar) els.historyFilterBar.innerHTML = "";
    els.historySection?.classList.remove("is-filtered");
    els.historySection?.classList.toggle("is-recall-active", Boolean(state.recallPractice.cardId));
    els.studyPanel?.classList.remove("is-filtered");
    els.historyList.innerHTML = `<p class="empty">保存済みのリーディングはありません。</p>`;
    renderHistoryReview(history);
    return;
  }

  if (!visibleRows.length) {
    els.historyList.innerHTML = `
      <p class="empty">このカードを含む保存済みリーディングはまだありません。次の観測候補として引いた時に保存すると、ここに集まります。</p>
    `;
    renderHistoryReview(visibleHistory);
    return;
  }

  els.historyList.innerHTML = `
    ${visibleRows.map(({ item, index }) => `
    <div class="history-row ${readingIdentity(item) === state.reviewedHistoryKey ? "is-active" : ""}" data-history-card-ids="${escapeText((Array.isArray(item.cards) ? item.cards : []).map((entry) => entry.cardId).join(" "))}">
      <button class="history-item" type="button" data-history-index="${index}" aria-label="${escapeText(`${item.spreadLabel} ${item.savedAt} を復元`)}">
        <b>${escapeText(item.spreadLabel)} / ${escapeText(item.savedAt)}</b>
        <span>${escapeText(item.summary)}${item.question ? ` / ${escapeText(item.question)}` : ""}</span>
      </button>
      <button class="history-delete" type="button" data-history-delete-index="${index}" aria-label="${escapeText(`${item.spreadLabel} ${item.savedAt} を削除`)}">削除</button>
    </div>
  `).join("")}
  `;

  els.historyList.querySelectorAll("[data-history-index]").forEach((button) => {
    button.addEventListener("click", () => restoreHistory(Number(button.dataset.historyIndex)));
  });
  els.historyList.querySelectorAll("[data-history-delete-index]").forEach((button) => {
    button.addEventListener("click", () => deleteHistory(Number(button.dataset.historyDeleteIndex)));
  });
  renderHistoryReview(visibleHistory);
}

function renderStatus() {
  const spread = currentSpread();
  els.spreadTitle.textContent = spread.label;
  els.spreadDescription.textContent = spread.description;
  els.statCards.textContent = String(spread.slots.length);
  els.statRevealed.textContent = String(state.revealedCount);
  els.revealButton.disabled = !state.drawn.length || state.revealedCount >= state.drawn.length;
  els.saveReadingButton.disabled = state.revealedCount === 0;
  const total = state.drawn.length || spread.slots.length;
  const status = state.revealedCount
    ? `${state.revealedCount} / ${total} opened`
    : state.drawn.length
      ? "Cards placed face down"
      : "Ready";
  els.statusLine.textContent = state.restoredAt ? `${status} / restored ${state.restoredAt}` : status;
}

function render() {
  renderSpreadControls();
  renderBoard();
  renderProgress();
  renderInspector();
  renderHistory();
  renderStatus();
  renderInspectorTabs();
}

function updateCurrentNote() {
  const selected = selectedSlot();
  if (!selected) return;
  state.notes[slotNoteKey(selected.slot, selected.index)] = els.noteInput.value;
  els.noteStatus.textContent = els.noteInput.value.trim() ? "記録中" : "自分の読みを記録";
  renderInspector();
}

function saveReading() {
  const spread = currentSpread();
  if (!state.revealedCount) return;
  const revealedCards = state.drawn.slice(0, state.revealedCount).map((card, index) => {
    const slot = spread.slots[index];
    return {
      cardId: card.id,
      number: card.number,
      displayNumber: card.displayNumber,
      japaneseName: card.japaneseName,
      englishName: card.englishName,
      reversed: card.reversed,
      slotKey: slot.key,
      slotLabel: slot.label,
      note: state.notes[slotNoteKey(slot, index)] || ""
    };
  });
  const item = {
    savedAt: new Date().toLocaleString("ja-JP"),
    question: els.questionInput.value.trim(),
    spreadId: spread.id,
    spreadLabel: spread.label,
    revealedCount: state.revealedCount,
    notes: state.notes,
    cards: revealedCards,
    summary: revealedCards
      .map((card) => `${card.slotLabel}:${card.displayNumber || card.number} ${card.japaneseName}${card.reversed ? "逆" : "正"}`)
      .join(" / ")
  };
  const history = readHistory();
  history.unshift(item);
  if (!writeHistory(history)) {
    els.noteStatus.textContent = "履歴を保存できません。空き容量またはブラウザ設定を確認してください。";
    renderHistory();
    renderStatus();
    return;
  }
  state.reviewedHistoryKey = readingIdentity(item);
  state.afterSaveKey = state.reviewedHistoryKey;
  state.inspectorTab = "history";
  els.noteStatus.textContent = "保存しました";
  renderHistory();
  renderStatus();
}

function restoreHistory(index) {
  const item = readHistory()[index];
  if (!item) return;
  const spread = getSpread(item.spreadId);
  if (!spread) return;
  state.spreadId = spread.id;
  state.drawn = item.cards.map((entry) => {
    const card = getCard(entry.cardId);
    return card ? { ...card, reversed: entry.reversed } : null;
  }).filter(Boolean);
  state.revealedCount = state.drawn.length;
  state.selectedIndex = state.drawn.length ? 0 : -1;
  state.notes = normalizeReadingNotes(item, spread);
  state.restoredAt = item.savedAt;
  state.reviewedHistoryKey = readingIdentity(item);
  state.afterSaveKey = null;
  state.studySheetOpen = false;
  state.studySheetCardId = null;
  state.inspectorTab = "card";
  state.slotDrill = blankSlotDrill();
  els.questionInput.value = item.question || "";
  els.noteStatus.textContent = "履歴を復元";
  render();
}

function deleteHistory(index) {
  const history = readHistory();
  const item = history[index];
  if (!item) return;
  const confirmed = window.confirm("この履歴を削除します。先に書き出していない場合は戻せません。");
  if (!confirmed) return;
  const deletedKey = readingIdentity(item);
  const nextHistory = history.filter((_, itemIndex) => itemIndex !== index);
  if (!writeHistory(nextHistory)) {
    els.noteStatus.textContent = "履歴を削除できません。ブラウザの保存設定を確認してください。";
    return;
  }
  if (state.reviewedHistoryKey === deletedKey) state.reviewedHistoryKey = null;
  if (state.afterSaveKey === deletedKey) state.afterSaveKey = null;
  if (state.restoredAt === item.savedAt) state.restoredAt = null;
  state.inspectorTab = "history";
  els.noteStatus.textContent = "履歴を削除しました";
  renderHistory();
  renderStatus();
}

function clearHistory() {
  const history = readHistory();
  if (!history.length) return;
  const confirmed = window.confirm("すべての履歴を削除します。先に書き出していない場合は戻せません。");
  if (!confirmed) return;
  if (!writeHistory([])) {
    els.noteStatus.textContent = "履歴を全消去できません。ブラウザの保存設定を確認してください。";
    state.settingsStatus = els.noteStatus.textContent;
    renderSettings();
    return;
  }
  state.reviewedHistoryKey = null;
  state.afterSaveKey = null;
  state.restoredAt = null;
  state.inspectorTab = "history";
  els.noteStatus.textContent = "履歴を全消去しました";
  state.settingsStatus = els.noteStatus.textContent;
  render();
}

function exportHistory() {
  const payload = {
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    history: readHistory()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `onoko-arcana-readings-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  state.settingsStatus = "履歴JSONを書き出しました";
  renderSettings();
}

async function importHistoryFile(file) {
  if (!file) return;
  try {
    const text = await file.text();
    let payload;
    try {
      payload = JSON.parse(text);
    } catch {
      throw new Error("履歴JSONを読めませんでした。");
    }
    const imported = importedHistoryFromPayload(payload);
    if (!imported.length) {
      els.noteStatus.textContent = "読み込む履歴がありません";
      state.settingsStatus = els.noteStatus.textContent;
      renderSettings();
      return;
    }
    const result = mergeImportedHistory(imported);
    state.inspectorTab = "history";
    renderHistory();
    renderStatus();
    if (result.storageFailed) {
      els.noteStatus.textContent = "履歴を読み込めません。空き容量またはブラウザ設定を確認してください。";
      state.settingsStatus = els.noteStatus.textContent;
      renderSettings();
      return;
    }
    if (!result.added) {
      els.noteStatus.textContent = result.skippedInvalid
        ? `読み込みなし / 無効 ${result.skippedInvalid}`
        : "読み込み済みの履歴です";
      state.settingsStatus = els.noteStatus.textContent;
      renderSettings();
      return;
    }
    const skipped = result.skippedDuplicate || result.skippedInvalid
      ? ` / 除外 ${result.skippedDuplicate + result.skippedInvalid}`
      : "";
    els.noteStatus.textContent = `履歴 ${result.added} 件を読み込み${skipped}`;
    state.settingsStatus = els.noteStatus.textContent;
    renderSettings();
  } catch (error) {
    els.noteStatus.textContent = error instanceof Error ? error.message : "履歴を読み込めませんでした";
    state.settingsStatus = els.noteStatus.textContent;
    renderSettings();
  } finally {
    els.importHistoryInput.value = "";
  }
}

function exportLearning() {
  const learningState = readLearningState();
  if (!learningState.attempts.length) return;
  const payload = {
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    learning: learningState
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `onoko-arcana-learning-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  state.settingsStatus = "学習JSONを書き出しました";
  renderSettings();
}

async function importLearningFile(file) {
  if (!file) return;
  try {
    const text = await file.text();
    let payload;
    try {
      payload = JSON.parse(text);
    } catch {
      throw new Error("学習JSONを読めませんでした。");
    }
    const imported = importedLearningFromPayload(payload);
    if (!imported.attempts.length) {
      state.settingsStatus = imported.skippedInvalid
        ? `学習の読み込みなし / 無効 ${imported.skippedInvalid}`
        : "読み込む学習データがありません";
      renderSettings();
      return;
    }
    const result = mergeImportedLearning(imported);
    renderHistory();
    if (result.storageFailed) {
      state.settingsStatus = "学習データを読み込めません。空き容量またはブラウザ設定を確認してください。";
      renderSettings();
      return;
    }
    if (!result.added) {
      state.settingsStatus = result.skippedInvalid
        ? `読み込みなし / 無効 ${result.skippedInvalid}`
        : "読み込み済みの学習データです";
      renderSettings();
      return;
    }
    const skipped = result.skippedDuplicate || result.skippedInvalid
      ? ` / 除外 ${result.skippedDuplicate + result.skippedInvalid}`
      : "";
    state.settingsStatus = `学習 ${result.added} 件を読み込み${skipped}`;
    renderSettings();
  } catch (error) {
    state.settingsStatus = error instanceof Error ? error.message : "学習データを読み込めませんでした";
    renderSettings();
  } finally {
    if (els.importLearningInput) els.importLearningInput.value = "";
  }
}

function clearLearning() {
  const learningState = readLearningState();
  if (!learningState.attempts.length) return;
  const confirmed = window.confirm("すべての学習データを消去します。履歴は残ります。先に書き出していない場合は戻せません。");
  if (!confirmed) return;
  try {
    localStorage.removeItem(learningKey);
    learningReadFailed = false;
    state.recallPractice = {
      cardId: null,
      orientation: "upright",
      answer: "",
      revealed: false,
      savedConfidence: null,
      status: ""
    };
    state.slotDrill = blankSlotDrill();
    state.settingsStatus = "学習データを消去しました";
    renderHistory();
  } catch {
    state.settingsStatus = "学習データを消去できません。ブラウザの保存設定を確認してください。";
    renderSettings();
  }
}

function updateCompactLearningSetting() {
  state.settings.compactLearningPanel = els.compactLearningToggle?.checked === true;
  if (!writeSettings(state.settings)) {
    state.settingsStatus = "表示設定を保存できません。ブラウザの保存設定を確認してください。";
    renderSettings();
    return;
  }
  state.settingsStatus = state.settings.compactLearningPanel
    ? "学習レンズをコンパクト表示にしました"
    : "学習レンズを通常表示にしました";
  applySettings();
  renderSettings();
}

els.drawButton.addEventListener("click", drawSpread);
els.revealButton.addEventListener("click", revealNext);
els.resetButton.addEventListener("click", resetTable);
els.saveReadingButton.addEventListener("click", saveReading);
els.openSettingsButton?.addEventListener("click", openSettings);
els.closeSettingsButton?.addEventListener("click", closeSettings);
els.settingsDialog?.querySelector("[data-close-settings]")?.addEventListener("click", closeSettings);
els.settingsImportHistoryButton?.addEventListener("click", () => els.importHistoryInput.click());
els.settingsExportHistoryButton?.addEventListener("click", exportHistory);
els.settingsClearHistoryButton?.addEventListener("click", clearHistory);
els.importHistoryButton.addEventListener("click", () => els.importHistoryInput.click());
els.importHistoryInput.addEventListener("change", () => importHistoryFile(els.importHistoryInput.files[0]));
els.exportHistoryButton.addEventListener("click", exportHistory);
els.clearHistoryButton.addEventListener("click", clearHistory);
els.importLearningButton?.addEventListener("click", () => els.importLearningInput?.click());
els.importLearningInput?.addEventListener("change", () => importLearningFile(els.importLearningInput.files[0]));
els.exportLearningButton?.addEventListener("click", exportLearning);
els.clearLearningButton?.addEventListener("click", clearLearning);
els.compactLearningToggle?.addEventListener("change", updateCompactLearningSetting);
els.inspectorTabs.forEach((button) => {
  button.addEventListener("click", () => setInspectorTab(button.dataset.inspectorTab));
  button.addEventListener("keydown", (event) => {
    if (event.key === "ArrowRight") {
      event.preventDefault();
      moveInspectorTab(button.dataset.inspectorTab, 1);
      return;
    }
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      moveInspectorTab(button.dataset.inspectorTab, -1);
      return;
    }
    if (event.key === "Home") {
      event.preventDefault();
      setInspectorTab(inspectorTabIds[0], { focus: true });
      return;
    }
    if (event.key === "End") {
      event.preventDefault();
      setInspectorTab(inspectorTabIds[inspectorTabIds.length - 1], { focus: true });
    }
  });
});
els.noteInput.addEventListener("input", updateCurrentNote);
els.toggleStudySheetButton?.addEventListener("click", toggleStudySheet);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.settingsOpen) closeSettings();
});

state.settings = readSettings();
applySettings();
render();
})();

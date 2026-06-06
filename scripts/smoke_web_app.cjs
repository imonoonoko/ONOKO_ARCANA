const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const Module = require("node:module");

const ROOT = path.resolve(__dirname, "..");
const WEB_NODE_MODULES = path.join(ROOT, "web-app", "node_modules");
process.env.NODE_PATH = [process.env.NODE_PATH, WEB_NODE_MODULES].filter(Boolean).join(path.delimiter);
Module._initPaths();

const { chromium } = require("playwright");

const APP = path.join(ROOT, "web-app", "index.html");
const REPORTS = path.join(ROOT, "reports");
const FIXTURES = path.join(ROOT, "tests", "fixtures", "history");
const HISTORY_KEY = "onoko-arcana:desktop:history:v1";
const LEARNING_KEY = "onoko-arcana:desktop:learning:v1";
const SETTINGS_KEY = "onoko-arcana:desktop:settings:v1";

function stamp() {
  const now = new Date();
  const pad = (value) => String(value).padStart(2, "0");
  return [
    now.getFullYear(),
    pad(now.getMonth() + 1),
    pad(now.getDate()),
    "-",
    pad(now.getHours()),
    pad(now.getMinutes()),
    pad(now.getSeconds())
  ].join("");
}

async function openPage(browser, viewport) {
  const page = await browser.newPage({
    ...viewport,
    acceptDownloads: true
  });
  const consoleErrors = [];
  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  await page.goto(pathToFileURL(APP).href, { waitUntil: "domcontentloaded" });
  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.evaluate((key) => localStorage.removeItem(key), LEARNING_KEY);
  await page.evaluate((key) => localStorage.removeItem(key), SETTINGS_KEY);
  return { page, consoleErrors };
}

async function reveal(page, count) {
  for (let index = 0; index < count; index += 1) {
    await page.click("#revealButton");
  }
}

async function openInspectorTab(page, tab) {
  await page.click(`[data-inspector-tab="${tab}"]`);
  await page.waitForSelector(`[data-inspector-panel="${tab}"]:not([hidden])`);
}

async function runDesktop(browser, id) {
  const screenshot = path.join(REPORTS, `onoko-arcana-web-app-celtic-${id}.png`);
  const firstLaunchScreenshot = path.join(REPORTS, `onoko-arcana-first-launch-${id}.png`);
  const settingsScreenshot = path.join(REPORTS, `onoko-arcana-settings-${id}.png`);
  const exportPath = path.join(REPORTS, `onoko-arcana-history-export-${id}.json`);
  const learningExportPath = path.join(REPORTS, `onoko-arcana-learning-export-${id}.json`);
  const invalidImportPath = path.join(FIXTURES, "invalid-json.json");
  const cardNoteOnlyImportPath = path.join(FIXTURES, "history-card-note-only-v1.json");
  const { page, consoleErrors } = await openPage(browser, {
    viewport: { width: 1424, height: 881 },
    deviceScaleFactor: 1
  });

  await page.waitForSelector("[data-first-launch-guide]");
  await openInspectorTab(page, "history");
  await page.screenshot({ path: firstLaunchScreenshot, fullPage: true });
  const firstLaunchState = await page.evaluate(() => ({
    firstLaunchVisible: Boolean(document.querySelector("[data-first-launch-guide]")),
    tabCount: document.querySelectorAll("[data-inspector-tab]").length,
    activeTab: document.querySelector("[data-inspector-tab][aria-selected='true']")?.dataset.inspectorTab,
    steps: document.querySelectorAll(".first-launch-steps li").length,
    text: document.querySelector("[data-first-launch-guide]")?.textContent,
    historyText: document.querySelector("#historyReview")?.textContent,
    boardCards: document.querySelectorAll(".arcana-card").length
  }));
  await page.click("[data-first-launch-focus-question]");
  const firstLaunchFocusState = await page.evaluate(() => ({
    activeId: document.activeElement?.id,
    spreadTitle: document.querySelector("#spreadTitle")?.textContent
  }));

  const spreadIds = [
    "one_card",
    "three_card_past_present_future",
    "five_card_cross",
    "seven_card_horseshoe",
    "celtic_cross",
    "relationship_line"
  ];
  for (const spreadId of spreadIds) {
    await page.click(`[data-spread-id="${spreadId}"]`);
  }

  await page.fill("#questionInput", "完成へ進めるために、今見るべき関係性は何か");
  await page.click('[data-spread-id="relationship_line"]');
  await page.click("#drawButton");
  await reveal(page, 6);
  await page.fill("#noteInput", "自分と相手、接点、課題、助言、可能性を同じ卓で読む。");
  await page.click("#saveReadingButton");

  await page.click('[data-spread-id="celtic_cross"]');
  await page.fill("#questionInput", "ONOKOアプリの完成へ向けて、今どの構造を採用するべきか");
  await page.click("#drawButton");
  await reveal(page, 10);
  await page.fill("#noteInput", "2D占い卓を本体として完成させ、UE化は現行ロードマップでは見送る。");
  await openInspectorTab(page, "card");
  const cardStudySheetState = await page.evaluate(() => {
    const panel = document.querySelector("#cardStudySheetPanel");
    const sheet = panel?.querySelector("[data-study-sheet-open]");
    return {
      open: Boolean(sheet),
      source: sheet?.dataset.studySheetSource,
      cardId: sheet?.dataset.studySheetCardId,
      text: panel?.textContent,
      symbols: panel?.querySelectorAll(".symbol-chip").length,
      cautions: panel?.querySelectorAll(".study-caution-list li").length,
      reflections: panel?.querySelectorAll(".study-reflection-list li").length,
      slotDrill: Boolean(panel?.querySelector("[data-slot-drill].is-active")),
      noteValue: document.querySelector("#noteInput")?.value,
      guideButtonExists: Boolean(document.querySelector("#toggleGuideButton")),
      guidePanelExists: Boolean(document.querySelector("#guidePanel"))
    };
  });
  await page.click("#saveReadingButton");
  await page.waitForTimeout(250);
  await page.screenshot({ path: screenshot, fullPage: true });
  await openInspectorTab(page, "study");
  await page.click("#toggleStudySheetButton");
  await page.waitForSelector("#studySheetPanel [data-study-sheet-open]");
  const selectedStudySheetState = await page.evaluate(() => ({
    open: Boolean(document.querySelector("#studySheetPanel [data-study-sheet-open]")),
    cardId: document.querySelector("#studySheetPanel [data-study-sheet-open]")?.dataset.studySheetCardId,
    text: document.querySelector("#studySheetPanel")?.textContent,
    symbols: document.querySelectorAll("#studySheetPanel .symbol-chip").length,
    cautions: document.querySelectorAll("#studySheetPanel .study-caution-list li").length,
    reflections: document.querySelectorAll("#studySheetPanel .study-reflection-list li").length,
    recallButton: Boolean(document.querySelector("#studySheetPanel [data-study-sheet-recall]")),
    filterButton: Boolean(document.querySelector("#studySheetPanel [data-study-sheet-filter]")),
    slotDrill: Boolean(document.querySelector("#studySheetPanel [data-slot-drill].is-active")),
    slotDrillText: document.querySelector("#studySheetPanel [data-slot-drill]")?.textContent,
    slotDrillRevealDisabled: document.querySelector("#studySheetPanel [data-slot-drill-reveal]")?.disabled,
    expanded: document.querySelector("#toggleStudySheetButton")?.getAttribute("aria-expanded")
  }));

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    spreadChoices: document.querySelectorAll("[data-spread-id]").length,
    revealed: document.querySelector("#statRevealed")?.textContent,
    saved: document.querySelector("#statSaved")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    selected: document.querySelector("#selectedCard h2")?.textContent,
    cardStudySheets: document.querySelectorAll("#cardStudySheetPanel [data-study-sheet-open]").length,
    guideButtonExists: Boolean(document.querySelector("#toggleGuideButton")),
    guidePanelExists: Boolean(document.querySelector("#guidePanel")),
    historyItems: document.querySelectorAll(".history-item").length,
    historyDeleteButtons: document.querySelectorAll(".history-delete").length,
    historyReviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
    studyLensText: document.querySelector("#studyLens")?.textContent,
    dueCount: document.querySelector("[data-due-count]")?.textContent,
    afterSaveActions: document.querySelectorAll("[data-after-save-actions] button").length,
    afterSaveText: document.querySelector("[data-after-save-actions]")?.textContent,
    status: document.querySelector("#statusLine")?.textContent,
    importExists: Boolean(document.querySelector("#importHistoryButton")),
    tabCount: document.querySelectorAll("[data-inspector-tab]").length,
    activeTab: document.querySelector("[data-inspector-tab][aria-selected='true']")?.dataset.inspectorTab,
    activePanel: document.querySelector("[data-inspector-panel]:not([hidden])")?.dataset.inspectorPanel,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled,
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    viewport: window.innerWidth,
    viewportHeight: window.innerHeight,
    sidePanelFits: document.querySelector(".side-panel")?.scrollHeight <= document.querySelector(".side-panel")?.clientHeight + 1,
    inspectorFits: document.querySelector(".inspector")?.scrollHeight <= document.querySelector(".inspector")?.clientHeight + 1
  }));

  const slotDrillBeforeAnswerState = await page.evaluate(() => ({
    text: document.querySelector("#studySheetPanel [data-slot-drill]")?.textContent,
    revealDisabled: document.querySelector("#studySheetPanel [data-slot-drill-reveal]")?.disabled,
    learningRaw: localStorage.getItem("onoko-arcana:desktop:learning:v1")
  }));
  await page.fill("#studySlotDrillAnswer", "この位置では、完成前の課題として読みを絞り込む。");
  await page.waitForFunction(() => !document.querySelector("#studySheetPanel [data-slot-drill-reveal]")?.disabled);
  await page.click("#studySheetPanel [data-slot-drill-reveal]");
  await page.waitForSelector("#studySheetPanel [data-slot-drill-guide]");
  const slotDrillRevealState = await page.evaluate(() => ({
    text: document.querySelector("#studySheetPanel [data-slot-drill]")?.textContent,
    guideText: document.querySelector("#studySheetPanel [data-slot-drill-guide]")?.textContent,
    confidenceButtons: document.querySelectorAll("#studySheetPanel [data-slot-drill-confidence]").length
  }));
  await page.click("#studySheetPanel [data-slot-drill-confidence='hard']");
  await page.waitForFunction(() => {
    const raw = localStorage.getItem("onoko-arcana:desktop:learning:v1");
    if (!raw) return false;
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed.attempts) && parsed.attempts.length === 1 && parsed.attempts[0].promptType === "slot_interpretation";
  });
  const slotDrillSavedState = await page.evaluate(() => {
    const learning = JSON.parse(localStorage.getItem("onoko-arcana:desktop:learning:v1"));
    return {
      text: document.querySelector("#studySheetPanel [data-slot-drill]")?.textContent,
      attempts: learning.attempts.length,
      latest: learning.attempts[0]
    };
  });

  const downloadPromise = page.waitForEvent("download");
  await openInspectorTab(page, "history");
  await page.click("#exportHistoryButton");
  const download = await downloadPromise;
  await download.saveAs(exportPath);

  await page.evaluate((key) => localStorage.setItem(key, "{ broken json"), HISTORY_KEY);
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForFunction(() => document.querySelector("#historyList")?.textContent.includes("履歴データを読めません"));
  const corruptStorageState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyText: document.querySelector("#historyList")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled
  }));

  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForSelector("#importHistoryInput");
  await page.setInputFiles("#importHistoryInput", exportPath);
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "2");
  const importState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    studyLensText: document.querySelector("#studyLens")?.textContent,
    noteStatus: document.querySelector("#noteStatus")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled
  }));

  await page.setInputFiles("#importHistoryInput", exportPath);
  await page.waitForFunction(() => document.querySelector("#noteStatus")?.textContent.includes("読み込み済み"));
  const duplicateImportState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    noteStatus: document.querySelector("#noteStatus")?.textContent
  }));

  await page.setInputFiles("#importHistoryInput", invalidImportPath);
  await page.waitForFunction(() => document.querySelector("#noteStatus")?.textContent.includes("読めません"));
  const invalidImportState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    noteStatus: document.querySelector("#noteStatus")?.textContent
  }));

  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.setInputFiles("#importHistoryInput", cardNoteOnlyImportPath);
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "1");
  await page.click('[data-history-index="0"]');
  await page.waitForFunction(() => document.querySelector("#statRevealed")?.textContent === "1");
  const cardNoteOnlyRestoreState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    restoredNote: document.querySelector("#noteInput")?.value,
    reviewText: document.querySelector("#historyReview")?.textContent
  }));

  await page.setInputFiles("#importHistoryInput", exportPath);
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "3");

  await openInspectorTab(page, "study");
  await page.waitForSelector("[data-study-card-id]");
  const firstStudyCard = await page.evaluate(() => {
    const button = document.querySelector("[data-study-card-id]");
    return {
      cardId: button?.dataset.studyCardId || "",
      label: button?.textContent?.replace(/\s+/g, " ").trim() || "",
      buttons: document.querySelectorAll("[data-study-card-id]").length
    };
  });
  await page.click(`[data-study-card-id="${firstStudyCard.cardId}"]`);
  await page.waitForSelector(".history-filter-bar");
  const studyFilterState = await page.evaluate((cardId) => {
    const rows = Array.from(document.querySelectorAll(".history-row"));
    return {
      cardId,
      filterText: document.querySelector(".history-filter-bar")?.textContent,
      historyItems: document.querySelectorAll(".history-item").length,
      clearExists: Boolean(document.querySelector("[data-clear-history-filter]")),
      activeStudyButtons: document.querySelectorAll(".study-card-button.is-active, .study-chip.is-active").length,
      reviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
      compareBlocks: document.querySelectorAll(".review-learning-compare").length,
      reviewText: document.querySelector("#historyReview")?.textContent,
      allRowsMatch: rows.length > 0 && rows.every((row) => String(row.dataset.historyCardIds || "").split(/\s+/).includes(cardId))
    };
  }, firstStudyCard.cardId);
  await page.click("[data-clear-history-filter]");
  await page.waitForFunction(() => !document.querySelector(".history-filter-bar"));
  const studyFilterClearState = await page.evaluate(() => ({
    historyItems: document.querySelectorAll(".history-item").length,
    filterVisible: Boolean(document.querySelector(".history-filter-bar"))
  }));

  await openInspectorTab(page, "study");
  const inactiveStudySheetCard = await page.evaluate(({ selectedCardId, filterCardId }) => {
    const buttons = Array.from(document.querySelectorAll("#studyLens [data-study-sheet-card-id]"));
    const excluded = new Set([selectedCardId, filterCardId].filter(Boolean));
    const button = buttons.find((candidate) => candidate.dataset.studySheetCardId && !excluded.has(candidate.dataset.studySheetCardId));
    return {
      cardId: button?.dataset.studySheetCardId || "",
      buttons: buttons.length
    };
  }, { selectedCardId: selectedStudySheetState.cardId, filterCardId: firstStudyCard.cardId });
  if (!inactiveStudySheetCard.cardId) {
    throw new Error("study lens sheet card candidate should exist");
  }
  await page.locator(`#studyLens [data-study-sheet-card-id="${inactiveStudySheetCard.cardId}"]`).first().click();
  await page.waitForSelector(`#studySheetPanel [data-study-sheet-open][data-study-sheet-card-id="${inactiveStudySheetCard.cardId}"]`);
  const studyLensSheetState = await page.evaluate((cardId) => ({
    cardId,
    openCardId: document.querySelector("#studySheetPanel [data-study-sheet-open]")?.dataset.studySheetCardId,
    text: document.querySelector("#studySheetPanel")?.textContent,
    activeSheetLinks: document.querySelectorAll(".study-sheet-link.is-active").length,
    slotDrillText: document.querySelector("#studySheetPanel [data-slot-drill]")?.textContent,
    slotDrillDisabled: Boolean(document.querySelector("#studySheetPanel [data-slot-drill].is-disabled")),
    actions: document.querySelectorAll("#studySheetPanel .study-sheet-actions button").length
  }), inactiveStudySheetCard.cardId);

  await page.waitForSelector("[data-recall-start]");
  const recallStartState = await page.evaluate(() => ({
    text: document.querySelector("[data-recall-practice]")?.textContent,
    starts: document.querySelectorAll("[data-recall-start]").length
  }));
  await page.click("[data-recall-start]");
  await page.waitForSelector("#recallAnswer");
  const recallBeforeAnswerState = await page.evaluate(() => ({
    cardText: document.querySelector("[data-recall-practice]")?.textContent,
    revealDisabled: document.querySelector("[data-recall-reveal]")?.disabled,
    learningRaw: localStorage.getItem("onoko-arcana:desktop:learning:v1")
  }));
  await page.fill("#recallAnswer", "内省、探求、灯りを探す。");
  await page.waitForFunction(() => !document.querySelector("[data-recall-reveal]")?.disabled);
  await page.click("[data-recall-orientation='reversed']");
  await page.fill("#recallAnswer", "孤立、閉じこもり、迷子。");
  await page.click("[data-recall-reveal]");
  await page.waitForSelector("[data-recall-guide]");
  const recallRevealState = await page.evaluate(() => ({
    text: document.querySelector("[data-recall-practice]")?.textContent,
    guideText: document.querySelector("[data-recall-guide]")?.textContent,
    confidenceButtons: document.querySelectorAll("[data-recall-confidence]").length
  }));
  await page.click("[data-recall-confidence='ok']");
  await page.waitForFunction(() => {
    const raw = localStorage.getItem("onoko-arcana:desktop:learning:v1");
    if (!raw) return false;
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed.attempts) && parsed.attempts.length === 2 && parsed.attempts[0].confidence === "ok";
  });
  const recallSavedState = await page.evaluate(() => {
    const learning = JSON.parse(localStorage.getItem("onoko-arcana:desktop:learning:v1"));
    return {
      text: document.querySelector("[data-recall-practice]")?.textContent,
      attempts: learning.attempts.length,
      latest: learning.attempts[0]
    };
  });

  await openInspectorTab(page, "history");
  await page.click("#openSettingsButton");
  await page.waitForSelector("#settingsDialog:not([hidden])");
  await page.screenshot({ path: settingsScreenshot, fullPage: true });
  const settingsOpenState = await page.evaluate(() => ({
    dialogVisible: !document.querySelector("#settingsDialog")?.hidden,
    title: document.querySelector("#settingsTitle")?.textContent,
    historyCount: document.querySelector("#settingsHistoryCount")?.textContent,
    learningCount: document.querySelector("#settingsLearningCount")?.textContent,
    learningUpdated: document.querySelector("#settingsLearningUpdated")?.textContent,
    historyExportDisabled: document.querySelector("#settingsExportHistoryButton")?.disabled,
    learningExportDisabled: document.querySelector("#exportLearningButton")?.disabled,
    compactChecked: document.querySelector("#compactLearningToggle")?.checked,
    version: document.querySelector("#settingsAppVersion")?.textContent,
    releaseWarning: document.querySelector("#settingsReleaseWarning")?.textContent,
    backupCue: document.querySelector("#settingsBackupCue")?.textContent,
    latestReleaseHref: document.querySelector("#settingsLatestReleaseLink")?.href,
    projectHref: document.querySelector("#settingsProjectLink")?.href,
    securityHref: document.querySelector("#settingsSecurityLink")?.href,
    licenseHref: document.querySelector("#settingsLicenseLink")?.href,
    licenseCue: document.querySelector("#settingsLicenseCue")?.textContent,
    localKeys: document.querySelector("#settingsLocalKeys")?.textContent
  }));

  const learningDownloadPromise = page.waitForEvent("download");
  await page.click("#exportLearningButton");
  const learningDownload = await learningDownloadPromise;
  await learningDownload.saveAs(learningExportPath);

  await page.check("#compactLearningToggle");
  const compactSettingState = await page.evaluate(() => ({
    bodyCompact: document.body.classList.contains("is-compact-learning"),
    settingsRaw: localStorage.getItem("onoko-arcana:desktop:settings:v1"),
    status: document.querySelector("#settingsStatus")?.textContent
  }));

  const clearLearningDialogPromise = page.waitForEvent("dialog").then((dialog) => dialog.accept());
  await page.click("#clearLearningButton");
  await clearLearningDialogPromise;
  await page.waitForFunction(() => document.querySelector("#settingsLearningCount")?.textContent === "0");
  const learningClearState = await page.evaluate(() => ({
    learningRaw: localStorage.getItem("onoko-arcana:desktop:learning:v1"),
    learningCount: document.querySelector("#settingsLearningCount")?.textContent,
    exportDisabled: document.querySelector("#exportLearningButton")?.disabled,
    clearDisabled: document.querySelector("#clearLearningButton")?.disabled,
    status: document.querySelector("#settingsStatus")?.textContent,
    recallText: document.querySelector("[data-recall-practice]")?.textContent
  }));

  await page.setInputFiles("#importLearningInput", learningExportPath);
  await page.waitForFunction(() => document.querySelector("#settingsLearningCount")?.textContent === "2");
  const learningImportState = await page.evaluate(() => ({
    learningCount: document.querySelector("#settingsLearningCount")?.textContent,
    status: document.querySelector("#settingsStatus")?.textContent,
    learningRaw: localStorage.getItem("onoko-arcana:desktop:learning:v1"),
    studyLensText: document.querySelector("#studyLens")?.textContent
  }));
  await page.click("#closeSettingsButton");
  await page.waitForFunction(() => document.querySelector("#settingsDialog")?.hidden === true);

  const dueAttempt = {
    attemptedAt: new Date(Date.now() - 86400000).toISOString(),
    cardId: firstStudyCard.cardId,
    cardLabel: firstStudyCard.label,
    orientation: "upright",
    promptType: "keyword_recall",
    answer: "復習予定を確認するための古い hard 記録",
    confidence: "hard"
  };
  await page.evaluate(({ key, attempt }) => {
    localStorage.setItem(key, JSON.stringify({
      app: "ONOKO_ARCANA",
      schemaVersion: 1,
      attempts: [attempt]
    }));
  }, { key: LEARNING_KEY, attempt: dueAttempt });
  await page.click("#resetButton");
  await openInspectorTab(page, "study");
  await page.waitForSelector("[data-due-review-cue]");
  const dueReviewState = await page.evaluate(() => ({
    dueText: document.querySelector("[data-due-review-cue]")?.textContent,
    dueCount: document.querySelector("[data-due-count]")?.textContent,
    dueButtons: document.querySelectorAll("[data-due-review-cue] [data-recall-start]").length,
    learningRaw: localStorage.getItem("onoko-arcana:desktop:learning:v1")
  }));

  await openInspectorTab(page, "history");
  await page.click('[data-history-index="0"]');
  await page.waitForFunction(() => Boolean(document.querySelector("#historyReview [data-review-active='true']")));
  await openInspectorTab(page, "history");
  const reviewState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    reviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
    reviewRows: document.querySelectorAll("#historyReview .review-card-row").length,
    reviewText: document.querySelector("#historyReview")?.textContent
  }));

  await openInspectorTab(page, "history");
  const deleteDialogPromise = page.waitForEvent("dialog").then((dialog) => dialog.accept());
  await page.click('[data-history-delete-index="0"]');
  await deleteDialogPromise;
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "2");
  const deleteState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    historyDeleteButtons: document.querySelectorAll(".history-delete").length,
    reviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
    noteStatus: document.querySelector("#noteStatus")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled
  }));

  const clearDialogPromise = page.waitForEvent("dialog").then((dialog) => dialog.accept());
  await page.click("#clearHistoryButton");
  await clearDialogPromise;
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "0");
  const clearState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    historyDeleteButtons: document.querySelectorAll(".history-delete").length,
    noteStatus: document.querySelector("#noteStatus")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled,
    reviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']"))
  }));

  await page.close();
  return {
    screenshot,
    firstLaunchScreenshot,
    settingsScreenshot,
    consoleErrors,
    exportPath,
    learningExportPath,
    invalidImportPath,
    cardNoteOnlyImportPath,
    corruptStorageState,
    firstLaunchState,
    firstLaunchFocusState,
    importState,
    duplicateImportState,
    invalidImportState,
    cardNoteOnlyRestoreState,
    firstStudyCard,
    inactiveStudySheetCard,
    cardStudySheetState,
    selectedStudySheetState,
    slotDrillBeforeAnswerState,
    slotDrillRevealState,
    slotDrillSavedState,
    studyFilterState,
    studyFilterClearState,
    studyLensSheetState,
    recallStartState,
    recallBeforeAnswerState,
    recallRevealState,
    recallSavedState,
    settingsOpenState,
    compactSettingState,
    learningClearState,
    learningImportState,
    dueReviewState,
    reviewState,
    deleteState,
    clearState,
    state
  };
}

async function runMobile(browser, id) {
  const screenshot = path.join(REPORTS, `onoko-arcana-web-app-mobile-${id}.png`);
  const { page, consoleErrors } = await openPage(browser, {
    viewport: { width: 390, height: 900 },
    deviceScaleFactor: 2,
    isMobile: true
  });

  await page.click('[data-spread-id="relationship_line"]');
  await page.click("#drawButton");
  await reveal(page, 6);
  await page.fill("#noteInput", "関係性を順番に読む。");
  await page.screenshot({ path: screenshot, fullPage: true });

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    revealed: document.querySelector("#statRevealed")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    cardStudySheets: document.querySelectorAll("#cardStudySheetPanel [data-study-sheet-open]").length,
    guideButtonExists: Boolean(document.querySelector("#toggleGuideButton")),
    scrollWidth: document.documentElement.scrollWidth,
    viewport: window.innerWidth
  }));

  await page.close();
  return { screenshot, consoleErrors, state };
}

(async () => {
  fs.mkdirSync(REPORTS, { recursive: true });
  const id = stamp();
  const browser = await chromium.launch({ headless: true });
  const desktop = await runDesktop(browser, id);
  const mobile = await runMobile(browser, id);
  await browser.close();

  const ok =
    desktop.consoleErrors.length === 0 &&
    mobile.consoleErrors.length === 0 &&
    desktop.firstLaunchState.firstLaunchVisible === true &&
    desktop.firstLaunchState.tabCount === 3 &&
    desktop.firstLaunchState.activeTab === "history" &&
    desktop.firstLaunchState.steps === 4 &&
    desktop.firstLaunchState.text.includes("はじめの一巡") &&
    desktop.firstLaunchState.text.includes("学習シートを見ながら保存") &&
    desktop.firstLaunchState.boardCards === 1 &&
    desktop.firstLaunchFocusState.activeId === "questionInput" &&
    desktop.state.spreadChoices === 6 &&
    desktop.state.tabCount === 3 &&
    desktop.state.activeTab === "study" &&
    desktop.state.activePanel === "study" &&
    desktop.state.revealed === "10" &&
    desktop.state.saved === "2" &&
    desktop.state.cards === 10 &&
    desktop.state.cardStudySheets === 1 &&
    desktop.state.guideButtonExists === false &&
    desktop.state.guidePanelExists === false &&
    desktop.state.historyItems === 2 &&
    desktop.state.historyDeleteButtons === 2 &&
    desktop.state.historyReviewActive === true &&
    desktop.state.studyLensText.includes("学習レンズ") &&
    desktop.state.studyLensText.includes("未出") &&
    desktop.state.dueCount.includes("0") &&
    desktop.state.afterSaveActions === 2 &&
    desktop.state.afterSaveText.includes("保存しました") &&
    desktop.state.afterSaveText.includes("次の問い") &&
    desktop.state.importExists === true &&
    desktop.state.exportDisabled === false &&
    desktop.state.clearDisabled === false &&
    desktop.importState.saved === "2" &&
    desktop.importState.historyItems === 2 &&
    desktop.importState.studyLensText.includes("学習レンズ") &&
    desktop.importState.exportDisabled === false &&
    desktop.importState.clearDisabled === false &&
    desktop.importState.noteStatus.includes("履歴 2 件を読み込み") &&
    desktop.duplicateImportState.saved === "2" &&
    desktop.duplicateImportState.historyItems === 2 &&
    desktop.duplicateImportState.noteStatus.includes("読み込み済み") &&
    desktop.invalidImportState.saved === "2" &&
    desktop.invalidImportState.historyItems === 2 &&
    desktop.invalidImportState.noteStatus.includes("読めません") &&
    desktop.cardNoteOnlyRestoreState.saved === "1" &&
    desktop.cardNoteOnlyRestoreState.restoredNote === "cards entryだけに残る復元メモ" &&
    desktop.cardNoteOnlyRestoreState.reviewText.includes("cards entryだけに残る復元メモ") &&
    desktop.cardNoteOnlyRestoreState.reviewText.includes("0 愚者") &&
    !desktop.cardNoteOnlyRestoreState.reviewText.includes("undefined") &&
    desktop.firstStudyCard.cardId &&
    desktop.firstStudyCard.buttons > 0 &&
    desktop.inactiveStudySheetCard.cardId &&
    desktop.inactiveStudySheetCard.buttons > 1 &&
    desktop.inactiveStudySheetCard.cardId !== desktop.selectedStudySheetState.cardId &&
    desktop.inactiveStudySheetCard.cardId !== desktop.firstStudyCard.cardId &&
    desktop.cardStudySheetState.open === true &&
    desktop.cardStudySheetState.source === "card" &&
    desktop.cardStudySheetState.text.includes("象徴") &&
    desktop.cardStudySheetState.text.includes("誤読しやすい点") &&
    desktop.cardStudySheetState.text.includes("内省質問") &&
    desktop.cardStudySheetState.symbols >= 2 &&
    desktop.cardStudySheetState.cautions >= 2 &&
    desktop.cardStudySheetState.reflections >= 2 &&
    desktop.cardStudySheetState.slotDrill === true &&
    desktop.cardStudySheetState.noteValue.includes("2D占い卓") &&
    desktop.cardStudySheetState.guideButtonExists === false &&
    desktop.cardStudySheetState.guidePanelExists === false &&
    desktop.selectedStudySheetState.open === true &&
    desktop.selectedStudySheetState.text.includes("象徴") &&
    desktop.selectedStudySheetState.text.includes("誤読しやすい点") &&
    desktop.selectedStudySheetState.text.includes("内省質問") &&
    desktop.selectedStudySheetState.symbols >= 2 &&
    desktop.selectedStudySheetState.cautions >= 2 &&
    desktop.selectedStudySheetState.reflections >= 2 &&
    desktop.selectedStudySheetState.recallButton === true &&
    desktop.selectedStudySheetState.filterButton === true &&
    desktop.selectedStudySheetState.slotDrill === true &&
    desktop.selectedStudySheetState.slotDrillText.includes("スロット練習") &&
    desktop.selectedStudySheetState.slotDrillRevealDisabled === true &&
    desktop.selectedStudySheetState.expanded === "true" &&
    desktop.slotDrillBeforeAnswerState.text.includes("解説を見る前") &&
    desktop.slotDrillBeforeAnswerState.revealDisabled === true &&
    desktop.slotDrillBeforeAnswerState.learningRaw === null &&
    desktop.slotDrillRevealState.guideText.includes("スロット") &&
    desktop.slotDrillRevealState.confidenceButtons === 3 &&
    desktop.slotDrillSavedState.attempts === 1 &&
    desktop.slotDrillSavedState.latest.promptType === "slot_interpretation" &&
    desktop.slotDrillSavedState.latest.slotKey &&
    desktop.slotDrillSavedState.latest.spreadId &&
    desktop.slotDrillSavedState.latest.confidence === "hard" &&
    desktop.slotDrillSavedState.text.includes("スロット練習を保存しました") &&
    desktop.studyFilterState.filterText.includes("カード別復習") &&
    desktop.studyFilterState.historyItems > 0 &&
    desktop.studyFilterState.clearExists === true &&
    desktop.studyFilterState.activeStudyButtons > 0 &&
    desktop.studyFilterState.reviewActive === true &&
    desktop.studyFilterState.compareBlocks > 0 &&
    desktop.studyFilterState.reviewText.includes("復習ノート") &&
    desktop.studyFilterState.reviewText.includes("自分の読み") &&
    desktop.studyFilterState.reviewText.includes("学習シート") &&
    desktop.studyFilterState.allRowsMatch === true &&
    desktop.studyFilterClearState.historyItems === 3 &&
    desktop.studyFilterClearState.filterVisible === false &&
    desktop.studyLensSheetState.openCardId === desktop.studyLensSheetState.cardId &&
    desktop.studyLensSheetState.text.includes("学習レンズから選択") &&
    desktop.studyLensSheetState.text.includes("正位置") &&
    desktop.studyLensSheetState.text.includes("逆位置") &&
    desktop.studyLensSheetState.slotDrillDisabled === true &&
    desktop.studyLensSheetState.slotDrillText.includes("卓でこのカードを選ぶ") &&
    desktop.studyLensSheetState.activeSheetLinks > 0 &&
    desktop.studyLensSheetState.actions === 2 &&
    desktop.recallStartState.text.includes("想起練習") &&
    desktop.recallStartState.starts > 0 &&
    desktop.recallBeforeAnswerState.cardText.includes("学習シートを見る前") &&
    desktop.recallBeforeAnswerState.revealDisabled === true &&
    desktop.recallBeforeAnswerState.learningRaw.includes('"slot_interpretation"') &&
    desktop.recallRevealState.text.includes("逆位置 学習シート") &&
    desktop.recallRevealState.guideText.includes("逆位置 学習シート") &&
    desktop.recallRevealState.confidenceButtons === 3 &&
    desktop.recallSavedState.attempts === 2 &&
    desktop.recallSavedState.latest.promptType === "keyword_recall" &&
    desktop.recallSavedState.latest.orientation === "reversed" &&
    desktop.recallSavedState.latest.answer.includes("迷子") &&
    desktop.recallSavedState.latest.confidence === "ok" &&
    desktop.recallSavedState.text.includes("練習結果を保存しました") &&
    desktop.settingsOpenState.dialogVisible === true &&
    desktop.settingsOpenState.title.includes("設定とバックアップ") &&
    desktop.settingsOpenState.historyCount === "3" &&
    desktop.settingsOpenState.learningCount === "2" &&
    desktop.settingsOpenState.historyExportDisabled === false &&
    desktop.settingsOpenState.learningExportDisabled === false &&
    desktop.settingsOpenState.version === "v0.1.3" &&
    desktop.settingsOpenState.releaseWarning.includes("未署名") &&
    desktop.settingsOpenState.releaseWarning.includes("自動更新") &&
    desktop.settingsOpenState.backupCue.includes("更新前") &&
    desktop.settingsOpenState.backupCue.includes("学習データ") &&
    desktop.settingsOpenState.latestReleaseHref === "https://github.com/imonoonoko/ONOKO_ARCANA/releases/latest" &&
    desktop.settingsOpenState.projectHref === "https://github.com/imonoonoko/ONOKO_ARCANA" &&
    desktop.settingsOpenState.securityHref === "https://github.com/imonoonoko/ONOKO_ARCANA/security/policy" &&
    desktop.settingsOpenState.licenseHref.includes("/docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md") &&
    desktop.settingsOpenState.licenseCue.includes("MIT") &&
    desktop.settingsOpenState.licenseCue.includes("再利用許諾外") &&
    desktop.settingsOpenState.localKeys.includes("onoko-arcana:desktop:history:v1") &&
    desktop.settingsOpenState.localKeys.includes("onoko-arcana:desktop:learning:v1") &&
    desktop.settingsOpenState.localKeys.includes("onoko-arcana:desktop:settings:v1") &&
    desktop.compactSettingState.bodyCompact === true &&
    desktop.compactSettingState.settingsRaw.includes('"compactLearningPanel":true') &&
    desktop.compactSettingState.status.includes("コンパクト") &&
    desktop.learningClearState.learningRaw === null &&
    desktop.learningClearState.learningCount === "0" &&
    desktop.learningClearState.exportDisabled === true &&
    desktop.learningClearState.clearDisabled === true &&
    desktop.learningClearState.status.includes("消去しました") &&
    desktop.learningClearState.recallText.includes("まだ練習記録") &&
    desktop.learningImportState.learningCount === "2" &&
    desktop.learningImportState.status.includes("学習 2 件") &&
    desktop.learningImportState.learningRaw.includes('"attempts"') &&
    desktop.learningImportState.studyLensText.includes("2 回") &&
    desktop.dueReviewState.dueText.includes("次に復習") &&
    desktop.dueReviewState.dueText.includes("復習時期") &&
    desktop.dueReviewState.dueCount.includes("1") &&
    desktop.dueReviewState.dueButtons > 0 &&
    desktop.dueReviewState.learningRaw.includes('"confidence":"hard"') &&
    desktop.corruptStorageState.saved === "0" &&
    desktop.corruptStorageState.historyText.includes("履歴データを読めません") &&
    desktop.corruptStorageState.exportDisabled === true &&
    desktop.corruptStorageState.clearDisabled === true &&
    desktop.reviewState.reviewActive === true &&
    desktop.reviewState.reviewRows === 10 &&
    desktop.reviewState.reviewText.includes("復習ノート") &&
    desktop.deleteState.saved === "2" &&
    desktop.deleteState.historyItems === 2 &&
    desktop.deleteState.historyDeleteButtons === 2 &&
    desktop.deleteState.exportDisabled === false &&
    desktop.deleteState.clearDisabled === false &&
    desktop.deleteState.noteStatus.includes("削除しました") &&
    desktop.clearState.saved === "0" &&
    desktop.clearState.historyItems === 0 &&
    desktop.clearState.historyDeleteButtons === 0 &&
    desktop.clearState.exportDisabled === true &&
    desktop.clearState.clearDisabled === true &&
    desktop.clearState.reviewActive === false &&
    desktop.clearState.noteStatus.includes("全消去しました") &&
    desktop.state.scrollWidth <= desktop.state.viewport &&
    desktop.state.scrollHeight <= desktop.state.viewportHeight &&
    desktop.state.sidePanelFits === true &&
    desktop.state.inspectorFits === true &&
    mobile.state.revealed === "6" &&
    mobile.state.cards === 6 &&
    mobile.state.cardStudySheets === 1 &&
    mobile.state.guideButtonExists === false &&
    mobile.state.scrollWidth <= mobile.state.viewport;

  const report = {
    ok,
    app: path.relative(ROOT, APP),
    desktop,
    mobile,
    checkedAt: new Date().toISOString()
  };
  const reportPath = path.join(REPORTS, `web-app-smoke-${id}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({ ...report, report: path.relative(ROOT, reportPath) }, null, 2));
  if (!ok) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

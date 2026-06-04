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
  const page = await browser.newPage(viewport);
  const consoleErrors = [];
  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  await page.goto(pathToFileURL(APP).href, { waitUntil: "domcontentloaded" });
  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  return { page, consoleErrors };
}

async function reveal(page, count) {
  for (let index = 0; index < count; index += 1) {
    await page.click("#revealButton");
  }
}

async function runDesktop(browser, id) {
  const screenshot = path.join(REPORTS, `onoko-arcana-web-app-celtic-${id}.png`);
  const exportPath = path.join(REPORTS, `onoko-arcana-history-export-${id}.json`);
  const invalidImportPath = path.join(FIXTURES, "invalid-json.json");
  const { page, consoleErrors } = await openPage(browser, {
    viewport: { width: 1424, height: 881 },
    deviceScaleFactor: 1
  });

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
  const guideDisabledBeforeNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.fill("#noteInput", "自分と相手、接点、課題、助言、可能性を同じ卓で読む。");
  const guideDisabledAfterNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.click("#toggleGuideButton");
  await page.click("#saveReadingButton");

  await page.click('[data-spread-id="celtic_cross"]');
  await page.fill("#questionInput", "ONOKOアプリの完成へ向けて、今どの構造を採用するべきか");
  await page.click("#drawButton");
  await reveal(page, 10);
  await page.fill("#noteInput", "2D占い卓を本体として完成させ、UE化は現行ロードマップでは見送る。");
  await page.click("#toggleGuideButton");
  await page.click("#saveReadingButton");
  await page.waitForTimeout(250);
  await page.screenshot({ path: screenshot, fullPage: true });

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    spreadChoices: document.querySelectorAll("[data-spread-id]").length,
    revealed: document.querySelector("#statRevealed")?.textContent,
    saved: document.querySelector("#statSaved")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    selected: document.querySelector("#selectedCard h2")?.textContent,
    guideRows: document.querySelectorAll(".guide-row").length,
    historyItems: document.querySelectorAll(".history-item").length,
    historyDeleteButtons: document.querySelectorAll(".history-delete").length,
    historyReviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
    status: document.querySelector("#statusLine")?.textContent,
    importExists: Boolean(document.querySelector("#importHistoryButton")),
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled,
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    viewport: window.innerWidth,
    viewportHeight: window.innerHeight,
    sidePanelFits: document.querySelector(".side-panel")?.scrollHeight <= document.querySelector(".side-panel")?.clientHeight + 1,
    inspectorFits: document.querySelector(".inspector")?.scrollHeight <= document.querySelector(".inspector")?.clientHeight + 1
  }));

  const downloadPromise = page.waitForEvent("download");
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

  await page.click('[data-history-index="0"]');
  await page.waitForSelector("#historyReview [data-review-active='true']");
  const reviewState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    reviewActive: Boolean(document.querySelector("#historyReview [data-review-active='true']")),
    reviewRows: document.querySelectorAll("#historyReview .review-card-row").length,
    reviewText: document.querySelector("#historyReview")?.textContent
  }));

  const deleteDialogPromise = page.waitForEvent("dialog").then((dialog) => dialog.accept());
  await page.click('[data-history-delete-index="0"]');
  await deleteDialogPromise;
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "1");
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
    consoleErrors,
    exportPath,
    invalidImportPath,
    corruptStorageState,
    importState,
    duplicateImportState,
    invalidImportState,
    reviewState,
    deleteState,
    clearState,
    guideDisabledBeforeNote,
    guideDisabledAfterNote,
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
  await page.click("#toggleGuideButton");
  await page.screenshot({ path: screenshot, fullPage: true });

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    revealed: document.querySelector("#statRevealed")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    guideRows: document.querySelectorAll(".guide-row").length,
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
    desktop.state.spreadChoices === 6 &&
    desktop.state.revealed === "10" &&
    desktop.state.saved === "2" &&
    desktop.state.cards === 10 &&
    desktop.state.guideRows === 3 &&
    desktop.state.historyItems === 2 &&
    desktop.state.historyDeleteButtons === 2 &&
    desktop.state.historyReviewActive === true &&
    desktop.state.importExists === true &&
    desktop.state.exportDisabled === false &&
    desktop.state.clearDisabled === false &&
    desktop.importState.saved === "2" &&
    desktop.importState.historyItems === 2 &&
    desktop.importState.exportDisabled === false &&
    desktop.importState.clearDisabled === false &&
    desktop.importState.noteStatus.includes("履歴 2 件を読み込み") &&
    desktop.duplicateImportState.saved === "2" &&
    desktop.duplicateImportState.historyItems === 2 &&
    desktop.duplicateImportState.noteStatus.includes("読み込み済み") &&
    desktop.invalidImportState.saved === "2" &&
    desktop.invalidImportState.historyItems === 2 &&
    desktop.invalidImportState.noteStatus.includes("読めません") &&
    desktop.corruptStorageState.saved === "0" &&
    desktop.corruptStorageState.historyText.includes("履歴データを読めません") &&
    desktop.corruptStorageState.exportDisabled === true &&
    desktop.corruptStorageState.clearDisabled === true &&
    desktop.reviewState.reviewActive === true &&
    desktop.reviewState.reviewRows === 10 &&
    desktop.reviewState.reviewText.includes("復習ノート") &&
    desktop.deleteState.saved === "1" &&
    desktop.deleteState.historyItems === 1 &&
    desktop.deleteState.historyDeleteButtons === 1 &&
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
    desktop.guideDisabledBeforeNote === true &&
    desktop.guideDisabledAfterNote === false &&
    desktop.state.scrollWidth <= desktop.state.viewport &&
    desktop.state.scrollHeight <= desktop.state.viewportHeight &&
    desktop.state.sidePanelFits === true &&
    desktop.state.inspectorFits === true &&
    mobile.state.revealed === "6" &&
    mobile.state.cards === 6 &&
    mobile.state.guideRows === 3 &&
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

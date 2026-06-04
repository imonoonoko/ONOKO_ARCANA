const fs = require("node:fs");
const path = require("node:path");
const Module = require("node:module");

const ROOT = path.resolve(__dirname, "..");
const PACKAGE_ROOT = path.join(ROOT, "dist", "onoko-arcana-local");
const PACKAGED_WEB = path.join(PACKAGE_ROOT, "web-app");
const PACKAGE_MAIN = path.join(PACKAGED_WEB, "electron", "main.cjs");
const PACKAGE_ELECTRON = path.join(PACKAGED_WEB, "node_modules", "electron", "dist", "electron.exe");
const PACKAGE_FIXTURES = path.join(PACKAGE_ROOT, "tests", "fixtures", "history");
const ROOT_WEB_NODE_MODULES = path.join(ROOT, "web-app", "node_modules");
const PACKAGE_NODE_MODULES = path.join(PACKAGED_WEB, "node_modules");
const REPORTS = path.join(ROOT, "reports");
const HISTORY_KEY = "onoko-arcana:desktop:history:v1";

process.env.NODE_PATH = [process.env.NODE_PATH, ROOT_WEB_NODE_MODULES, PACKAGE_NODE_MODULES]
  .filter(Boolean)
  .join(path.delimiter);
Module._initPaths();

const { _electron: electron } = require("playwright");

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

function failMissing(input) {
  if (!fs.existsSync(input)) {
    console.error(JSON.stringify({
      ok: false,
      message: "local package is missing; run scripts/package_electron_local.cjs first",
      missing: path.relative(ROOT, input)
    }, null, 2));
    process.exit(1);
  }
}

(async () => {
  [PACKAGE_ROOT, PACKAGE_MAIN, PACKAGE_ELECTRON, PACKAGE_FIXTURES].forEach(failMissing);
  fs.mkdirSync(REPORTS, { recursive: true });

  const id = stamp();
  const screenshot = path.join(REPORTS, `onoko-arcana-package-smoke-${id}.png`);
  const exportPath = path.join(REPORTS, `onoko-arcana-package-history-export-${id}.json`);
  const invalidImportPath = path.join(PACKAGE_FIXTURES, "invalid-json.json");

  const electronApp = await electron.launch({
    executablePath: PACKAGE_ELECTRON,
    args: [PACKAGE_MAIN]
  });
  const page = await electronApp.firstWindow();
  const consoleErrors = [];

  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.waitForSelector('[data-spread-id="relationship_line"]', { timeout: 15000 });
  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.click('[data-spread-id="relationship_line"]');
  await page.fill("#questionInput", "local packageから継続使用できるか");
  await page.click("#drawButton");
  for (let index = 0; index < 6; index += 1) {
    await page.click("#revealButton");
  }
  const guideDisabledBeforeNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.fill("#noteInput", "package内のElectronから起動し、保存と復元を確認する。");
  const guideDisabledAfterNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.click("#toggleGuideButton");
  await page.click("#saveReadingButton");
  await page.screenshot({ path: screenshot, fullPage: true });

  const savedState = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    spreadChoices: document.querySelectorAll("[data-spread-id]").length,
    revealed: document.querySelector("#statRevealed")?.textContent,
    saved: document.querySelector("#statSaved")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    guideRows: document.querySelectorAll(".guide-row").length,
    historyItems: document.querySelectorAll(".history-item").length,
    title: document.title,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled,
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    viewport: window.innerWidth,
    viewportHeight: window.innerHeight,
    sidePanelFits: document.querySelector(".side-panel")?.scrollHeight <= document.querySelector(".side-panel")?.clientHeight + 1,
    inspectorFits: document.querySelector(".inspector")?.scrollHeight <= document.querySelector(".inspector")?.clientHeight + 1
  }));

  const exportPayload = await page.evaluate((key) => ({
    app: "ONOKO_ARCANA",
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    history: JSON.parse(localStorage.getItem(key) || "[]")
  }), HISTORY_KEY);
  fs.writeFileSync(exportPath, JSON.stringify(exportPayload, null, 2), "utf8");

  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.reload({ waitUntil: "domcontentloaded" });
  await page.waitForSelector("#importHistoryInput");
  await page.setInputFiles("#importHistoryInput", exportPath);
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "1");
  const importState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    noteStatus: document.querySelector("#noteStatus")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled
  }));

  await page.setInputFiles("#importHistoryInput", invalidImportPath);
  await page.waitForFunction(() => document.querySelector("#noteStatus")?.textContent.includes("読めません"));
  const invalidImportState = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    historyItems: document.querySelectorAll(".history-item").length,
    noteStatus: document.querySelector("#noteStatus")?.textContent
  }));

  await electronApp.close();

  const ok =
    consoleErrors.length === 0 &&
    guideDisabledBeforeNote === true &&
    guideDisabledAfterNote === false &&
    savedState.spreadTitle === "関係性ライン" &&
    savedState.spreadChoices === 6 &&
    savedState.revealed === "6" &&
    savedState.saved === "1" &&
    savedState.cards === 6 &&
    savedState.guideRows === 3 &&
    savedState.historyItems === 1 &&
    savedState.title === "ONOKO ARCANA" &&
    savedState.exportDisabled === false &&
    savedState.clearDisabled === false &&
    savedState.scrollWidth <= savedState.viewport &&
    savedState.scrollHeight <= savedState.viewportHeight &&
    savedState.sidePanelFits === true &&
    savedState.inspectorFits === true &&
    importState.saved === "1" &&
    importState.historyItems === 1 &&
    importState.noteStatus.includes("履歴 1 件を読み込み") &&
    importState.exportDisabled === false &&
    importState.clearDisabled === false &&
    invalidImportState.saved === "1" &&
    invalidImportState.historyItems === 1 &&
    invalidImportState.noteStatus.includes("読めません");

  const report = {
    ok,
    package: path.relative(ROOT, PACKAGE_ROOT),
    app: path.relative(ROOT, PACKAGE_MAIN),
    screenshot,
    exportPath,
    invalidImportPath,
    guideDisabledBeforeNote,
    guideDisabledAfterNote,
    savedState,
    importState,
    invalidImportState,
    consoleErrors,
    checkedAt: new Date().toISOString()
  };
  const reportPath = path.join(REPORTS, `electron-package-smoke-${id}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({ ...report, report: path.relative(ROOT, reportPath) }, null, 2));
  if (!ok) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

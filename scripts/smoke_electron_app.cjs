const fs = require("node:fs");
const path = require("node:path");
const Module = require("node:module");

const ROOT = path.resolve(__dirname, "..");
const WEB_NODE_MODULES = path.join(ROOT, "web-app", "node_modules");
process.env.NODE_PATH = [process.env.NODE_PATH, WEB_NODE_MODULES].filter(Boolean).join(path.delimiter);
Module._initPaths();

const { _electron: electron } = require("playwright");

const MAIN = path.join(ROOT, "web-app", "electron", "main.cjs");
const REPORTS = path.join(ROOT, "reports");
const HISTORY_KEY = "onoko-arcana:desktop:history:v1";
const APP_ICON_PNG = path.join(ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.png");
const APP_ICON_ICO = path.join(ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.ico");

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

function canAssertSingleViewportFit(state) {
  return state.viewport >= 1400 && state.viewportHeight >= 860;
}

(async () => {
  fs.mkdirSync(REPORTS, { recursive: true });
  const iconState = {
    png: path.relative(ROOT, APP_ICON_PNG),
    ico: path.relative(ROOT, APP_ICON_ICO),
    pngExists: fs.existsSync(APP_ICON_PNG),
    icoExists: fs.existsSync(APP_ICON_ICO),
    mainUsesAppUserModelId: fs.readFileSync(MAIN, "utf8").includes("setAppUserModelId")
  };
  const id = stamp();
  const screenshot = path.join(REPORTS, `onoko-arcana-electron-smoke-${id}.png`);
  const electronPath = require("electron");
  const electronApp = await electron.launch({ executablePath: electronPath, args: [MAIN] });
  const page = await electronApp.firstWindow();
  const consoleErrors = [];

  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.waitForSelector('[data-spread-id="relationship_line"]', { timeout: 15000 });
  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.click('[data-spread-id="relationship_line"]');
  await page.fill("#questionInput", "Electronで完成形の操作を確認する");
  await page.click("#drawButton");
  for (let index = 0; index < 6; index += 1) {
    await page.click("#revealButton");
  }
  await page.fill("#noteInput", "Electron shellでも同じリーディング体験を保つ。");
  const cardStudySheetState = await page.evaluate(() => ({
    open: Boolean(document.querySelector("#cardStudySheetPanel [data-study-sheet-open]")),
    text: document.querySelector("#cardStudySheetPanel")?.textContent,
    guideButtonExists: Boolean(document.querySelector("#toggleGuideButton")),
    guidePanelExists: Boolean(document.querySelector("#guidePanel"))
  }));
  await page.click("#saveReadingButton");
  await page.screenshot({ path: screenshot, fullPage: true });

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    spreadChoices: document.querySelectorAll("[data-spread-id]").length,
    revealed: document.querySelector("#statRevealed")?.textContent,
    saved: document.querySelector("#statSaved")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    cardStudySheets: document.querySelectorAll("#cardStudySheetPanel [data-study-sheet-open]").length,
    guideButtonExists: Boolean(document.querySelector("#toggleGuideButton")),
    historyItems: document.querySelectorAll(".history-item").length,
    title: document.title,
    scrollWidth: document.documentElement.scrollWidth,
    scrollHeight: document.documentElement.scrollHeight,
    viewport: window.innerWidth,
    viewportHeight: window.innerHeight,
    sidePanelFits: document.querySelector(".side-panel")?.scrollHeight <= document.querySelector(".side-panel")?.clientHeight + 1,
    inspectorFits: document.querySelector(".inspector")?.scrollHeight <= document.querySelector(".inspector")?.clientHeight + 1
  }));
  const singleViewportFitChecked = canAssertSingleViewportFit(state);

  await electronApp.close();

  const ok =
    consoleErrors.length === 0 &&
    iconState.pngExists === true &&
    iconState.icoExists === true &&
    iconState.mainUsesAppUserModelId === true &&
    cardStudySheetState.open === true &&
    cardStudySheetState.text.includes("象徴") &&
    cardStudySheetState.text.includes("誤読しやすい点") &&
    cardStudySheetState.guideButtonExists === false &&
    cardStudySheetState.guidePanelExists === false &&
    state.spreadTitle === "関係性ライン" &&
    state.spreadChoices === 6 &&
    state.revealed === "6" &&
    state.saved === "1" &&
    state.cards === 6 &&
    state.cardStudySheets === 1 &&
    state.guideButtonExists === false &&
    state.historyItems === 1 &&
    state.title === "ONOKO ARCANA" &&
    state.scrollWidth <= state.viewport &&
    (!singleViewportFitChecked || state.scrollHeight <= state.viewportHeight) &&
    state.sidePanelFits === true &&
    state.inspectorFits === true;

  const report = {
    ok,
    app: path.relative(ROOT, MAIN),
    screenshot,
    iconState,
    cardStudySheetState,
    singleViewportFitChecked,
    state,
    consoleErrors,
    checkedAt: new Date().toISOString()
  };
  const reportPath = path.join(REPORTS, `electron-app-smoke-${id}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({ ...report, report: path.relative(ROOT, reportPath) }, null, 2));
  if (!ok) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

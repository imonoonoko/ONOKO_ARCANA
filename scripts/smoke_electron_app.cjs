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

(async () => {
  fs.mkdirSync(REPORTS, { recursive: true });
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
  const guideDisabledBeforeNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.fill("#noteInput", "Electron shellでも同じリーディング体験を保つ。");
  const guideDisabledAfterNote = await page.locator("#toggleGuideButton").isDisabled();
  await page.click("#toggleGuideButton");
  await page.click("#saveReadingButton");
  await page.screenshot({ path: screenshot, fullPage: true });

  const state = await page.evaluate(() => ({
    spreadTitle: document.querySelector("#spreadTitle")?.textContent,
    spreadChoices: document.querySelectorAll("[data-spread-id]").length,
    revealed: document.querySelector("#statRevealed")?.textContent,
    saved: document.querySelector("#statSaved")?.textContent,
    cards: document.querySelectorAll(".arcana-card").length,
    guideRows: document.querySelectorAll(".guide-row").length,
    historyItems: document.querySelectorAll(".history-item").length,
    title: document.title
  }));

  await electronApp.close();

  const ok =
    consoleErrors.length === 0 &&
    guideDisabledBeforeNote === true &&
    guideDisabledAfterNote === false &&
    state.spreadTitle === "関係性ライン" &&
    state.spreadChoices === 6 &&
    state.revealed === "6" &&
    state.saved === "1" &&
    state.cards === 6 &&
    state.guideRows === 3 &&
    state.historyItems === 1 &&
    state.title === "ONOKO ARCANA";

  const report = {
    ok,
    app: path.relative(ROOT, MAIN),
    screenshot,
    guideDisabledBeforeNote,
    guideDisabledAfterNote,
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

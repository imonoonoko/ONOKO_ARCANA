const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
require("module").Module._initPaths();

const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const APP = path.join(ROOT, "web-app", "index.html");
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

async function activeDescriptor(page) {
  return page.evaluate(() => {
    const el = document.activeElement;
    if (!el) return "";
    if (el.id) return `#${el.id}`;
    if (el.dataset?.spreadId) return `[data-spread-id="${el.dataset.spreadId}"]`;
    if (el.dataset?.historyIndex) return `[data-history-index="${el.dataset.historyIndex}"]`;
    if (el.dataset?.historyDeleteIndex) return `[data-history-delete-index="${el.dataset.historyDeleteIndex}"]`;
    return el.tagName.toLowerCase();
  });
}

async function run() {
  fs.mkdirSync(REPORTS, { recursive: true });
  const id = stamp();
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1366, height: 768 }, deviceScaleFactor: 1 });
  const consoleErrors = [];
  page.on("pageerror", (error) => consoleErrors.push(error.message));
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });

  await page.goto(pathToFileURL(APP).href, { waitUntil: "domcontentloaded" });
  await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
  await page.reload({ waitUntil: "domcontentloaded" });

  const focusSequence = [];
  for (let index = 0; index < 9; index += 1) {
    await page.keyboard.press("Tab");
    focusSequence.push(await activeDescriptor(page));
  }

  const firstFocused = focusSequence[0];
  const includesSpread = focusSequence.some((step) => step.startsWith("[data-spread-id="));
  const includesDraw = focusSequence.includes("#drawButton");
  const keyboardOutline = await page.evaluate(() => {
    const el = document.activeElement;
    const style = window.getComputedStyle(el);
    return {
      descriptor: el.id ? `#${el.id}` : el.tagName.toLowerCase(),
      outlineStyle: style.outlineStyle,
      outlineWidth: style.outlineWidth
    };
  });

  await page.fill("#questionInput", "キーボードだけで読みを完了できるか");
  await page.focus("#drawButton");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.querySelector("#statusLine")?.textContent.includes("Cards placed"));

  await page.focus("#revealButton");
  await page.keyboard.press("Space");
  await page.waitForFunction(() => document.querySelector("#statRevealed")?.textContent === "1");

  await page.focus("#noteInput");
  await page.keyboard.type("キーボード操作で自分の読みを残す。");
  await page.waitForFunction(() => !document.querySelector("#toggleGuideButton")?.disabled);

  await page.focus("#toggleGuideButton");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.querySelectorAll(".guide-row").length === 3);
  const guideRowsAfterToggle = await page.evaluate(() => document.querySelectorAll(".guide-row").length);

  await page.focus("#saveReadingButton");
  await page.keyboard.press("Enter");
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "1");

  await page.focus('[data-history-index="0"]');
  await page.keyboard.press("Enter");
  await page.waitForSelector("#historyReview [data-review-active='true']");

  await page.focus('[data-history-delete-index="0"]');
  const deleteDialogPromise = page.waitForEvent("dialog").then((dialog) => dialog.accept());
  await page.keyboard.press("Enter");
  await deleteDialogPromise;
  await page.waitForFunction(() => document.querySelector("#statSaved")?.textContent === "0");

  const state = await page.evaluate(() => ({
    saved: document.querySelector("#statSaved")?.textContent,
    revealed: document.querySelector("#statRevealed")?.textContent,
    guideRows: document.querySelectorAll(".guide-row").length,
    historyItems: document.querySelectorAll(".history-item").length,
    clearDisabled: document.querySelector("#clearHistoryButton")?.disabled,
    noteStatus: document.querySelector("#noteStatus")?.textContent,
    scrollWidth: document.documentElement.scrollWidth,
    viewport: window.innerWidth
  }));

  await browser.close();

  const ok =
    consoleErrors.length === 0 &&
    firstFocused === "#questionInput" &&
    includesSpread &&
    includesDraw &&
    keyboardOutline.outlineStyle !== "none" &&
    keyboardOutline.outlineWidth !== "0px" &&
    state.revealed === "1" &&
    state.saved === "0" &&
    guideRowsAfterToggle === 3 &&
    state.historyItems === 0 &&
    state.clearDisabled === true &&
    state.noteStatus.includes("削除しました") &&
    state.scrollWidth <= state.viewport;

  const report = {
    ok,
    app: path.relative(ROOT, APP),
    focusSequence,
    keyboardOutline,
    guideRowsAfterToggle,
    consoleErrors,
    state,
    checkedAt: new Date().toISOString()
  };
  const reportPath = path.join(REPORTS, `keyboard-focus-smoke-${id}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({ ...report, report: path.relative(ROOT, reportPath) }, null, 2));
  if (!ok) process.exit(1);
}

run().catch((error) => {
  console.error(error);
  process.exit(1);
});

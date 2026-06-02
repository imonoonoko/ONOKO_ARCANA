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
  const { page, consoleErrors } = await openPage(browser, {
    viewport: { width: 1600, height: 980 },
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
  await page.fill("#noteInput", "2D占い卓を本体として完成させ、UEは将来の高級表現層として残す。");
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
    status: document.querySelector("#statusLine")?.textContent,
    exportDisabled: document.querySelector("#exportHistoryButton")?.disabled,
    scrollWidth: document.documentElement.scrollWidth,
    viewport: window.innerWidth
  }));

  await page.close();
  return {
    screenshot,
    consoleErrors,
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
    desktop.state.exportDisabled === false &&
    desktop.guideDisabledBeforeNote === true &&
    desktop.guideDisabledAfterNote === false &&
    desktop.state.scrollWidth <= desktop.state.viewport &&
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

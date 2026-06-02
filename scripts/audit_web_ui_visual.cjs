const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
require("module").Module._initPaths();

const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const APP = path.join(ROOT, "web-app", "index.html");
const REPORTS = path.join(ROOT, "reports");
const HISTORY_KEY = "onoko-arcana:desktop:history:v1";

const SPREADS = [
  { id: "one_card", slots: 1, label: "one-card" },
  { id: "three_card_past_present_future", slots: 3, label: "three-card" },
  { id: "five_card_cross", slots: 5, label: "five-cross" },
  { id: "seven_card_horseshoe", slots: 7, label: "seven-horseshoe" },
  { id: "celtic_cross", slots: 10, label: "celtic-cross" },
  { id: "relationship_line", slots: 6, label: "relationship-line" }
];

const VIEWPORTS = [
  { id: "desktop", width: 1600, height: 980, mobile: false, spreads: SPREADS.map((spread) => spread.id) },
  { id: "compact", width: 1280, height: 840, mobile: false, spreads: ["one_card", "five_card_cross", "celtic_cross", "relationship_line"] },
  { id: "mobile", width: 390, height: 900, mobile: true, spreads: ["one_card", "seven_card_horseshoe", "relationship_line"] }
];

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
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: viewport.mobile ? 2 : 1,
    isMobile: viewport.mobile
  });
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

async function auditDom(page, meta) {
  return page.evaluate((input) => {
    const issues = [];
    const rectOf = (el) => {
      const rect = el.getBoundingClientRect();
      return {
        left: Number(rect.left.toFixed(2)),
        top: Number(rect.top.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        bottom: Number(rect.bottom.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        height: Number(rect.height.toFixed(2))
      };
    };
    const intersects = (a, b, tolerance = 0) => !(
      a.right <= b.left + tolerance ||
      b.right <= a.left + tolerance ||
      a.bottom <= b.top + tolerance ||
      b.bottom <= a.top + tolerance
    );
    const cssPath = (el) => {
      if (el.id) return `#${el.id}`;
      const className = String(el.className || "").trim().split(/\s+/).filter(Boolean).slice(0, 3).join(".");
      const tag = el.tagName.toLowerCase();
      return className ? `${tag}.${className}` : tag;
    };
    const textOf = (el) => (el.textContent || "").replace(/\s+/g, " ").trim();
    const add = (severity, code, message, context = {}) => {
      issues.push({
        severity,
        code,
        message,
        ...context
      });
    };

    if (document.documentElement.scrollWidth > window.innerWidth + 1) {
      add("P1", "horizontal-overflow", "page has horizontal overflow", {
        scrollWidth: document.documentElement.scrollWidth,
        viewport: window.innerWidth
      });
    }

    const overflowSelectors = [
      ".spread-choice-copy strong",
      ".spread-choice-copy span",
      ".slot-label",
      ".card-inscription",
      ".button",
      ".progress-dot span:last-child",
      ".selected-copy h2",
      ".selected-copy p",
      ".badge",
      ".guide-row span",
      ".history-item",
      ".micro-status"
    ];
    document.querySelectorAll(overflowSelectors.join(",")).forEach((el) => {
      const overflowX = el.scrollWidth - Math.ceil(el.clientWidth);
      const overflowY = el.scrollHeight - Math.ceil(el.clientHeight);
      const style = getComputedStyle(el);
      const fontSize = Number.parseFloat(style.fontSize || "0");
      if (overflowX > 1 || overflowY > 1) {
        add("P1", "text-overflow", "text is clipped or overflows its box", {
          selector: cssPath(el),
          text: textOf(el).slice(0, 80),
          rect: rectOf(el),
          overflowX,
          overflowY
        });
      }
      if (textOf(el) && fontSize > 0 && fontSize < 8) {
        add("P2", "tiny-text", "text is below 8px and likely unreadable in normal play", {
          selector: cssPath(el),
          text: textOf(el).slice(0, 80),
          fontSize,
          rect: rectOf(el)
        });
      }
    });

    document.querySelectorAll(".spread-choice").forEach((row) => {
      const copy = row.querySelector(".spread-choice-copy");
      const mini = row.querySelector(".spread-mini");
      const count = row.querySelector("em");
      if (!copy || !mini || !count) return;
      const copyRect = rectOf(copy);
      const miniRect = rectOf(mini);
      const countRect = rectOf(count);
      if (intersects(copyRect, miniRect, -2) || intersects(copyRect, countRect, -2)) {
        add("P1", "spread-row-overlap", "spread row text intersects the mini diagram or count", {
          spread: row.dataset.spreadId,
          copy: copyRect,
          mini: miniRect,
          count: countRect,
          text: textOf(copy)
        });
      }
    });

    const labels = Array.from(document.querySelectorAll(".slot-label"));
    const cards = Array.from(document.querySelectorAll(".slot .arcana-card"));
    labels.forEach((label, index) => {
      const labelRect = rectOf(label);
      const ownCard = cards[index];
      if (ownCard && intersects(labelRect, rectOf(ownCard), -1)) {
        add("P1", "slot-label-card-overlap", "slot label overlaps its card", {
          slot: index + 1,
          label: textOf(label),
          labelRect,
          cardRect: rectOf(ownCard)
        });
      }
      cards.forEach((card, cardIndex) => {
        if (cardIndex === index) return;
        if (intersects(labelRect, rectOf(card), -3)) {
          add("P2", "slot-label-other-card-overlap", "slot label overlaps another card", {
            labelSlot: index + 1,
            cardSlot: cardIndex + 1,
            label: textOf(label),
            labelRect,
            cardRect: rectOf(card)
          });
        }
      });
    });

    labels.forEach((a, aIndex) => {
      labels.slice(aIndex + 1).forEach((b, offset) => {
        if (intersects(rectOf(a), rectOf(b), -2)) {
          add("P1", "slot-label-label-overlap", "slot labels overlap each other", {
            aSlot: aIndex + 1,
            bSlot: aIndex + offset + 2,
            aText: textOf(a),
            bText: textOf(b),
            aRect: rectOf(a),
            bRect: rectOf(b)
          });
        }
      });
    });

    cards.forEach((a, aIndex) => {
      cards.slice(aIndex + 1).forEach((b, offset) => {
        if (intersects(rectOf(a), rectOf(b), -4)) {
          add("P3", "card-card-overlap", "card rectangles overlap; verify whether this is intentional for the spread", {
            aSlot: aIndex + 1,
            bSlot: aIndex + offset + 2,
            aRect: rectOf(a),
            bRect: rectOf(b)
          });
        }
      });
    });

    document.querySelectorAll(".arcana-card img").forEach((img, index) => {
      const card = img.closest(".arcana-card");
      const rect = rectOf(img);
      const natural = { width: img.naturalWidth, height: img.naturalHeight };
      const hasReadableInscriptions = Boolean(card?.querySelector(".card-inscription"));
      if (hasReadableInscriptions && (rect.width < 120 || rect.height < 180)) {
        add("P2", "card-rendered-small", "card image is rendered too small for in-card labels/details", {
          slot: index + 1,
          rect,
          natural
        });
      }
      const previewLongSide = Math.max(rect.width, rect.height);
      if (!hasReadableInscriptions && previewLongSide < 105) {
        add("P2", "card-preview-too-small", "marker-mode card preview is too small to identify the artwork", {
          slot: index + 1,
          rect,
          natural
        });
      }
      if (natural.width && rect.width > natural.width + 1) {
        add("P1", "card-upscaled", "card image is rendered larger than its source width", {
          slot: index + 1,
          rect,
          natural
        });
      }
    });

    document.querySelectorAll(".section-row .button.compact").forEach((button) => {
      const row = button.closest(".section-row");
      if (!row) return;
      const buttonRect = rectOf(button);
      const rowRect = rectOf(row);
      if (buttonRect.right > rowRect.right + 1 || buttonRect.left < rowRect.left - 1) {
        add("P2", "section-button-outside-row", "compact section button extends outside its section row", {
          text: textOf(button),
          buttonRect,
          rowRect
        });
      }
    });

    return {
      meta: input,
      title: document.querySelector("#spreadTitle")?.textContent || "",
      cardCount: cards.length,
      inscriptionCount: document.querySelectorAll(".card-inscription").length,
      consoleState: {
        scrollWidth: document.documentElement.scrollWidth,
        viewport: window.innerWidth,
        bodyHeight: document.body.scrollHeight
      },
      issues
    };
  }, meta);
}

async function runCase(browser, runDir, viewport, spread) {
  const { page, consoleErrors } = await openPage(browser, viewport);
  await page.click(`[data-spread-id="${spread.id}"]`);
  await page.fill("#questionInput", `UI監査: ${spread.label}`);
  await page.click("#drawButton");
  await reveal(page, spread.slots);
  await page.waitForTimeout(220);

  const screenshot = path.join(runDir, `${viewport.id}-${spread.label}.png`);
  await page.screenshot({ path: screenshot, fullPage: true });
  const domAudit = await auditDom(page, {
    viewport: viewport.id,
    width: viewport.width,
    height: viewport.height,
    spreadId: spread.id,
    spreadLabel: spread.label,
    screenshot: path.relative(ROOT, screenshot)
  });
  await page.close();
  return {
    ...domAudit,
    consoleErrors
  };
}

(async () => {
  fs.mkdirSync(REPORTS, { recursive: true });
  const id = stamp();
  const runDir = path.join(REPORTS, `ui-visual-audit-${id}`);
  fs.mkdirSync(runDir, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const cases = [];
  for (const viewport of VIEWPORTS) {
    for (const spread of SPREADS.filter((item) => viewport.spreads.includes(item.id))) {
      cases.push(await runCase(browser, runDir, viewport, spread));
    }
  }
  await browser.close();

  const issues = cases.flatMap((item) => item.issues.map((issue) => ({
    viewport: item.meta.viewport,
    spreadId: item.meta.spreadId,
    spreadLabel: item.meta.spreadLabel,
    screenshot: item.meta.screenshot,
    ...issue
  })));
  const counts = issues.reduce((acc, issue) => {
    acc[issue.severity] = (acc[issue.severity] || 0) + 1;
    acc[`${issue.severity}:${issue.code}`] = (acc[`${issue.severity}:${issue.code}`] || 0) + 1;
    return acc;
  }, {});
  const report = {
    ok: cases.every((item) => item.consoleErrors.length === 0),
    app: path.relative(ROOT, APP),
    runDir: path.relative(ROOT, runDir),
    cases,
    issues,
    counts,
    checkedAt: new Date().toISOString()
  };
  const reportPath = path.join(runDir, "report.json");
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2), "utf8");
  console.log(JSON.stringify({
    ok: report.ok,
    runDir: report.runDir,
    cases: cases.length,
    issueCount: issues.length,
    counts,
    report: path.relative(ROOT, reportPath)
  }, null, 2));
  if (!report.ok) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});

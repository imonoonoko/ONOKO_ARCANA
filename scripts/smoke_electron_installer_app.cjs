const fs = require("node:fs");
const path = require("node:path");
const Module = require("node:module");

const ROOT = path.resolve(__dirname, "..");
const WEB_APP = path.join(ROOT, "web-app");
const PACKAGE_JSON_PATH = path.join(WEB_APP, "package.json");
const PACKAGE_JSON = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, "utf8"));
const INSTALLER_DIR = path.join(ROOT, "dist", "installer");
const SETUP_EXE = path.join(INSTALLER_DIR, `onoko-arcana-v${PACKAGE_JSON.version}-setup.exe`);
const UNPACKED_DIR = path.join(INSTALLER_DIR, "win-unpacked");
const APP_EXE = path.join(UNPACKED_DIR, "ONOKO ARCANA.exe");
const RESOURCES = path.join(UNPACKED_DIR, "resources");
const REPORTS = path.join(ROOT, "reports");
const ROOT_WEB_NODE_MODULES = path.join(WEB_APP, "node_modules");
const HISTORY_KEY = "onoko-arcana:desktop:history:v1";

process.env.NODE_PATH = [process.env.NODE_PATH, ROOT_WEB_NODE_MODULES]
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

function fail(message, details = {}) {
  console.error(JSON.stringify({ ok: false, message, ...details }, null, 2));
  process.exit(1);
}

function requirePath(input, label) {
  if (!fs.existsSync(input)) {
    fail(`${label} is missing; run npm run package:installer first`, {
      missing: path.relative(ROOT, input)
    });
  }
}

function assertInstallerConfig() {
  const build = PACKAGE_JSON.build || {};
  const win = build.win || {};
  const nsis = build.nsis || {};
  const target = Array.isArray(win.target) ? win.target : [];
  const hasNsis = target.some((entry) => {
    if (typeof entry === "string") return entry === "nsis";
    return entry && entry.target === "nsis";
  });

  const state = {
    appId: build.appId,
    productName: build.productName,
    artifactName: build.artifactName,
    winIcon: win.icon,
    hasNsis,
    createDesktopShortcut: nsis.createDesktopShortcut,
    createStartMenuShortcut: nsis.createStartMenuShortcut,
    shortcutName: nsis.shortcutName
  };

  const failures = [];
  if (build.appId !== "com.onoko.arcana") failures.push("build.appId must stay com.onoko.arcana");
  if (build.productName !== "ONOKO ARCANA") failures.push("build.productName must stay ONOKO ARCANA");
  if (!String(win.icon || "").endsWith("onoko-arcana-app-icon-v1.ico")) {
    failures.push("build.win.icon must point to the .ico app icon");
  }
  if (!hasNsis) failures.push("build.win.target must include nsis");
  if (nsis.createDesktopShortcut !== "always") {
    failures.push('build.nsis.createDesktopShortcut must be "always"');
  }
  if (nsis.createStartMenuShortcut !== true) {
    failures.push("build.nsis.createStartMenuShortcut must be true");
  }
  if (nsis.shortcutName !== "ONOKO ARCANA") {
    failures.push("build.nsis.shortcutName must stay ONOKO ARCANA");
  }

  if (failures.length > 0) fail("installer shortcut/icon config is incomplete", { state, failures });
  return state;
}

(async () => {
  const installerConfig = assertInstallerConfig();
  const requiredPaths = [
    [SETUP_EXE, "NSIS setup artifact"],
    [APP_EXE, "packaged app executable"],
    [path.join(RESOURCES, "app.asar"), "packaged app archive"],
    [path.join(RESOURCES, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.ico"), "packaged app icon"],
    [path.join(RESOURCES, "assets", "generated", "card-production-v5-full", "web-labeled", "alpha", "card-back-onoko-v5-alpha.png"), "packaged card back"],
    [path.join(RESOURCES, "DISTRIBUTION_NOTICE.md"), "packaged distribution notice"],
    [path.join(RESOURCES, "docs", "legal", "ASSET_LICENSE_AND_ATTRIBUTION.md"), "packaged asset attribution"]
  ];
  requiredPaths.forEach(([input, label]) => requirePath(input, label));
  if (fs.statSync(SETUP_EXE).size < 50 * 1024 * 1024) {
    fail("NSIS setup artifact is unexpectedly small", {
      setup: path.relative(ROOT, SETUP_EXE),
      bytes: fs.statSync(SETUP_EXE).size
    });
  }

  fs.mkdirSync(REPORTS, { recursive: true });
  const id = stamp();
  const screenshot = path.join(REPORTS, `onoko-arcana-installer-smoke-${id}.png`);
  const reportPath = path.join(REPORTS, `onoko-arcana-installer-smoke-${id}.json`);
  const consoleErrors = [];
  const electronApp = await electron.launch({ executablePath: APP_EXE });

  try {
    const page = await electronApp.firstWindow();
    page.on("pageerror", (error) => consoleErrors.push(error.message));
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });

    await page.waitForSelector('[data-spread-id="relationship_line"]', { timeout: 15000 });
    await page.evaluate((key) => localStorage.removeItem(key), HISTORY_KEY);
    await page.click('[data-spread-id="relationship_line"]');
    await page.fill("#questionInput", "installer packageからカード画像と履歴保存を確認する");
    await page.click("#drawButton");
    for (let index = 0; index < 6; index += 1) {
      await page.click("#revealButton");
    }
    await page.fill("#noteInput", "electron-builder packaged app smoke");
    await page.click("#saveReadingButton");
    await page.click('[data-inspector-tab="history"]');
    await page.click("#openSettingsButton");
    await page.waitForSelector("#settingsDialog:not([hidden])");

    const pageState = await page.evaluate(async () => {
      const images = Array.from(document.images);
      await Promise.all(images.map((image) => {
        if (image.complete) return undefined;
        return new Promise((resolve) => {
          const done = () => resolve(undefined);
          image.addEventListener("load", done, { once: true });
          image.addEventListener("error", done, { once: true });
          setTimeout(done, 1200);
        });
      }));

      return {
        title: document.title,
        spreadTitle: document.querySelector("#spreadTitle")?.textContent,
        revealed: document.querySelector("#statRevealed")?.textContent,
        saved: document.querySelector("#statSaved")?.textContent,
        release: {
          version: document.querySelector("#settingsAppVersion")?.textContent,
          warning: document.querySelector("#settingsReleaseWarning")?.textContent,
          backupCue: document.querySelector("#settingsBackupCue")?.textContent,
          latestReleaseHref: document.querySelector("#settingsLatestReleaseLink")?.href,
          securityHref: document.querySelector("#settingsSecurityLink")?.href,
          licenseHref: document.querySelector("#settingsLicenseLink")?.href,
          licenseCue: document.querySelector("#settingsLicenseCue")?.textContent
        },
        imageCount: images.length,
        brokenImages: images
          .filter((image) => image.naturalWidth === 0 || image.naturalHeight === 0)
          .map((image) => image.getAttribute("src"))
          .slice(0, 10)
      };
    });

    await page.screenshot({ path: screenshot, fullPage: true });

    const report = {
      ok: true,
      setup: path.relative(ROOT, SETUP_EXE),
      setupBytes: fs.statSync(SETUP_EXE).size,
      appExe: path.relative(ROOT, APP_EXE),
      resources: path.relative(ROOT, RESOURCES),
      screenshot: path.relative(ROOT, screenshot),
      installerConfig,
      pageState,
      consoleErrors
    };

    if (pageState.brokenImages.length > 0) {
      fail("packaged app has broken image resources", report);
    }
    if (consoleErrors.length > 0) {
      fail("packaged app emitted console errors", report);
    }
    if (
      pageState.release.version !== `v${PACKAGE_JSON.version}` ||
      !pageState.release.warning.includes("未署名") ||
      !pageState.release.warning.includes("自動更新") ||
      !pageState.release.backupCue.includes("更新前") ||
      pageState.release.latestReleaseHref !== "https://github.com/imonoonoko/ONOKO_ARCANA/releases/latest" ||
      pageState.release.securityHref !== "https://github.com/imonoonoko/ONOKO_ARCANA/security/policy" ||
      !pageState.release.licenseHref.includes("/docs/legal/ASSET_LICENSE_AND_ATTRIBUTION.md") ||
      !pageState.release.licenseCue.includes("再利用許諾外")
    ) {
      fail("packaged app release/support settings are incomplete", report);
    }

    fs.writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
    console.log(JSON.stringify({ ...report, report: path.relative(ROOT, reportPath) }, null, 2));
  } finally {
    await electronApp.close();
  }
})().catch((error) => {
  fail(error.message, { stack: error.stack });
});

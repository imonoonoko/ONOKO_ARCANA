const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const DIST = path.join(ROOT, "dist");
const PACKAGE_ROOT = path.join(DIST, "onoko-arcana-local");
const WEB_APP = path.join(ROOT, "web-app");
const ELECTRON_MODULE = path.join(WEB_APP, "node_modules", "electron");

const copyEntries = [
  {
    source: WEB_APP,
    target: path.join(PACKAGE_ROOT, "web-app")
  },
  {
    source: path.join(ROOT, "assets", "generated", "card-production-v5-full", "web-labeled", "alpha"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "card-production-v5-full", "web-labeled", "alpha")
  },
  {
    source: path.join(ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.ico"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.ico")
  },
  {
    source: path.join(ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.png"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "app-icons", "onoko-arcana-app-icon-v1.png")
  },
  {
    source: path.join(ROOT, "assets", "generated", "hud-elements", "20260602-astra-modular-kit", "components"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "hud-elements", "20260602-astra-modular-kit", "components")
  },
  {
    source: path.join(ROOT, "assets", "generated", "hud-elements", "20260602-astra-nine-slice-kit", "nine-slice"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "hud-elements", "20260602-astra-nine-slice-kit", "nine-slice")
  },
  {
    source: path.join(ROOT, "assets", "generated", "hud-candidates", "20260602-named-hud-sets", "astra-nocturne-background-v1.png"),
    target: path.join(PACKAGE_ROOT, "assets", "generated", "hud-candidates", "20260602-named-hud-sets", "astra-nocturne-background-v1.png")
  },
  {
    source: path.join(ROOT, "docs", "data"),
    target: path.join(PACKAGE_ROOT, "docs", "data")
  },
  {
    source: path.join(ROOT, "tests", "fixtures", "history"),
    target: path.join(PACKAGE_ROOT, "tests", "fixtures", "history")
  },
  {
    source: path.join(ROOT, "README.md"),
    target: path.join(PACKAGE_ROOT, "README.md")
  },
  {
    source: path.join(ROOT, "LICENSE"),
    target: path.join(PACKAGE_ROOT, "LICENSE")
  },
  {
    source: path.join(ROOT, "SECURITY.md"),
    target: path.join(PACKAGE_ROOT, "SECURITY.md")
  },
  {
    source: path.join(ROOT, "docs", "legal"),
    target: path.join(PACKAGE_ROOT, "docs", "legal")
  },
  {
    source: path.join(ROOT, "docs", "release", "DISTRIBUTION_NOTICE.md"),
    target: path.join(PACKAGE_ROOT, "DISTRIBUTION_NOTICE.md")
  },
  {
    source: path.join(ROOT, "reports", "README.md"),
    target: path.join(PACKAGE_ROOT, "reports", "README.md")
  }
];

function assertInside(child, parent) {
  const relative = path.relative(parent, child);
  if (!relative || relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Refusing to operate outside ${parent}: ${child}`);
  }
}

function assertExists(source) {
  if (!fs.existsSync(source)) {
    throw new Error(`Required package input is missing: ${path.relative(ROOT, source)}`);
  }
}

function resolveElectronExecutable() {
  assertExists(ELECTRON_MODULE);
  const electronExecutable = require(ELECTRON_MODULE);
  assertExists(electronExecutable);
  return electronExecutable;
}

function copyPath(source, target) {
  assertExists(source);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, { recursive: true });
}

function writeLauncher() {
  const launcher = [
    "@echo off",
    "setlocal",
    'cd /d "%~dp0"',
    'if not exist "web-app\\node_modules\\electron\\dist\\electron.exe" (',
    "  echo Electron runtime was not found in this local package.",
    "  exit /b 1",
    ")",
    '"web-app\\node_modules\\electron\\dist\\electron.exe" "web-app\\electron\\main.cjs"',
    ""
  ].join("\r\n");
  fs.writeFileSync(path.join(PACKAGE_ROOT, "START_ONOKO_ARCANA.cmd"), launcher, "utf8");
}

function writeDesktopShortcutScript() {
  const shortcutScript = [
    "param(",
    '  [string] $DesktopPath = [Environment]::GetFolderPath("Desktop")',
    ")",
    "",
    '$ErrorActionPreference = "Stop"',
    '$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path',
    '$ElectronExe = Join-Path $PackageRoot "web-app\\node_modules\\electron\\dist\\electron.exe"',
    '$EntryPoint = Join-Path $PackageRoot "web-app\\electron\\main.cjs"',
    '$WorkingDirectory = Join-Path $PackageRoot "web-app"',
    '$IconPath = Join-Path $PackageRoot "assets\\generated\\app-icons\\onoko-arcana-app-icon-v1.ico"',
    '$ShortcutPath = Join-Path $DesktopPath "ONOKO ARCANA.lnk"',
    "",
    'foreach ($Required in @($ElectronExe, $EntryPoint, $WorkingDirectory, $IconPath)) {',
    "  if (!(Test-Path -LiteralPath $Required)) {",
    '    throw "Missing required file: $Required"',
    "  }",
    "}",
    "",
    "New-Item -ItemType Directory -Force -Path $DesktopPath | Out-Null",
    "",
    "$Shell = New-Object -ComObject WScript.Shell",
    "$Shortcut = $Shell.CreateShortcut($ShortcutPath)",
    "$Shortcut.TargetPath = $ElectronExe",
    '$Shortcut.Arguments = "`"$EntryPoint`""',
    "$Shortcut.WorkingDirectory = $WorkingDirectory",
    '$Shortcut.IconLocation = "$IconPath,0"',
    '$Shortcut.Description = "Launch ONOKO ARCANA desktop reading table"',
    "$Shortcut.WindowStyle = 1",
    "$Shortcut.Save()",
    "",
    "[PSCustomObject]@{",
    "  ok = $true",
    "  shortcut = $ShortcutPath",
    "  target = $Shortcut.TargetPath",
    "  arguments = $Shortcut.Arguments",
    "  icon = $Shortcut.IconLocation",
    "} | ConvertTo-Json",
    ""
  ].join("\r\n");
  fs.writeFileSync(path.join(PACKAGE_ROOT, "CREATE_DESKTOP_SHORTCUT.ps1"), shortcutScript, "utf8");
}

function main() {
  copyEntries.forEach((entry) => assertExists(entry.source));
  const electronExecutable = resolveElectronExecutable();

  fs.mkdirSync(DIST, { recursive: true });
  assertInside(PACKAGE_ROOT, DIST);
  fs.rmSync(PACKAGE_ROOT, { recursive: true, force: true });
  fs.mkdirSync(PACKAGE_ROOT, { recursive: true });

  copyEntries.forEach((entry) => copyPath(entry.source, entry.target));
  writeLauncher();
  writeDesktopShortcutScript();

  const manifest = {
    app: "ONOKO_ARCANA",
    packageType: "local-electron-folder",
    output: path.relative(ROOT, PACKAGE_ROOT),
    launcher: "START_ONOKO_ARCANA.cmd",
    desktopShortcutScript: "CREATE_DESKTOP_SHORTCUT.ps1",
    electronEntry: "web-app/electron/main.cjs",
    electronExecutable: path.relative(ROOT, electronExecutable),
    appIcon: "assets/generated/app-icons/onoko-arcana-app-icon-v1.ico",
    appUserModelId: "com.onoko.arcana",
    license: "Split license. See LICENSE and DISTRIBUTION_NOTICE.md.",
    assetReuse: "Project artwork, generated visuals, app icons, and ONOKO ARCANA identity assets are not granted for reuse outside this project.",
    historyStorage: "Electron localStorage key onoko-arcana:desktop:history:v1",
    copiedAt: new Date().toISOString(),
    copiedEntries: copyEntries.map((entry) => path.relative(ROOT, entry.source))
  };
  const manifestPath = path.join(PACKAGE_ROOT, "package-manifest.json");
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

  console.log(JSON.stringify({
    ok: true,
    package: path.relative(ROOT, PACKAGE_ROOT),
    launcher: path.relative(ROOT, path.join(PACKAGE_ROOT, "START_ONOKO_ARCANA.cmd")),
    desktopShortcutScript: path.relative(ROOT, path.join(PACKAGE_ROOT, "CREATE_DESKTOP_SHORTCUT.ps1")),
    manifest: path.relative(ROOT, manifestPath)
  }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(JSON.stringify({
    ok: false,
    message: error instanceof Error ? error.message : String(error)
  }, null, 2));
  process.exit(1);
}

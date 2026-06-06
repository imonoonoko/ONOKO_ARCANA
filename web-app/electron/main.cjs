const { app, BrowserWindow, shell } = require("electron");
const path = require("node:path");

const allowedExternalHost = "github.com";
const allowedExternalPathPrefix = "/imonoonoko/ONOKO_ARCANA";

const iconDir = path.join(
  __dirname,
  "..",
  "..",
  "assets",
  "generated",
  "app-icons"
);
const windowIcon = path.join(
  iconDir,
  process.platform === "win32"
    ? "onoko-arcana-app-icon-v1.ico"
    : "onoko-arcana-app-icon-v1.png"
);

app.setName("ONOKO ARCANA");
if (process.platform === "win32") {
  app.setAppUserModelId("com.onoko.arcana");
}

function isAllowedExternalUrl(input) {
  try {
    const url = new URL(input);
    return (
      url.protocol === "https:" &&
      url.hostname === allowedExternalHost &&
      (
        url.pathname === allowedExternalPathPrefix ||
        url.pathname.startsWith(`${allowedExternalPathPrefix}/`)
      )
    );
  } catch {
    return false;
  }
}

function openAllowedExternalUrl(url) {
  if (!isAllowedExternalUrl(url)) return false;
  shell.openExternal(url);
  return true;
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1440,
    height: 920,
    minWidth: 1100,
    minHeight: 760,
    backgroundColor: "#03070c",
    title: "ONOKO ARCANA",
    icon: windowIcon,
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true
    }
  });

  win.webContents.setWindowOpenHandler(({ url }) => {
    openAllowedExternalUrl(url);
    return { action: "deny" };
  });

  win.webContents.on("will-navigate", (event, url) => {
    if (url.startsWith("file://")) return;
    event.preventDefault();
    openAllowedExternalUrl(url);
  });

  win.loadFile(path.join(__dirname, "..", "index.html"));
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

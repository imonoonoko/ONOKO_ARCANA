const { app, BrowserWindow } = require("electron");
const path = require("node:path");

const windowIcon = path.join(
  __dirname,
  "..",
  "..",
  "assets",
  "generated",
  "card-production-v5-full",
  "web-labeled",
  "alpha",
  "card-back-onoko-v5-alpha.png"
);

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

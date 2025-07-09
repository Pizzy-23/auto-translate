const { app, BrowserWindow } = require("electron");
const path = require("path");

const isDev = process.argv.includes("--dev");

if (isDev) {
  try {
    require("electron-reloader")(module, {
      ignore: [path.join(__dirname, "..", "node_modules"), "..\\.git"],
    });
  } catch (_) {
    console.log("Error: electron-reloader não pôde ser carregado.");
  }
}

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile("index.html");

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", function () {
  if (process.platform !== "darwin") app.quit();
});

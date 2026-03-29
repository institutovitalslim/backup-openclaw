import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const cdpUrl = process.env.ENDOGIN_CDP_URL;
const outputPath = process.env.ENDOGIN_OUTPUT_PATH;
const seconds = Number(process.env.ENDOGIN_CAPTURE_SECONDS || "15");
const recorderUrl = process.env.ENDOGIN_RECORDER_URL;

if (!cdpUrl || !outputPath || !recorderUrl) {
  console.error("Required env vars: ENDOGIN_CDP_URL, ENDOGIN_OUTPUT_PATH, ENDOGIN_RECORDER_URL");
  process.exit(1);
}

const browser = await chromium.connectOverCDP(cdpUrl);
const context = browser.contexts()[0];
const page = await context.newPage();

try {
  await page.goto(`${recorderUrl}?seconds=${seconds}`, { waitUntil: "domcontentloaded" });
  console.log("[tab-share] click Iniciar captura and choose the Endogin tab with audio");
  await page.locator("#start").click();
  await page.waitForFunction(() => {
    const el = document.getElementById("status");
    return el && (el.textContent === "done" || el.textContent.startsWith("error:"));
  }, null, { timeout: (seconds + 120) * 1000 });
  const status = await page.locator("#status").textContent();
  if (!status || status.startsWith("error:")) throw new Error(status || "capture failed");
  const base64 = await page.locator("#payload").inputValue();
  console.log(`[tab-share] status=${status} payload_chars=${base64.length}`);
  await fs.writeFile(`${outputPath}.base64.txt`, base64, "utf8");
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  await fs.writeFile(outputPath, Buffer.from(base64, "base64"));
  console.log(outputPath);
} finally {
  await browser.close().catch(() => {});
}

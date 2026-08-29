const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runAudit() {
  console.log("Starting browser audit...");
  const browser = await chromium.launch({ headless: true });
  
  // Create output directory for screenshots
  const outDir = path.join(__dirname, 'public', 'screenshots');
  if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
  }

  const url = 'http://localhost:3001'; // We will run it on 3001 to avoid conflicts

  // Desktop
  console.log("Testing Desktop 1440x900...");
  const desktopContext = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const desktopPage = await desktopContext.newPage();
  
  // Capture console errors
  const consoleErrors = [];
  desktopPage.on('console', msg => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  desktopPage.on('pageerror', err => {
    consoleErrors.push(err.message);
  });

  await desktopPage.goto(url);
  await desktopPage.waitForLoadState('networkidle');
  await desktopPage.waitForTimeout(2000); // let animations settle
  await desktopPage.screenshot({ path: path.join(outDir, 'presentation-desktop.png'), fullPage: true });

  // Tablet
  console.log("Testing Tablet 1024x768...");
  const tabletContext = await browser.newContext({ viewport: { width: 1024, height: 768 } });
  const tabletPage = await tabletContext.newPage();
  await tabletPage.goto(url);
  await tabletPage.waitForLoadState('networkidle');
  await tabletPage.screenshot({ path: path.join(outDir, 'presentation-tablet.png'), fullPage: true });

  // Mobile
  console.log("Testing Mobile 390x844...");
  const mobileContext = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto(url);
  await mobilePage.waitForLoadState('networkidle');
  await mobilePage.screenshot({ path: path.join(outDir, 'presentation-mobile.png'), fullPage: true });

  // Reduced Motion
  console.log("Testing Reduced Motion...");
  const rmContext = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
  const rmPage = await rmContext.newPage();
  await rmPage.goto(url);
  await rmPage.waitForLoadState('networkidle');
  
  // Section audit helper
  const sections = await desktopPage.$$eval('section', els => els.map(e => e.id || e.className));
  
  console.log("--- AUDIT RESULTS ---");
  console.log(`Console Errors: ${consoleErrors.length}`);
  if (consoleErrors.length > 0) console.log(consoleErrors);
  console.log(`Number of sections found: ${sections.length}`);
  
  await browser.close();
  console.log("Audit complete.");
}

runAudit().catch(console.error);

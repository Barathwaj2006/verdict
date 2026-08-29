const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runTest() {
  console.log("Starting browser validation...");
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    colorScheme: 'dark',
  });
  const page = await context.newPage();

  try {
    // 1. Landing Page Test
    console.log("Testing Landing Page...");
    await page.goto('http://localhost:3000');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'landing-desktop.png' });
    console.log("Captured landing-desktop.png");

    // 2. Start a Real Investigation
    console.log("Starting investigation...");
    await page.fill('textarea', 'Find the strongest project idea for a hackathon. I am a solo developer with three days to build. I want strong differentiation, real-world impact, and a memorable demo.');
    await page.click('button[type="submit"]');
    
    // Wait for workspace page to load and SSE connection to establish
    console.log("Waiting for workspace to load...");
    await page.waitForURL(/.*\/workspace\/.*/, { timeout: 30000 });
    
    // Let the demo investigation run
    console.log("Waiting for investigation activity (10s)...");
    await page.waitForTimeout(10000);
    
    // Desktop Workspace Capture
    await page.screenshot({ path: 'workspace-desktop.png' });
    console.log("Captured workspace-desktop.png");

    // Desktop Final Verdict Capture
    await page.screenshot({ path: 'final-verdict.png', fullPage: true });
    console.log("Captured final-verdict.png");
    
    // Mobile Workspace Capture (simulate mobile)
    const mobileContext = await browser.newContext({
        viewport: { width: 390, height: 844 },
        isMobile: true
    });
    const mobilePage = await mobileContext.newPage();
    const url = page.url();
    await mobilePage.goto(url);
    await mobilePage.waitForLoadState('networkidle');
    await mobilePage.waitForTimeout(2000); // Wait for state
    await mobilePage.screenshot({ path: 'workspace-mobile.png', fullPage: true });
    console.log("Captured workspace-mobile.png");

    // Reduced Motion / 2D Fallback Capture
    const reducedMotionContext = await browser.newContext({
        viewport: { width: 1280, height: 720 },
        colorScheme: 'dark',
        reducedMotion: 'reduce'
    });
    const fallbackPage = await reducedMotionContext.newPage();
    await fallbackPage.goto(url);
    await fallbackPage.waitForLoadState('networkidle');
    await fallbackPage.waitForTimeout(2000); // Wait for state
    await fallbackPage.screenshot({ path: 'workspace-2d.png' });
    console.log("Captured workspace-2d.png");

    console.log("Validation complete.");

  } catch (e) {
    console.error("Test failed: ", e);
  } finally {
    await browser.close();
  }
}

runTest();

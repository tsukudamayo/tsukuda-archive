const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
	headless: false,
	slowMo: 50,
    });

    const page = await browser.newPage();

    await page.setViewport({
	width: 1200,
	height: 800,
    });

    await page.goto('https://www.shuwasystem.co.jp');

    await page.waitForSelector('#gs_tti50 .gsc-input');

    await page.type('#gs_tti50 .gsc-input', 'Puppeteer');

    await browser.close();
})();

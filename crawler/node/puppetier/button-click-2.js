const puppeteer = require('puppeteer');

(async() => {
    const browser = await puppeteer.launch({
	headless: false,
	slowMo: 50,
    });

    const page = await browser.newPage();

    await page.setViewport({
	width: 1200,
	height: 800,
    });

    await page.goto('http://www.google.co.jp/');

    await page.type('input[name=q]', 'Puppeteer API');

    await page.focus('input[name=btnK]');

    await page.click('input[name=btnK]');

    await browser.close();
})();

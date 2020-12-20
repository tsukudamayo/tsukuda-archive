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

    await page.goto('https://www.shuwasystem.co.jp/');

    await page.waitForSelector('#newbook');

    const newBook = await page.evaluate((selector) => {
	return document.querySelector(selector).innerHTML;
    }, '#newbook');

    console.log(newBook);

    await browser.close();
})();

const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch(
	{
	headless: false,
	slowMo: 50,
    });

    const page = await browser.newPage();

    await page.setViewport({
	width: 1200,
	height: 800,
    });

    await page.goto('https://www.shuwasystem.co.jp/');
    const imgTags = await page.$$('img');
    for (const imgTag of imgTags) {
	const src = await imgTag.getProperty('src');
	console.log(await src.jsonValue());
    }

    await browser.close();
})();

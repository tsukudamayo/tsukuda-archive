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

    const newbookImages = await page.$$('#newbook img');

    for (imgTag of newbookImages) {
	const prop = await imgTag.getProperty('src');
	const src = await prop.jsonValue();
	console.log(src);
    }

    await browser.close();
})();

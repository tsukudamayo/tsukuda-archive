const puppeteer = require('puppeteer');
const delay = require('delay');

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

    console.log('---------- go to ----------');
    await page.goto('https://www.yahoo.co.jp/');
    await delay(1000);

    console.log('---------- wait and click ----------');
    await Promise.all([
	page.waitForNavigation({ waitUntil: 'load' }),
	page.click('#topicsfb .topicsindex ul.emphasis li:nth-child(1) a'),
    ]);

    console.log('---------- evaluate ----------');
    const h2Title = await page.evaluate(
	() => document.querySelector('h2.newsTitle').textContent
    );
    console.log(h2Title);

    console.log('---------- close ----------');

    await browser.close();
})();
    

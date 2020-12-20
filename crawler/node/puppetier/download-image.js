const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

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

    await page.goto('https://www.google.co.jp/');

    // get img tag
    const image = await page.$('#lga img');
    console.log(image);

    // get src tag
    const src = await image.getProperty('src');
    console.log(src);

    // get JSHandle object
    const targetUrl = await src.jsonValue();
    console.log(`targetUrl=${targetUrl}`);

    // get filename
    const filename = targetUrl.split('/').pop();
    console.log(`filename=${filename}`);

    const localfilefullpath = path.join(__dirname, filename);
    console.log(`localfilename=${localfilefullpath}`);

    const viewSource = await page.goto(targetUrl);
    fs.writeFile(localfilefullpath, await viewSource.buffer(), (error) => {
	if (error) {
	    console.log(`error=${error}`);
	    return;
	}
	console.log('The file was saved');
    });

    await browser.close();
})();

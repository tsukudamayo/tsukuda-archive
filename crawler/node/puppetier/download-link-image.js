const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

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

    await page.goto('https://mainichi.jp/graphs/20180612/hpj/00m/040/001000g/1');

    const image = await page.$('#main > article > div > figure > div > img');
    console.log(image);

    const src = await image.getProperty('src');
    console.log(src);

    const targeturl = await src.jsonValue();
    console.log(`targeturl=${targeturl}`);

    const filename = targeturl.split('/').pop().split('?').shift();

    const localfilefullpath = path.join(__dirname, filename);

    const viewSource = await page.goto(targeturl);
    fs.writeFile(localfilefullpath, await viewSource.buffer(), (error) => {
	if(error) {
	    console.log(`error=${error}`);
	    return;
	}
	console.log('The file was saved!');
    });

    await browser.close();
})();

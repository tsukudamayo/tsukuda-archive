const puppeteer = require('puppeteer');
const delay = require('delay');
require('dotenv').config();

const USER_ID = process.env.MY_USER_ID;
const PASSWORD = process.env.MY_PASSWORD;

(async () => {
    const browser = await puppeteer.launch({
	headless: false,
	slowMo: false,
    });

    const page = await browser.newPage();

    await page.setViewport({
	width: 1200,
	height: 800,
    });

    await page.goto('https://mail.pactera.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.pactera.com%2fowa%2f%3fmodurl%3d0');
    await delay(1000);

    // login
    await page.type('input[id="username"]', USER_ID);
    await page.type('input[id="password"]', PASSWORD);
    page.click('input[type="submit"]');
    await delay(5000);

    // await page.waitForSelector('#divTrNdHl');

    // const newPage = await page.evaluate((selector) => {
    // 	return document.querySelector(selector).innerHTML;
    // }, '#divTrNdHl');
    // console.log(newPage);

    const xpath = `//*[@id="fLgAAAAB/BEkDkhKJSJceomj1EzHJAQB36ypeyJ2CSrrlQYOygWzIAAAAHiFLAAAB"]`;
    await page.waitForXPath(xpath);
    await (await page.$x(xpath))[0].click();

    await delay(3000);
    // // get mail titles
    // const mailTitles = await page.evaluate(() => {
    // 	const node = document.querySelectorAll('#divSubject');
    // 	const titleArray = [];
    // 	for (item of node) {
    // 	    titleArray.push(item.innerText);
    // 	    console.log(item);
    // 	}
    // 	return titleArray;
    // });
    // console.log(mailTitles);

    // for (title of mailTitles) {
    // 	const pattern = '作業報告';
    // 	if (title.includes(pattern)) {
    // 	    console.log(title);
    // 	}
    // };

    const mailUrls = await page.$$('#divSubject');

    var i = 0;
    for (var mailUrl of mailUrls) {
    	console.log(mailUrl);
    	await mailUrl.click();
    	i += 1;
    	await delay(100);
    }

    // for(const mailUrl of mailUrls) {
    // 	const div = await mailUrl.getProperty('div');
    // 	console.log(await div.jsonValue());
    // }

    // TODO get mailTitles url

    // const title = await page.evaluate('#divSubject', item => {
    // 	return item.textContent;
    // });
    // console.log(title);
    

    // wait page navigation
    // await page.waitFor('span[id="spnFldrNm"]', {timeout: 120000});
    
    // const data = await page.$eval('span', el => el.value);
    // console.log(data);

    // await browser.close();
})();

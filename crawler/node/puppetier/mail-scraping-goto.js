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

    await page.goto('https://mail.pactera.com/owa/?ae=Item&a=Open&t=IPM.Note&id=RgAAAAB%2fBEkDkhKJSJceomj1EzHJBwB36ypeyJ2CSrrlQYOygWzIAAAAHiFLAAB36ypeyJ2CSrrlQYOygWzIAAATz0gLAAAA&pspid=_1545968168099_198630365');
    await delay(3000);

    await page.goto('https://mail.pactera.com/owa/?ae=Item&a=Open&t=IPM.Note&id=RgAAAAB%2fBEkDkhKJSJceomj1EzHJBwB36ypeyJ2CSrrlQYOygWzIAAAAHiFLAAB36ypeyJ2CSrrlQYOygWzIAAATz0gMAAAA&pspid=_1545968496548_800644464');
    await delay(3000);

    await page.goto('https://mail.pactera.com/owa/?ae=Item&a=Open&t=IPM.Note&id=RgAAAAB%2fBEkDkhKJSJceomj1EzHJBwB36ypeyJ2CSrrlQYOygWzIAAAAHiFLAAB36ypeyJ2CSrrlQYOygWzIAAATz0gJAAAA&pspid=_1545968496548_800644464');
    await delay(3000);

    await page.goto('https://mail.pactera.com/owa/?ae=Item&a=Open&t=IPM.Note&id=RgAAAAB%2fBEkDkhKJSJceomj1EzHJBwB36ypeyJ2CSrrlQYOygWzIAAAAHiFLAAB36ypeyJ2CSrrlQYOygWzIAAATz0gIAAAA&pspid=_1545968496548_800644464')
    await delay(3000);
    
})();

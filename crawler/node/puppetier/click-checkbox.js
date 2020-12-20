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

    await page.goto('http://3min.ntv.co.jp/3min/search_option/');

    await page.click(
	'#main >' +
        'div >' +
        'div.inner >' +
        'form > ' +
        'div:nth-child(6) > ' +
        'div:nth-child(3) > ' +
        'ul > ' +
        'li:nth-child(3) > ' +
        'label > ' +
        'input[type="checkbox"]'
    );

    await browser.close();
})();

    

    
    

const puppeteer = require('puppeteer');
const delay = require('delay');
const fs = require('fs');

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

  for (let index = 365; index < 10000; index++) {
    await page.goto(
      'https://www.weekcook.jp/recipe/' + String(index) + '/index.html'
    );
    await delay(1000);

    let textList = [];
    let xpath = '/html/body/div[2]/div[2]/div[1]/div[2]/div';
    // await page.waitForXPath(xpath);

    const elementHandleList = await page.$x(xpath);
    // console.log(elementHandleList);

    for (let index=0; index < elementHandleList.length; index++) {
      let value = await(await elementHandleList[index].getProperty('textContent'))
	  .jsonValue();
      // console.log(index);
      // console.log(value);
      textList.push(value);
    }
    console.log('textList');
    console.log(textList);

    // make directory if dataDir does not exist
    var recipeDir = 'data/weekcook_ingredient';
    try {
      fs.statSync(recipeDir);
      console.log('pass mkdir data');
    } catch (error) {
      if (error.code === 'ENOENT') {
	console.log('mkdir data');
	fs.mkdirSync(recipeDir);
      } else {
	console.log(error);
      }
    }

    // define filepath and filename
    console.log(index);
    var zeroPadding = '00000000' + String(index);
    var length = 8;
    var indexNumber = zeroPadding.slice(-length);
    var fname = recipeDir + '/' + 'weekcook_' + indexNumber + '.txt';

    fs.writeFile(fname, textList, 'utf8', (err) => {
      if (err) {
	console.log(fname);
	console.log(textList);
      } else {
	console.log(err);
      }
    });
    
  }

  await browser.close();
})();

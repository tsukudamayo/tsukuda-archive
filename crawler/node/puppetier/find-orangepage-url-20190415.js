const puppeteer = require('puppeteer');
const delay = require('delay');
const fs = require('fs');
const csvSync = require('csv-parse/lib/sync');


const readFile = __dirname + '/target_orangepage_url_20190415.csv';
let data = fs.readFileSync(readFile);
let allRecipeUrl = csvSync(data);

console.log(allRecipeUrl);

for(let recipeUrl of allRecipeUrl) {
    console.log(recipeUrl[0]);
}

(async () => {
    // pupeeteer settings
    const browser = await puppeteer.launch({
	headless: false,
	slowMo: 50,
    });

    const page = await browser.newPage();

    await page.setViewport({
	width: 1200,
	height: 800,
    });

    // start scraping
    for (let recipeUrl of allRecipeUrl) {
	console.log(recipeUrl[0]);
        await page.goto(
	    recipeUrl[0]
	);
        await delay(1000);

	let textList = [];
	let xpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[3]/div/div/div[1]';
	await page.waitForXPath(xpath);
	
	const elementHandleList = await page.$x(xpath);
	// console.log(elementHandleList);
	for (let index=0; index < elementHandleList.length; index++) {
	    let value = await(
		await elementHandleList[index].getProperty('textContent'))
		.jsonValue();
	    console.log(index);
	    console.log(value);
	    value = value.replace(/ /g, '');	    
	    value = value.replace(/\n*作り方\n*\n/g, '');
	    value = value.replace(/\n*\n/g, '\n');
	    textList.push(value);
	}
	console.log('textList');
	console.log(textList);

	// make directory if dataDir does not exist
	var dataDir = 'data';
	try {
	    fs.statSync(dataDir);
	    console.log('pass mkdir data');
	} catch (error) {
	    if (error.code === 'ENOENT') {
		console.log('mkdir data');
		fs.mkdirSync(dataDir);
	    } else {
		console.log(error);
	    }
	}

	// make directory if recipeDir does not exist
	var recipeDir = 'data/orangepage_recipe';
	try {
	    fs.statSync(recipeDir);
	    console.log('pass mkdir recipeDir');
	} catch (error) {
	    if (error.code === 'ENOENT') {
		console.log('mkdir recipeDir');
		fs.mkdirSync(recipeDir);
	    } else {
		console.log(error);
	    }
	}

	// define filepath and filename
	var fheader = recipeUrl[0].split('/')[4];
	console.log('fheader');
	console.log(fheader);
	var fname = recipeDir + '/' + fheader + '.txt';

	// output recipe to text
	fs.writeFile(fname, textList, 'utf8', (err) => {
	    if (err) {
		console.log(fname);
		console.log(textList);
	    } else {
		console.log(err);
	    }
	});
    }

    // await page.type('#gs_tti50 .gsc-input', 'Puppeteer');

    await browser.close();
})();

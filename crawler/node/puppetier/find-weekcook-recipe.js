const puppeteer = require('puppeteer');
const delay = require('delay');
const fs = require('fs');

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
    for (let index = 1; index < 9999; index++) {
        await page.goto(
            'https://www.weekcook.jp/recipe/' + String(index) + '/index.html'
        );
        
        await delay(1000);

        const allRecipe = await page.evaluate(() => {
            const node = document.querySelectorAll(
                'body > div.contents-all.recipe > div:nth-child(3) > div.howto'
            );
            console.log('accsess recipe div');
            console.log(node);
            const recipeStrings = [];
        
            // access recipe data
            for (item of node) {
                var recipeString = item.innerText;
                // recipeString = recipeString.replace
                recipeString = recipeString.replace(
                    /作り方\n/g, ''
                );
            }
            recipeStrings.push(recipeString);
            return recipeStrings;
        });
        console.log(allRecipe);

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
        var recipeDir = 'data/weekcook_recipe';
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
        console.log(index);
        var zeroPadding = '00000000' + String(index);
        var length = 8;
        var indexNumber = zeroPadding.slice(-length);
        var fname = recipeDir + '/' + 'weekcook_' + indexNumber + '.txt';

        // output recipe to text
        try {
            fs.writeFile(fname, allRecipe, 'utf8', (err) => {
                if (err) {
                    console.log(fname);
                    console.log(allRecipe);
                } else {
                    console.log(err);
                }
            });
        } catch(e) {
            console.log('!!!!!!!!!!!!!!!! error !!!!!!!!!!!!!!!!');
            continue;
        }
    }

    // await page.type('#gs_tti50 .gsc-input', 'Puppeteer');

    await browser.close();
})();

const puppeteer = require('puppeteer');
const delay = require('delay');
const fs = require('fs');

const TIMEOUT_THRESHOLD = 300000;

const ingredientDispatcher = (element) => {
  if (element === '材料（2人分4人分）') {
    return 'servings2and4';
  }
  if (element === '材料（2人分）') {
    return 'servings2';
  }
  if (element === '材料（4人分）') {
    return 'servings4';
  }
  if (element.match(/^　/)) {
    return 'subingredients';
  }
  return 'ingredients';
};

const servingsReplace = (element) => {
  let keyvaluePair = element.split('材料');
  let key = '材料';
  let value = keyvaluePair[1].replace(/（/g, '');
  value = value.replace(/）/g, '');
  return [key, value];
};

const ingredientsReplace = (element) => {
  let key;
  let value;
  let keyvaluePair = element.split('　');
  if (keyvaluePair.length !== 1) {
    key = keyvaluePair[0];
    value = keyvaluePair[1];
    return [key, value];
  } else {
    key = element;
    value = '';
    return [key, value];
  }
};

const makeDirIfNotExists = (dataDir) => {
  // make directory if dataDir does not exist
  try {
    fs.statSync(dataDir);
  } catch (error) {
    if (error.code === 'ENOENT') {
      fs.mkdirSync(dataDir);
    } else {
      console.log(error);
    }
  }
};

const specifyOutputPath = (index, dataDir) => {
  // define filepath and filename
  let fheader = String(index);
  let filePath = dataDir + '/detail_' + fheader + '.json';

  return filePath;
};

const outputData = (data, filePath) => {
  // output recipe to text
  fs.writeFile(filePath, JSON.stringify(data, null, '    '), 'utf8', (err) => {
    if (err) {
      console.log(filePath);
    } else {
      console.log(err);
    }
  });
};

// main process
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
  let targetStrings;
  let cookingTime;
  let recipeCalory;
  let recipeSalt;
  let elementHandleList;
  let titleXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/h1';
  let recipeXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[3]/div/div/div[1]';
  let timeXPath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[1]/ul/li[1]/time';
  let ingredientsXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[2]/div';
  let caloryXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[1]/ul/li[2]/span[2]';
  let saltXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[1]/ul/li[3]';
  let imageXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[1]/img';

  for (let index = 301148; index < 400000; index++) {
    
    await page.goto(
      'https://www.orangepage.net/recipes/detail_' + String(index),
      {timeout: TIMEOUT_THRESHOLD}
    );
    await delay(1000);

    // ignore 404
    let currentURL = page.url();
    if (currentURL === 'https://www.orangepage.net/404.html') {
      console.log('recipe %s returns 404 Error', index);
      continue;
    }
    console.log('recipe index : ', index);

    await page.waitForXPath(recipeXpath);

    let title;
    elementHandleList = await page.$x(titleXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      title = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
    }
    console.log('title : ', title);

    // scraping recipe
    let textList = [];
    elementHandleList = await page.$x(recipeXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      targetStrings = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
      targetStrings = targetStrings.replace(/ /g, '');
      targetStrings = targetStrings.replace(/\n*作り方\n*\n/g, '');
      targetStrings = targetStrings.replace(/\n*\n/g, '\n');
      textList.push(targetStrings);
    }
    console.log(textList);

    // time
    let hasCookingTime = true;
    elementHandleList = await page.$x(timeXPath);
    for (let index=0; index < elementHandleList.length; index++) {
      if (elementHandleList.length === 0) {
        hasCookingTime = false;
        cookingTime = '';
        break;
      }
      targetStrings = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
      cookingTime = targetStrings;
      console.log('cookingTime : ', cookingTime);
    }

    // calory
    let hasCalory = true;
    elementHandleList = await page.$x(caloryXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      if (elementHandleList.length === 0) {
        hasCalory = false;
        recipeCalory = '';
        break;
      }
      targetStrings = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
      recipeCalory = targetStrings;
      recipeCalory = recipeCalory.split(' ');
      recipeCalory = recipeCalory[1];
      console.log('recipeCalory : ', recipeCalory);
    }

    // salt
    let hasSalt = false;
    elementHandleList = await page.$x(saltXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      if (elementHandleList.length === 0) {
        hasSalt = false;
        recipeSalt = '';
        break;
      }
      targetStrings = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
      recipeSalt = targetStrings;
      recipeSalt = recipeSalt.replace(/\n    /g, '');
      recipeSalt = recipeSalt.split(' ')[1];
      console.log('recipeSalt : ', recipeSalt);
    }

    // scraping ingredients
    let ingredientList = [];
    let ingredientsEnum = {};
    let ingredients;
    let replaceArray;

    // ingredients textContent to Array
    elementHandleList = await page.$x(ingredientsXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      let targetStrings = await(await elementHandleList[index].getProperty('textContent')).jsonValue();
      targetStrings = targetStrings.replace(/ /g, '');
      ingredients = targetStrings.split('\n');
      ingredients = ingredients.filter(Boolean);
    }
    console.log('ingredients textContent to Array/ingredients : ', ingredients);
    // ingredients = ingredients.map((element) => {
    //   replaceArray = element.replace(/^　/g, '');
    //   return replaceArray;
    // });

    // ingredients Array to Enum
    let key;
    let value;
    let keyvaluePair;
    let subIngredientsKey;
    let subIngredientsEnum;
    let subIngredintsFlg = false;

    const generateIngredinetsEnum = (keyvaluePair, ingredientsEnum) => {
      key = keyvaluePair[0];
      value = keyvaluePair[1];
      console.log('key - value : ', key + ' - ' + value);
      ingredientsEnum[key] = value;
      return;
    };

    ingredients.forEach((element, index, array) => {

      let dispatcher = ingredientDispatcher(element);
      console.log('diapathcer : ', dispatcher);

      if (subIngredintsFlg && dispatcher !== 'subingredients') {
        ingredientsEnum[subIngredientsKey] = subIngredientsEnum;
        subIngredintsFlg = false;
      }

      switch(dispatcher) {
      case 'servings2':
        keyvaluePair = servingsReplace(element);
        generateIngredinetsEnum(keyvaluePair, ingredientsEnum);
        break;
      case 'servings4':
        keyvaluePair = servingsReplace(element);
        generateIngredinetsEnum(keyvaluePair, ingredientsEnum);
        break;
      case 'servings2and4':
        keyvaluePair = servingsReplace(element);
        generateIngredinetsEnum(keyvaluePair, ingredientsEnum);
        break;
      case 'ingredients':
        keyvaluePair = ingredientsReplace(element);
        generateIngredinetsEnum(keyvaluePair, ingredientsEnum);
        break;
      case 'subingredients':
        if (!subIngredintsFlg) {
          subIngredintsFlg = true;
          subIngredientsEnum = {};
          subIngredientsKey = array[index - 1];
        }
        element = element.replace(/^　/g, '');
        keyvaluePair = ingredientsReplace(element);
        generateIngredinetsEnum(keyvaluePair, subIngredientsEnum);
        break;
      default:
        ;
      }

      if (subIngredintsFlg && (array.length - 1) === index) {
        ingredientsEnum[subIngredientsKey] = subIngredientsEnum;
      }
    });
    console.log(ingredientsEnum);

    // download image
    let imageUrl;
    elementHandleList = await page.$x(imageXpath);
    for (let index=0; index < elementHandleList.length; index++) {
      if (elementHandleList.length === 0) {
        break;
      }
      imageUrl = await(await elementHandleList[index].getProperty('src')).jsonValue();
      console.log('download image/targetStrings : ', imageUrl);
    }
    // // output image
    // makeDirIfNotExists('data');
    // makeDirIfNotExists('data/orangepage_recipe/img')
    // const ext = imageUrl.split('.').pop();
    // const fileName = currentURL.split('/').pop();
    // const downloadFilePath = 'data/orangepage_recipe/img/' + 'orangepage_' + fileName + '.' + ext;
    // const viewSource = await page.goto(imageUrl);
    // fs.writeFile(downloadFilePath, await viewSource.buffer(), (error) => {
    //   if (error) {
    //     console.log(`error="${error}`);
    //     return;
    //   }
    //   console.log('Image file ' + fileName + ' was saved');
    // });

    // result
    let recipeData = {
      title: title,
      url: currentURL,
      recipe: textList[0],
      time: cookingTime,
      calory: recipeCalory,
      salt: recipeSalt,
      ingredients: ingredientsEnum,
      imageurl: imageUrl
    };

    // output data
    makeDirIfNotExists('data');
    makeDirIfNotExists('data/orangepage_recipe');
    let filePath = specifyOutputPath(index, 'data/orangepage_recipe');
    outputData(recipeData, filePath);

    if (hasCookingTime === false) {
      continue;
    } else {
      ;
    }
    
  }
  // await page.type('#gs_tti50 .gsc-input', 'Puppeteer');
  await browser.close();
})();

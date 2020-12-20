const puppeteer = require('puppeteer');
const delay = require('delay');
const fs = require('fs');

const TIMEOUT_THRESHOLD = 300000;

const ingredientDispatcher = (element) => {
  if (element === '材料 （2人分4人分）') {
    return 'servings2and4';
  }
  if (element === '材料 （2人分）') {
    return 'servings2';
  }
  if (element === '材料 （4人分）') {
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
  let filePath = dataDir + '/' + fheader + '.json';

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

const tableToMap = (targetStrings) => {
  targetStrings = targetStrings.replace(/\t/g, '');
  targetStrings = targetStrings.replace(/\n*\n/g, '\n');
  targetStrings = targetStrings.split('\n');
  targetStrings = targetStrings.map((item) => {
    let splitItem = item.split('：');
    console.log('splitItem : ', splitItem);
    let tableKey = splitItem[0];
    let tableValue = splitItem[1];
    console.log('key : ', tableKey);
    return { "key" : tableKey, "value": tableValue };
  });

  return targetStrings;
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
  let titleXpath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/table[1]/tbody/tr[1]/td[2]/span[1]/h1';
  let recipeXpath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/div/table/tbody/tr[1]/td/span/table';
  let timeXPath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/table[1]/tbody/tr[2]/td';
  let ingredientsXpath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/table[2]/tbody/tr/td';
  let caloryXpath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/table[1]/tbody/tr[2]/td';
  let saltXpath = '/html/body/div[1]/div[6]/div[1]/div/div[1]/div[2]/div[1]/ul/li[3]';
  let imageXpath = '/html/body/div/div/table/tbody/tr[2]/td[1]/div/table[1]/tbody/tr[1]/td[1]/img';

  var urlFoundCount = 0;
  var notFoundCount = 0;

  for (let index = 10000000; index < 999999999; index++) {

    var urlNumber = ('0000000000' + String(index)).slice(-9);
    console.log('urlNumber : ', urlNumber);

    await page.goto(
      // 'https://www.bh-recipe.jp/recipe/' + String(index) + '.html',
      'https://www.bh-recipe.jp/recipe/' + urlNumber + '.html',
      {timeout: TIMEOUT_THRESHOLD}
    );
    await delay(1000);

    const currentURL = page.url();

    // ignore 404

    let currentTitle = elementHandleList = await page.$x(caloryXpath);
    if (currentTitle.length === 0) {
      console.log('recipe %s returns 404 Error', index);
      notFoundCount += 1;
      console.log('notFoundCount : ', notFoundCount);
      if (notFoundCount === 10) {
        index += 100000;        
        index -= (notFoundCount + urlFoundCount);
        notFoundCount = 0;
        urlFoundCount = 0;
      }
      continue;
    }
    urlFoundCount += 1;
    
    console.log('recipe index : ', index);

    await page.waitForXPath(recipeXpath);

    let title;
    elementHandleList = await page.$x(titleXpath);
    for (let idx=0; idx < elementHandleList.length; idx++) {
      title = await(await elementHandleList[idx].getProperty('textContent')).jsonValue();
    }
    console.log('title : ', title);

    // scraping recipe
    let textList = [];
    elementHandleList = await page.$x(recipeXpath);
    for (let idx=0; idx < elementHandleList.length; idx++) {
      targetStrings = await(await elementHandleList[idx].getProperty('textContent')).jsonValue();
      targetStrings = targetStrings.replace(/ /g, '');
      targetStrings = targetStrings.replace(/\n*作り方\n*\n/g, '');
      targetStrings = targetStrings.replace(/\t/g, '');
      targetStrings = targetStrings.replace(/\n*[0-9]*\n/g, '\n');
      targetStrings = targetStrings.replace(/^\n/g, '');
      textList.push(targetStrings);
    }
    console.log(textList);

    // time
    let hasCookingTime = true;
    elementHandleList = await page.$x(timeXPath);
    if (elementHandleList.length === 0) {
      hasCookingTime = false;
      cookingTime = '';
      break;
    }
    targetStrings = await(await elementHandleList[0].getProperty('textContent')).jsonValue();
    targetStrings = tableToMap(targetStrings);
    targetStrings = targetStrings.filter(function(item, index) {
      if (item.key == '調理時間') return true;
      return false;
    });
    targetStrings = targetStrings[0].value
    cookingTime = targetStrings;
    console.log('cookingTime : ', cookingTime);
      
    // calory
    let hasCalory = true;
    elementHandleList = await page.$x(caloryXpath);
    if (elementHandleList.length === 0) {
        hasCalory = false;
        recipeCalory = '';
        break;
    }
    targetStrings = await(await elementHandleList[0].getProperty('textContent')).jsonValue();
    targetStrings = tableToMap(targetStrings);
    targetStrings = targetStrings.filter(function(item, index) {
      if (item.key == 'カロリー') return true;
      return false;
    });
    targetStrings = targetStrings[0].value;
    recipeCalory = targetStrings;
    console.log('recipeCalory : ', recipeCalory);

    // salt
    let hasSalt = false;
    elementHandleList = await page.$x(saltXpath);
    for (let idx=0; idx < elementHandleList.length; idx++) {
      if (elementHandleList.length === 0) {
        hasSalt = false;
        recipeSalt = '';
        break;
      }
      targetStrings = await(await elementHandleList[idx].getProperty('textContent')).jsonValue();
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
    for (let idx=0; idx < elementHandleList.length; idx++) {
      targetStrings = await(await elementHandleList[idx].getProperty('textContent')).jsonValue();
      targetStrings = targetStrings.replace(/\t/g, '');
      targetStrings = targetStrings.replace(/\n*\n/g, '\n');
      targetStrings = targetStrings.replace(/^\n/g, '食材');
      targetStrings = targetStrings.replace(/〉/g, '');
      targetStrings = targetStrings.replace(/〈/g, '');
      targetStrings = targetStrings.replace(/ /g, '');
      targetStrings = targetStrings.replace(/\n\n/g, '');
      targetStrings = targetStrings.replace(/\n　　/g, '　');
      ingredients = targetStrings.split('\n');
      ingredients = ingredients.filter(Boolean);
    }
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
      console.log('dispatcher : ', dispatcher);

      if (subIngredintsFlg && dispatcher !== 'subingredients') {
        ingredientsEnum[subIngredientsKey] = subIngredientsEnum;
        subIngredintsFlg = false;
      }

      switch(dispatcher) {
      case 'ingredients':
        keyvaluePair = ingredientsReplace(element);
        generateIngredinetsEnum(keyvaluePair, ingredientsEnum);
        break;
      case 'subingredients':
        if (!subIngredintsFlg) {
          subIngredintsFlg = true;
          subIngredientsEnum = {};
          subIngredientsKey = array[index - 1];
          subIngredientsKey = subIngredientsKey.replace(/　/g, '');
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
      console.log('download image/imageUrl : ', imageUrl);
    }
    // output image
    makeDirIfNotExists('data');
    makeDirIfNotExists('data/betterhome_recipe');
    makeDirIfNotExists('data/betterhome_recipe/img');
    const ext = imageUrl.split('.').pop();
    const fileName = currentURL.split('/').pop();
    const downloadFilePath = 'data/betterhome_recipe/img/' + 'betterhome_' + fileName + '.' + ext;
    const viewSource = await page.goto(imageUrl);
    fs.writeFile(downloadFilePath, await viewSource.buffer(), (error) => {
      if (error) {
        console.log(`error="${error}`);
        return;
      }
      console.log('Image file ' + fileName + 'was saved');
    });

    // result
    let recipeData = {
      title: title,
      url: currentURL,
      recipe: textList[0],
      time: cookingTime,
      calory: recipeCalory,
      salt: recipeSalt,
      ingredients: ingredientsEnum
    };

    // output data
    makeDirIfNotExists('data');
    makeDirIfNotExists('data/betterhome_recipe');
    let filePath = specifyOutputPath(index, 'data/betterhome_recipe');
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

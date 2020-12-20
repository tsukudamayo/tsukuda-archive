import * as fs from "fs";
import * as path from "path";

const recipeDir = 'data/weekcook_recipe';
const dstDir = 'data/weekcook_recipe_random_choice';
const extFilter = 'txt';

const allFiles = fs.readdirSync(recipeDir);
const countFiles = Object.keys(allFiles).length;
console.log(countFiles);

const randomNum = Math.floor(Math.random() * countFiles);
console.log(randomNum);

if (!fs.existsSync(dstDir)) {
  fs.mkdirSync(dstDir);
}

var fname = allFiles[randomNum]

var filePath = recipeDir + '/' + fname;
console.log(filePath);

var dstPath = dstDir + '/' + fname;
fs.copyFileSync(filePath, dstPath);

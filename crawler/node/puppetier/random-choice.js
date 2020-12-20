"use strict";
exports.__esModule = true;
var fs = require("fs");
var recipeDir = 'data/weekcook_recipe';
var dstDir = 'data/weekcook_recipe_random_choice';
var extFilter = 'txt';
var allFiles = fs.readdirSync(recipeDir);
var countFiles = Object.keys(allFiles).length;
console.log(countFiles);
var randomNum = Math.floor(Math.random() * countFiles);
console.log(randomNum);
if (!fs.existsSync(dstDir)) {
    fs.mkdirSync(dstDir);
}
var fname = allFiles[randomNum];
var filePath = recipeDir + '/' + fname;
console.log(filePath);
var dstPath = dstDir + '/' + fname;
fs.copyFileSync(filePath, dstPath);

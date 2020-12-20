"use strict";
exports.__esModule = true;
var fs = require("fs");
var path = require("path");
var recipeDir = 'data/weekcook_ingredient';
var extFilter = 'txt';
function extension(element) {
    var extName = path.extname(element);
    return extName === '.' + extFilter;
}
;
function seekDir(dirpath) {
    fs.readdir(recipeDir, function (err, list) {
        if (list !== undefined) {
            list.filter(extension).forEach(function (file) {
                var filePath = dirpath + '/' + file;
                var fileStats = fs.statSync(filePath);
                var fileSize = fileStats.size;
                console.log(filePath);
                console.log(fileSize);
                if (fileSize === 0) {
                    fs.unlinkSync(filePath);
                    console.log('delete ' + filePath);
                }
                else {
                    console.log('file exist!');
                }
            });
        }
    });
}
seekDir(recipeDir);

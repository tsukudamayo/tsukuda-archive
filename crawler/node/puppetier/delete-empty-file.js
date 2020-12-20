const fs = require('fs');

var recipeDir = 'data/sample';
fs.readdir(recipeDir, function(err, files) {
  // console.log(files);
  if (err) throw err;
  var fileList = files.filter(function(file) {
    filePath = recipeDir + '/' + file;
    var fileStats = fs.statSync(filePath);
    var fileSize = fileStats.size
    console.log(filePath);
    console.log(fileStats.size);
    if (fileSize === 0) {
      fs.unlinkSync(filePath);
      console.log('delete ' + filePath);
      return true;
    } else {
      return false;
    }
  });
});

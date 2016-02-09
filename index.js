var fs = require('fs');
var spawn = require('child_process').spawn;
var express = require('express');
var app = express();
var router = express.Router();
var multer = require('multer');
var bodyParser = require('body-parser');
var mkdirp = require('mkdirp');


/**
*  File upload configuration of multer.
*  Targt dir is './uploads' and file limit size 15MB.
*/
var upload = multer({
  dest: './uploads/',
  limits: {
    fieldSize: '15MB',
    files: 1
  }
}).single('file');

app.set('port', (process.env.PORT || 5000));
app.use(express.static(__dirname, '/css'));
app.use(bodyParser.urlencoded({extended: false}));
app.use(router);

router.get('/', function(req, res, next) {
  res.sendFile(__dirname + '/index.html');
});

router.post('/upload', upload, function(req, res, next) {
  if (req.file && req.file.mimetype === 'audio/mp3') {
    var tmpPath = req.file.path;
    var targetPath = './uploads/' + req.file.originalname;
    var convertedPath = './uploads/' + 'CnS-' + req.file.originalname;

    mkdirp('./uploads/', function(err, result) {
      if (err) {
        throw err;
      }

      fs.rename(tmpPath, targetPath, function(err) {
        if (err) {
          throw err;
        }

        // Call Python script 'screw.py', wait for it to process song.
        var child = spawn('python', ['screw.py', targetPath, convertedPath]);

        // Handle python script errors
        child.stdout.on('data', function(data) {
          console.log('child_data: ' + data.toString());
        });

      	child.stderr.on('data', function(data) {
          console.log('child_stderr: ' + data.toString());
        });

        child.on('error', function(err) {
          console.log('child_error: ' + data.toString());
        });

        // Python script has finished executing.
        // Chopped and screwed song is ready for download.
        child.on('close', function(code, signal) {
          // Remove uploaded song.
          fs.unlink(targetPath, function(unlink_err) {
            if (unlink_err) {
              throw unlink_err;
            } else {
              // Prompt user for download.
              res.download(convertedPath, function() {
                // Remove chopped and screwed song.
                fs.unlink(convertedPath, function(err) {
                  if (err) {
                    console.log('unlink_err: ' + err.toString());
                    return res.redirect('/');
                  }
                });
              });
            }
          })
        });
      });
    });
  } else {
    // Just send them back to the starting page.
    res.redirect('/');
  }
});

app.get('*', function(req, res) {
  // Just send them back to the starting page.
  res.redirect('/');
});

app.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});

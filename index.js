var fs = require('fs');
var child_process = require('child_process');

var express = require('express');
var multer = require('multer');
var bodyParser = require('body-parser');
var mkdirp = require('mkdirp');
var app = express();


/**
 *  File upload configuration of multer.
 *  Targt dir is './uploads' and file limit size 10MB.
 */
var upload = multer({
    dest: './uploads/',
    limits: {
        fieldSize: '15MB'
    }
}).single('file');

function puts(err, stdout, stderr) {
    if (err) {
        console.log(stderr);
        console.log(stdout);
        console.log(err);

        throw err;
    }

    console.log(stdout);
}

app.set('port', (process.env.PORT || 5005));

app.use(bodyParser.urlencoded({extended: false}));

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.post('/upload', upload, function(req, res, next) {
    var username = req.body.username;
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
            res.send("File uploaded to " + targetPath);

            child_process.execFile('python',
		   ['screw.py', targetPath, convertedPath],
		   function(err, stdout, stderr) {
		       if (err) {
			   console.log(stderr);
			   console.log(stdout);
			   console.log(err);

			   throw err;
		       }

		       console.log(stdout);

		       fs.unlink(targetPath, function(err) {
			   if (err) {
			       throw err;
			   }
		       });
	    });
        });
    });
});

app.listen(app.get('port'), function() {
    console.log('Node app is running on port', app.get('port'));
});

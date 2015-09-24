var fs = require('fs');
var child_process = require('child_process');

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
        fieldSize: '15MB'
    }
}).single('file');

app.set('port', (process.env.PORT || 5000));
app.use(router);
app.use(express.static(__dirname, '/css'));
app.use(bodyParser.urlencoded({extended: false}));

router.get('/', function(req, res, next) {
    res.sendFile(__dirname + '/upload.html');
});

router.post('/upload', upload, function(req, res, next) {
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

                                       res.download(convertedPath);
                                   });
        });
    });
});

//app.get('/download', function(req, res, next) {
//	  res.download('');
//});

//app.get('/analyze', function(req, res, next) {
//	  res.send('analyzing...');
//});

app.listen(app.get('port'), function() {
    console.log('Node app is running on port', app.get('port'));
});

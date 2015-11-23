var fs = require('fs'),
    spawn = require('child_process').spawn,
    express = require('express'),
    app = express(),
    router = express.Router(),
    multer = require('multer'),
    bodyParser = require('body-parser'),
    mkdirp = require('mkdirp');


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

            var child = spawn('python', ['screw.py', targetPath, convertedPath]);

            child.stdout.on('data', function(data) {
                console.log(data.toString());
            });

            child.on('close', function(code, signal) {
                res.download(convertedPath, function() {
                    fs.unlink(targetPath, function(err) {
                        if (err) {
                            throw err;
                        }
                    });
                });
            });
        });
    });
});

app.listen(app.get('port'), function() {
    console.log('Node app is running on port', app.get('port'));
});

var express = require('express');
var multer = require('multer');
var router = express.Router();

/* GET home page. */
router.get('/report', function(req, res) {
  res.render('report', {title: 'This is Sparta', filename: 'Dummy File', report:'This is an example', original:'There is no such file here'});
});

module.exports = router;

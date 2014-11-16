var express = require('express');
var multer = require('multer');
var router = express.Router();
var fs = require("fs"); 
var inspect = require('eyes').inspector({maxLength:20000});
var pdf_extract = require('pdf-extract');
var shell = require('shelljs')

var abs_path = '/home/sriganesh/Documents/IS/RoughWork/Needed/App/RRAnalyzer/';

router.get('/uploads', function(req, res) { 
	console.log("inside upload get function");
  	res.redirect('/'); 
});

router.post('/uploads', function(req, res) {
	console.log("inside uploads post function");
	if (typeof req.files.myFile === 'undefined') {
		res.render('index', {title: "I love files!"}); 
	}
	if (req.files.myFile.extension === 'pdf') {
		var options = {
			type : 'text'
		}
		var filepath = abs_path+req.files.myFile.path;
		var processor = pdf_extract(filepath, options, function(err) {
			if(err) {
				console.log("Something went wrong");
				return callback(err);
			}
		});
		processor.on('complete', function(data) {
		 	fs.openSync(abs_path+'uploads/message.txt', 'w+');
			console.log("File created");
			for (var i = 0; i < data.text_pages.length; i++) {
				fs.appendFileSync(abs_path+'uploads/message.txt', data.text_pages[i]);
				console.log("Append finished");
			}
			var id = data.text_pages.toString().split('\n');
			var dir_path = abs_path+'uploads/';
			shell.cd(dir_path);
			if (shell.exec('sh normalize.sh').code == 0) {
				shell.cd('../');
				console.log('finished');
				var finalreport = []
				var contents = fs.readFileSync(abs_path+'uploads/result.txt');
				contents =  contents.toString();
				contents = contents.split('\n');
				contents.pop();
				var diagnose = fs.readFileSync(abs_path+'uploads/diagnose.txt');
				diagnose =  diagnose.toString();
				diagnose = diagnose.split('\n');
				diagnose.pop();
				var sectionList = [];
				for(var i = 0; i < contents.length; i++) {
					sectionList.push("section"+(i+1).toString());				
				}
				for(var i = 0; i < contents.length; i++) {
					finalreport.push({content: contents[i], section: sectionList[i], result: diagnose[i]})
				}
				var pdfFile = './../' + req.files.myFile.path.toString();
				res.render('report', {title: 'Radiology Report', filename: req.files.myFile.originalname, report: finalreport, original: pdfFile});
			}
		});	
	}
	else {
		res.render('index', {title: "I love files!"}); 
	}
});

module.exports = router;

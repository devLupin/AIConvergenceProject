// import
const path = require("path");
var express = require('express');
const https = require('https');

var ssl_options = require('./config/ssl_config').options;

// 함수 저장
var app = express();
const port = 16984;

var bodyParser = require('body-parser');
const { query } = require("express");
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

var publicPath = path.join(__dirname, 'public');
app.use(express.static(publicPath));

const server = https.createServer({
    key: ssl_options.key,
    cert: ssl_options.cert,
}, app);

// 서버 오픈
server.listen(port, () => console.log('express server running on port ' + port));

app.get('/', function (req, res) {
    res.sendFile('public/index.html');
})
const fs = require('fs');
var path = require('path');

module.exports.options = {
    key: fs.readFileSync(path.join(__dirname, 'key.pem')),
    cert: fs.readFileSync(path.join(__dirname, 'cert.pem')),
    passphrase:'lht1080',
    agent:false
};
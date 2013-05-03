var connect = require('connect');
var app = connect();
var router = require('flask-router')();

app.use(connect.static(__dirname + '/public'));
app.use(router.route);

router.post('/upload');

app.listen(8080);


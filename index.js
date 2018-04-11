var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use(express.static(__dirname + '/static'));

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
  res.sendFile(__dirname + '/base.css');

});

io.on('connection', function (socket) {
  console.log('a user connected');
  socket.on('disconnect', function () {
    console.log('user disconnected');
  });
});

io.on('connection', function (socket) {
  socket.on('chat message', function (msg,user) {
    console.log(timeNow()+" "+ user + ' sent ' + msg);
    msg = msg.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    io.emit('chat message', msg, user, timeNow());
  });
});

http.listen(3000, function () {
  console.log('listening on *:3000');
});

function timeNow() {
  var d = new Date(),
    h = (d.getHours() < 10 ? '0' : '') + d.getHours(),
    m = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
    return (h + ':' + m);
}
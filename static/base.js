$(document).ready(function () {
    var socket = io();
    var user;
    $('#user_select').modal('show');

    $('#pop').submit(function () {
        $('#user_select').modal('hide');

        user = $('#username').val();
        console.log(user);
        return false;     
    });

    $('#messager').submit(function () {
        var message = $('#message').val()
        console.log(user);
        socket.emit('chat message', message, user );
        $('#message').val('');
        return false;
    });
    socket.on('chat message', function (msg, usr, time) {
        if (user == usr){
            $('#messages').append("<li class='list-group-item'><div class='inlined'>" + time + "</div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"  + usr + ": " + msg + " </li>");
        }
        else{
            $('#messages').append("<li class='list-group-item list-group-item-primary'><div class='inlined'>" + time +"</div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + usr + ": " + msg + " </li>");
               
        }
    });
});
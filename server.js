const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
let net = require('net');

const io = new Server(server, {
    cors: {
      origin: "*",
      credentials: true,
    },
  });

const SOCKET_PORT = 3006;
const TCP_PORT = 12001;
const HOST = "10.128.0.28";

net.createServer(function (socket) {
    console.log('TCP connect');
    socket.on('data', function(data) {
        io.sockets.emit('message', data.toString()); 
    });
    socket.on('end', function() {
        console.log('TCP end');
    });
    socket.on('close', function() {
        console.log('TCP close');
    });
    socket.on('error', function(e) {
        console.log('TCP error ', e);
    });
  }).listen(TCP_PORT, HOST, () => {
        console.log(`TCP Server is listening on port ${TCP_PORT}`);
});

io.on('connection', (socket) => {
    console.log('Socket connect');
})

server.listen(SOCKET_PORT, HOST, () => {
    console.log(`Socket Server is listening on port ${PORT}`)
})

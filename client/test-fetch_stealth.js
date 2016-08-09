// $ nodejs test-fetch_stealth.js
var WebSocket = require('ws')
var ws = new WebSocket("ws://localhost:8888/");
ws.onopen = function() {
  var request = {
    "id": 1,
    "command": "fetch_stealth",
    "params": ["", 419135]
  }
  var message = JSON.stringify(request);
  ws.send(message);
};
ws.onmessage = function (evt) {
  console.log(evt.data);
};


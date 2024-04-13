console.log("WEBPICKER");


// axios.get('127.0.0.1:5000')
//   .then(response => {
//     console.log(response.data);
//   })
//   .catch(error => {
//     console.error(error);
//   });


        
var socket = new WebSocket("ws://127.0.0.1:5000");

socket.onopen = function() {
    console.log("connected.");
};

socket.onmessage("hi")

let data_block = document.querySelector('.data')

let sendDataButton = document.querySelector('.sendData button');
let sendDataTextarea = document.querySelector('.sendData textarea');

let sendData;



var socket = new WebSocket("wss://socketsbay.com/wss/v2/1/demo/");

socket.onopen = function() {
    alert("Соединение установлено.");
};

socket.onmessage = function(event) {
    data_block.innerText = "Получены данные \n" + event.data + "\n \nJSON TYPE: \n" + JSON.stringify(event.data) ;

};

sendDataButton.onclick = function() {
    sendData = sendDataTextarea.value;
    socket.send(sendData);
};


socket.onclose = function(event) {
  if (event.wasClean) {
    alert('Соединение закрыто чисто');
  } else {
    alert('Обрыв соединения'); // например, "убит" процесс сервера
  }
  alert('Код: ' + event.code + ' причина: ' + event.reason);
};



// socket.onerror = function(error) {
//   alert("Ошибка " + error.message);
// };


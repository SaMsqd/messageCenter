console.log("WEBPICKER");

document.addEventListener('DOMContentLoaded', function(){
    let sidebar = document.querySelector('.sidebar');       // поиск левого меню    
    let chatElements = sidebar.querySelectorAll('.chat');   // поиск всех .chat
    let nochat = document.querySelector('.nochat');         // поиск блока ошибки
    let mainChatForm = document.querySelector('.main')      // поиск формы чата
    let lastTappedChat = null;                              // хранит ссылку на последний чат, на который было нажато
    
 
    chatElements.forEach(chat => {

        // Если не найдет .chat, то сообщит об этом
        if(chat === null) {
            nochat.style.display = 'flex'; // если нашел .chat, то ошибка скрыта
        } else {
            nochat.style.display = 'none'; // если не нашел .chat, то покажет ошибку 
        }

        let checkCircle = chat.querySelector('.new-msg');
        chat.onclick = tapFunc;

        function tapFunc() {
            if (lastTappedChat !== null) {              
                lastTappedChat.style.borderColor = '';  // У предыдущего .chat 
                lastTappedChat.style.borderWidth = '';  // пропадает цвет обводки и сама обводка
            }
            console.log("Tap!")
            checkCircle.classList.add("__none");        // пропадет кружок
            chat.style.borderColor = 'greenyellow';     // Обводка станет зеленой у текущего чата
            chat.style.borderWidth = '2px';             // Обводка 2px
            mainChatForm.style.display = 'flex';        // Появляется чат

            
            lastTappedChat = chat;                      // обновляем последний чат
            

        }
    });
});

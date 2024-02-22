console.log("WEBPICKER");

document.addEventListener('DOMContentLoaded', function(){
    let sidebar = document.querySelector('.sidebar');       // поиск левого меню    
    let messanger = document.querySelector('.messanger');   // поиск .messanger
    let chatElements = sidebar.querySelectorAll('.chat');   // поиск всех .chat
    let nochat = document.querySelector('.nochat');         // поиск блока ошибки
    let mainChatForm = document.querySelector('.main')      // поиск формы чата
                            
    
    let main = document.querySelector('.main');
    let arrow = document.querySelector('.arrow');  //  Стрелка     
 
    
    let lastmsg = sidebar.querySelectorAll('.last-msg');
    let name = sidebar.querySelectorAll('.name')
    let lastTappedChat = null;  // хранит ссылку на последний чат, на который было нажато
    arrow.onclick = tapArrow;
    
    let rotation = 0;
    
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
            checkCircle.classList.add("__none");        // пропадет кружок
            
            chat.style.borderColor = 'greenyellow';     // Обводка станет зеленой у текущего чата
            chat.style.borderWidth = '2px';             // Обводка 2px
            mainChatForm.style.display = 'flex';        // Появляется чат

            lastTappedChat = chat;                      // обновляем последний чат
        }
   
    });


    function tapArrow() {
        rotation += 180; // Add 180 degrees for the opposite rotation
        arrow.style.transform = `rotate(${rotation}deg)`;

        if (rotation % 360 === 0) {
            console.log("Side open")
            sidebar.classList.add("__open");
            sidebar.classList.remove("__close")
            messanger.classList.remove("__open");
            messanger.classList.add("__close");


            lastmsg.forEach(lastmsg => { 
                lastmsg.style.display = 'flex';
            });
            name.forEach(name => {
                name.classList.remove("__smallname")
            });

          } else {
            console.log("Side close")

            sidebar.classList.add("__close");
            sidebar.classList.remove("__open");
            messanger.classList.remove("__close");
            messanger.classList.add("__open");
            
            lastmsg.forEach(lastmsg => { 
                lastmsg.style.display = 'none';
            });

            name.forEach(name => {
                name.classList.add("__smallname")
            });

            chatElements.forEach(chat => {
                console.log(chat.style.borderColor == 'greenyellow')
                if (chat.style.borderColor === 'greenyellow') {
                    main.style.display = 'flex';
                    console.log("ПОКАЗАТЬ")
                } else {
                    // main.style.display = 'none';
                }
            });
            

        }
        
    }

});

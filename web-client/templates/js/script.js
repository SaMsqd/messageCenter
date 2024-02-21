console.log("WEBPICKER")

document.addEventListener('DOMContentLoaded', function(){
    let sidebar = document.querySelector('.sidebar');
    let chat = sidebar.querySelector('.chat');
    let nochat = document.querySelector('.nochat');

    if(chat === null) {
        nochat.style.display = 'flex';
    } else {
        nochat.style.display = 'none';
    }

});
function processMessage() {

    const roomName = JSON.parse(document.getElementById('room-name').textContent);
    const trivia_user = sessionStorage.trivia_user;
    document.querySelector('#user-txt').innerHTML = trivia_user

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);
        // modal-log, game-modal

        document.querySelector('#modal-log').innerHTML = data.log;
        logHtml = document.querySelector('.game-modal').innerHTML;
        document.querySelector('#game-container').innerHTML = logHtml;
    };

    chatSocket.onclose = function (e) {
        console.error('Game socket closed unexpectedly');
    };

    let buttonAnswer = document.querySelectorAll('.questionBtn')
    for (let i = 0; i < buttonAnswer.length; i++) {
        buttonAnswer[i].addEventListener('click', function () {
            let option = buttonAnswer[i].querySelector('input[name="option-input"]');
            chatSocket.send(JSON.stringify({
                'user': trivia_user,
                'option': option.value
            }));
        })
    }

}
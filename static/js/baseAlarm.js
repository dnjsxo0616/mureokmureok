

const roomName = JSON.parse(document.getElementById('room-name').textContent);

const alarmSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/alarm/'
    + roomName
    + '/'
);

alarmSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    //document.querySelector('#chat-log').value += (data.message + '\n');
    console.log(data);
    document.getElementById("alarm-dropdown").innerHTML = "<li class='alarm-dropdown-item'>" + data + "</li><hr class='alarm-dropdown-divider'>" + document.getElementById("alarm-dropdown").innerHTML;
    document.getElementById("alarm-badge").innerHTML = parseInt(document.getElementById("alarm-badge").innerHTML) + 1;
};

alarmSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


const alarm_button = document.getElementById("alarm-button");

alarm_button.addEventListener('click', () => {
const alarm_dropdown = document.getElementById("alarm-dropdown");
alarm_dropdown.style.display = 'block';
});


alarm_button.addEventListener('blur', () => {
    const alarm_dropdown = document.getElementById("alarm-dropdown");
    
    // 0.2초 뒤에 실행
    setTimeout(() => {
        alarm_dropdown.style.display = 'none';
    }, 5);

});

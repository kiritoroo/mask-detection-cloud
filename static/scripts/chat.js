function formatTime(date){
    d = new Date(date);
    var h=d.getHours(),m=d.getMinutes(),l="AM";
    if(h > 12){ h = h - 12; }
    if(h < 10){ h = '0'+h; }
    if(m < 10){ m = '0'+m; }
    if(d.getHours() >= 12){ l="PM"
    } else{ l="AM" }
    return h+':'+m+' '+l;
}

if (token["jwt"] === undefined) {
    window.location.replace("/login");
}

const token_decode = parseJwt(token['jwt'])

const url = "ws://" + location.hostname + ':' + location.port + "/ws/" + token_decode['sub']
const ws = new WebSocket(url);

ws.onopen = (event) => {
    ws.send(token_decode['sub'] + " connect");
};

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    const panel = document.getElementById('chat-panel')

    if(message.clientId != token_decode['sub']) {
        panel.innerHTML +=
        `<div class="col-start-1 col-end-8 p-3 rounded-lg">
            <div class="flex flex-row items-center">
                <div class="flex items-center justify-center mt-4 h-10 w-10 rounded-full bg-gradient-to-br from-blue-200 to-red-100 flex-shrink-0">
                    ${message.clientId.charAt(0).toUpperCase()}
                </div>
                <div class="flex flex-col">
                        <p class="relative text-xs py-1 px-4 ">${JSON.parse(event.data).time} Today</p>
                    <div class="inner-flex flex-col justify-start">
                        <div class="relative ml-3 text-sm bg-white py-2 px-4 shadow rounded-xl">
                            <div>${message.message}</div>
                        </div>
                        <span class="bg-blue-100 text-blue-600 text-xs font-semibold ml-4 my-2 px-2.5 py-0.5 rounded ">${message.clientId}</span>
                    </div>
                </div>

            </div>
        </div>`

        const scroll = document.getElementById('chat-scroll');
        scroll.scrollTo(0, panel.scrollHeight);
    }
};

function sendt(){
    const panel = document.getElementById('chat-panel')
    const msg = document.getElementById("msg-send").value;

    ws.send(msg);

    panel.innerHTML +=
    `<div class="col-start-6 col-end-13 p-3 rounded-lg">
        <div class="flex items-center justify-start flex-row-reverse">
            <div class="flex items-center justify-center mt-4 h-10 w-10 rounded-full bg-gradient-to-br from-blue-200 to-red-100 flex-shrink-0">
                ${token_decode['sub'].charAt(0).toUpperCase()}
            </div>
            <div class="flex flex-col">
                <p class="text-xs py-1 px-4 justify-self-end text-end">${formatTime(new Date())} .Today</p>
                <div class="relative mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl">
                    <div>${msg}</div>
                </div>
            </div>
        </div>
    </div>`

    const scroll = document.getElementById('chat-scroll');
    scroll.scrollTo(0, panel.scrollHeight);
}

const msgInput = document.getElementById("msg-send")
msgInput.addEventListener("keypress", () => {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("msg-button").click();
        msgInput.value = "";
    }
});

const sendButton = document.getElementById("msg-button");

sendButton.addEventListener('click', () => {
    sendt();
    msgInput.value = "";
});
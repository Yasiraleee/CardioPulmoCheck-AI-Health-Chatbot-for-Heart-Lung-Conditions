function voice(){
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "en-GB";
    recognition.onresult = function(event){
        console.log(event);
        document.getElementById("textarea").value = document.getElementById("textarea").value + " " +
            event.results[0][0].transcript;
    }
    recognition.start();
    }


const chatInput = document.querySelector(".Message input");
const sendChatBtn = document.getElementById("sendMessage");
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);

    if (className === "outgoing") {
        chatLi.id = "outgoingmsg";
        chatLi.innerHTML = `<p>${message}</p>`;
    } else {
        chatLi.innerHTML = `<span class="material-symbols-outlined"><img src="/static/chatboi.png" width="60"></img></span><p>${message}</p>`;
    }
    scrollChatToBottom();
    return chatLi;
}



const handleChat = () => {
    const userMessage = chatInput.value.trim();
    console.log(userMessage);
    if (!userMessage) return;

    chatbox.appendChild(createChatLi(userMessage, "outgoing"));

    setTimeout(() => {
        ChatFunc(userMessage);
    }, 900);
};

sendChatBtn.addEventListener("click", handleChat);

function ChatFunc(O_Msg) {
    fetch('/api/DataInput', {
            method: 'POST',
            body: JSON.stringify({
                sentence: O_Msg
            }),
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
            }
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            console.log(data,"yes");
            displayAnswer(data.ans);
        })
        .catch(error => console.error('Error:', error));
};
function displayAnswer(answer) {
    const incomingMessageElement = document.getElementById("incomingid");
    const chat= document.querySelector('.chatbox');
    if (chat) {
        chat.innerHTML += `<li id="incomingmsg" class="chat incoming" style="height: 46px;">
                    <span class="material-symbols-outlined"><img src="/static/chatboi.png"
                                                                 width="60"></img></span>
                    <p>${answer}</br></p>
                </li>`;
    }
}




function scrollChatToBottom() {
        var chatContainer = document.querySelector(".chatbox");
        chatContainer.scrollTop = chatContainer.scrollHeight;
        console.log(chatContainer.scrollHeight);
    }
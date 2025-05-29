// === Text-to-Speech Function ===
function speakText(text) {
    const synth = window.speechSynthesis;
    const utter = new SpeechSynthesisUtterance(text);
    utter.pitch = 1;
    utter.rate = 1;
    utter.voice = synth.getVoices().find(voice => voice.lang === 'en-US') || synth.getVoices()[0];
    synth.speak(utter);
}

// === Add glowing animation on mic button during recording ===
const micBtn = document.getElementById("MicBtn");

micBtn.addEventListener("mousedown", () => {
    micBtn.classList.add("glowing-mic");
});
micBtn.addEventListener("mouseup", () => {
    micBtn.classList.remove("glowing-mic");
});

// === Handle Enter Key in Input Field ===
document.getElementById("chatbox").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        e.preventDefault();
        document.getElementById("SendBtn").click();
    }
});

// === Eel fallback (simulate Python response) ===
if (typeof eel === 'undefined') {
    window.eel = {
        process_command: (text) => {
            return (callback) => {
                const mockResponse = `You said: "${text}" (Python not connected)`;
                callback(mockResponse);
            };
        }
    };
}

// === Voice output for J.A.R.V.I.S. replies (modify eel callback) ===
eel.expose(display_response);
function display_response(response) {
    $('#chat-canvas-body').append(`<div class="bot-msg mb-3"><strong>J.A.R.V.I.S:</strong> ${response}</div>`);
    speakText(response);
    const chatBody = document.getElementById("chat-canvas-body");
    chatBody.scrollTop = chatBody.scrollHeight;
}

// === Optional: Clear input on focus ===
document.getElementById("chatbox").addEventListener("focus", () => {
    document.getElementById("chatbox").value = "";
});
function closeWindow() {
    window.open('', '_self', '');
    window.close();
}
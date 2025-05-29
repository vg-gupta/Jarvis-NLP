const siriWave = new SiriWave({
    container: document.getElementById('siri-container'),
    width: 800,
    height: 200,
    style: 'ios9',
    speed: 0.10,
    amplitude: 1.5,
    frequency: 4,
    autostart: true
});
// === Initialize SiriWave ===

// === Initialize Speech Recognition ===
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US';

// === Mic Button Click Event ===
document.getElementById("MicBtn").addEventListener("click", () => {
    
    siriWave.start();
    recognition.start();
});
window.onload = () => {
    eel.wishMe();  // This will run only once when the app loads
};

document.getElementById("SettingsBtn").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
  
    // Optional: Change icon or show a tooltip/message
    const gearIcon = this.querySelector("i");
    if (document.body.classList.contains("dark-mode")) {
      gearIcon.classList.remove("bi-gear");
      gearIcon.classList.add("bi-moon-stars-fill");
    } else {
      gearIcon.classList.remove("bi-moon-stars-fill");
      gearIcon.classList.add("bi-gear");
    }
  });
  
// === Handle Recognition Result ===
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById("chatbox").value = transcript;
    siriWave.stop();

    // Auto-send message
    document.getElementById("SendBtn").click();
};

recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    siriWave.stop();
};

// === Send Button Click Event ===
document.getElementById("SendBtn").addEventListener("click", () => {
    const input = document.getElementById("chatbox").value.trim();
    if (!input) return;

    // Append user message to chat canvas
    $('#chat-canvas-body').append(`<div class="user-msg mb-2" style="color:rgb(255, 255, 255);"><strong>You:</strong> ${input}</div>`);

    // Call Python backend via eel
    eel.process_command(input)(function (response) {
        // Append bot response
        $('#chat-canvas-body').append(`<div class="bot-msg mb-3" style="color:rgb(255, 255, 255);"><strong>J.A.R.V.I.S:</strong> ${response}</div>`);
        $('#chatbox').val('');
        

        // Scroll chat to bottom
        const chatBody = document.getElementById("chat-canvas-body");
        chatBody.scrollTop = chatBody.scrollHeight;

        // Open chat canvas if hidden
        
    });
    eel.process_command(text)(function(response) {
        addBotMessage(response); // Don't worry if function is named differently
    });
    
});

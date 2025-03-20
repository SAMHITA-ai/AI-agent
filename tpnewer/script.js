let followUpIntent = null;

function addMessageToChat(message) {
    const chatbox = document.getElementById("chat-box");
    const messageElem = document.createElement("p");
    messageElem.textContent = message;
    chatbox.appendChild(messageElem);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    

    addMessageToChat("You: " + userInput);
    document.getElementById("user-input").value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botResponse = data.response || "❌ No response received.";
        addMessageToChat("Chatbot: " + botResponse);
    })
    .catch(error => {
        console.error("Fetch error:", error);
        addMessageToChat("Chatbot: ❌ Error connecting to server.");
    });
}

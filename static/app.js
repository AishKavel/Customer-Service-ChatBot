class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let userMessage = textField.value.trim();

        if (userMessage === "") {
            return;
        }

        // Add user message to messages array
        this.messages.push({ name: "User", message: userMessage });

        // Fetch response from Flask server
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: userMessage }),
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(data => data.json())
        .then(data => {
            // Extract 'output' from the JSON response
            if (data.output) {
                let botMessage = data.output;
                this.messages.push({ name: "Jimmy", message: botMessage });
            } else {
                this.messages.push({ name: "Jimmy", message: "Sorry, I couldn't understand that." });
            }
            this.updateChatText(chatbox);
            textField.value = ""; // Clear input field
        })
        .catch(error => {
            console.error('Error:', error);
            this.messages.push({ name: "Jimmy", message: "Error: Unable to process the request." });
            this.updateChatText(chatbox);
            textField.value = "";
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function (item) {
            if (item.name === "Jimmy") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatMessages = chatbox.querySelector('.chatbox__messages');
        chatMessages.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();

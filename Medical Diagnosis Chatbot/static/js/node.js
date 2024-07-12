document.addEventListener('DOMContentLoaded', (event) => {
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    const chat = document.getElementById('chat');

    // Function to append messages to the chat
    const appendMessage = (text, className) => {
        const message = document.createElement('div');
        message.textContent = text;
        message.className = className;
        chat.appendChild(message);
        chat.scrollTop = chat.scrollHeight; // Scroll to the bottom of the chat
    };

    // Function to send user message and process bot response
    const sendMessage = () => {
        const userText = userInput.value;
        if (userText.trim() !== '') {
            appendMessage(userText, 'p-2 my-2 text-right bg-blue-100 rounded'); // User message
            userInput.value = ''; // Clear input after sending
            
            const typingIndicator = document.createElement('div');
            typingIndicator.textContent = 'Typing...';
            typingIndicator.className = 'p-2 my-2 text-left bg-gray-100 rounded';
            chat.appendChild(typingIndicator);

            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userText }),
            })
            .then(response => response.json())
            .then(data => {
                chat.removeChild(typingIndicator);
                appendMessage(data.message, 'p-2 my-2 text-left bg-green-100 rounded'); // Bot message
                
                // Focus the input if the bot asks for more symptoms or another input
                if (data.message.includes('Please provide more symptoms') || data.message.includes('Any other symptoms') || data.message.includes('enter your age') || data.message.includes('enter your gender') || data.message.includes('describe your symptoms')) {
                    userInput.focus();
                }
            })
            .catch((error) => {
                chat.removeChild(typingIndicator);
                appendMessage('An error occurred. Please try again.', 'p-2 my-2 text-left bg-red-100 rounded');
                console.error('Error:', error);
            });
        }
    };

    // Event listeners for sending messages
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
            e.preventDefault(); // Prevent the default action to stop form submission
        }
    });
});

// Simple AI Assistant Test
console.log('🚀 Simple AI Assistant JS loaded');

// Simple config
const AI_ASSISTANT_CONFIG = {
    getApiUrl: function () {
        return 'https://aa8c9e5294ad.ngrok-free.app';
    }
};

// Simple test
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Simple AI Assistant: DOM loaded');
    console.log('📋 Config:', AI_ASSISTANT_CONFIG);

    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    console.log('📱 DOM elements found:', {
        chatInput: !!chatInput,
        sendButton: !!sendButton,
        chatMessages: !!chatMessages
    });

    if (!chatInput || !sendButton || !chatMessages) {
        console.error('❌ Missing DOM elements!');
        return;
    }

    sendButton.addEventListener('click', function () {
        console.log('🔘 Send button clicked');
        const message = chatInput.value.trim();
        if (message) {
            console.log('📤 Sending message:', message);
            chatMessages.innerHTML += '<p>You: ' + message + '</p>';
            chatInput.value = '';

            // Show loading
            chatMessages.innerHTML += '<p>Loading...</p>';

            // Test API call with better error handling
            const apiUrl = AI_ASSISTANT_CONFIG.getApiUrl();
            console.log('🌐 Making request to:', apiUrl + '/health');

            fetch(apiUrl + '/health', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true'
                },
                mode: 'cors'
            })
                .then(response => {
                    console.log('📡 Response status:', response.status);
                    if (!response.ok) {
                        throw new Error('HTTP ' + response.status + ': ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('📊 API Response:', data);
                    chatMessages.innerHTML += '<p>✅ API Response: ' + JSON.stringify(data) + '</p>';
                })
                .catch(error => {
                    console.error('❌ Fetch error:', error);
                    chatMessages.innerHTML += '<p>❌ Error: ' + error.message + '</p>';
                });
        } else {
            console.log('⚠️ No message to send');
        }
    });

    console.log('✅ Simple AI Assistant initialized');
});

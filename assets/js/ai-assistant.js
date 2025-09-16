// AI Assistant Configuration
const AI_ASSISTANT_CONFIG = {
    // API URL - For local development
    API_URL: 'http://localhost:5001',

    // Environment detection
    isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',

    // Auto-detect production URL if on GitHub Pages
    getApiUrl: function () {
        if (this.isProduction) {
            // Replace with your ngrok URL
            return 'https://ffe765f92326.ngrok-free.app';
        }
        return this.API_URL;
    }
};

class Assistant {
    constructor() {
        this.apiUrl = AI_ASSISTANT_CONFIG.getApiUrl();

        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        this.assistantContainer = document.getElementById('assistant-container');

        this.conversationHistory = [];
        this.isInitialState = true;

        this.initializeEventListeners();
        this.checkServerStatus();
        this.setInitialState();
        this.focusInput();
    }

    initializeEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.chatInput.addEventListener('input', () => {
            this.autoResizeTextarea();
            this.updateSendButton();
        });
    }

    autoResizeTextarea() {
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 120) + 'px';
    }

    updateSendButton() {
        const hasText = this.chatInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }

    async checkServerStatus() {
        try {
            const response = await fetch(`${this.apiUrl}/health`, {
                headers: {
                    'ngrok-skip-browser-warning': 'true'
                }
            });

            const data = await response.json();

            if (data.status !== 'healthy') {
                this.addSystemMessage('AI server is not responding properly.');
            }
        } catch (error) {
            this.addSystemMessage('⚠️ Cannot connect to the AI server. Please make sure the backend server is running.');
        }
    }

    addMessage(content, type = 'assistant', isStreaming = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        // Render markdown for assistant messages, plain text for user/system
        const processedContent = (type === 'assistant' && typeof marked !== 'undefined')
            ? marked.parse(content)
            : content;

        messageDiv.innerHTML = `
      <div class="message-content">${processedContent}</div>
    `;

        this.chatMessages.appendChild(messageDiv);
        this.updateChatLayout();

        if (isStreaming) {
            return messageDiv.querySelector('.message-content');
        }
    }

    addSystemMessage(content) {
        this.addMessage(content, 'system');
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
      <div class="typing-dots">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    `;
        this.chatMessages.appendChild(typingDiv);
        this.updateChatLayout();
    }

    hideTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    setInitialState() {
        this.assistantContainer.className = 'initial-state';
        this.chatMessages.style.justifyContent = 'center';
    }

    focusInput() {
        // Focus the input field after a short delay to ensure the page is fully loaded
        setTimeout(() => {
            this.chatInput.focus();
        }, 100);
    }

    setConversationState() {
        this.assistantContainer.className = 'conversation-state';
        this.chatMessages.style.justifyContent = 'flex-start';
        this.isInitialState = false;
    }

    updateChatLayout() {
        const messages = this.chatMessages.children;
        const hasMessages = messages.length > 0;

        if (hasMessages && this.isInitialState) {
            this.setConversationState();
        }

        if (hasMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');

        // Add to conversation history
        this.conversationHistory.push({ role: 'user', content: message });

        // Clear input and disable send button
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        this.sendButton.disabled = true;

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true'
                },
                body: JSON.stringify({
                    message: message,
                    history: this.conversationHistory.slice(-10) // Send last 10 messages for context
                })
            });

            if (response.ok) {
                // Hide typing indicator
                this.hideTypingIndicator();

                const data = await response.json();
                const aiResponse = data.response;

                // Simulate streaming by typing out the response
                await this.typeResponse(aiResponse);

                // Add to conversation history
                this.conversationHistory.push({ role: 'assistant', content: aiResponse });
            } else {
                const data = await response.json();
                this.hideTypingIndicator();
                this.addSystemMessage(`Error: ${data.error || 'Unknown error occurred'}`);
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addSystemMessage(`Connection error: ${error.message}`);
        } finally {
            this.chatInput.focus();
        }
    }

    async typeResponse(text) {
        // Remove the typing indicator
        this.hideTypingIndicator();

        // Create a new message for the response
        const messageContent = this.addMessage('', 'assistant', true);

        // Type out the response character by character with increasing speed
        let currentText = '';
        for (let i = 0; i < text.length; i++) {
            currentText += text[i];

            // Render markdown for the current text
            if (typeof marked !== 'undefined') {
                messageContent.innerHTML = marked.parse(currentText);
            } else {
                messageContent.textContent = currentText;
            }

            this.updateChatLayout();

            // Calculate dynamic delay - starts slow, gets faster
            const progress = i / text.length;
            const baseDelay = 30; // Starting delay
            const minDelay = 5;   // Minimum delay
            const delay = Math.max(minDelay, baseDelay * (1 - progress * 0.8));

            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }
}

// Initialize assistant when page loads
document.addEventListener('DOMContentLoaded', () => {
    try {
        // Configure marked.js options
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,        // Convert \n to <br>
                gfm: true,          // GitHub Flavored Markdown
                sanitize: false,    // Allow HTML (be careful with this in production)
                smartLists: true,   // Better list handling
                smartypants: true   // Smart quotes and dashes
            });
        }

        new Assistant();

    } catch (error) {
        console.error('Error initializing assistant:', error);
    }
});

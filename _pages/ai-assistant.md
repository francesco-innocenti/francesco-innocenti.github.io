---
permalink: /ai-assistant/
layout: single
author_profile: true
---

The following simple AI assistant should be able to answer any questions about 
my professional experience. Note that it can make mistakes and hallucinate facts, 
so please refer to my CV for fact-checking.

<!-- Include marked.js for markdown rendering -->
<script src="https://cdn.jsdelivr.net/npm/marked@9.1.6/marked.min.js"></script>

<div id="assistant-container">
  <div id="chat-messages"></div>
  <div id="chat-input-container">
    <div id="input-wrapper">
      <textarea id="chat-input" placeholder="Ask anything about Francesco's professional background..." rows="1"></textarea>
      <button id="send-button" disabled>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M7 11L12 6L17 11M12 18V7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</div>

<style>
#assistant-container {
  width: 100%;
  height: calc(100vh - 200px);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
}

#assistant-container.initial-state {
  flex-direction: column;
}

#assistant-container.conversation-state {
  flex-direction: column;
}

#chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background: #ffffff;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 0;
}

#chat-messages::-webkit-scrollbar {
  width: 6px;
}

#chat-messages::-webkit-scrollbar-track {
  background: transparent;
}

#chat-messages::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

.message {
  margin-bottom: 24px;
  display: block;
  width: 100%;
  max-width: 768px;
  padding: 0 20px;
}

.message.user {
  text-align: right;
}

.message.assistant {
  text-align: left;
}

.message-content {
  display: inline-block;
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  line-height: 1.5;
  word-wrap: break-word;
  white-space: pre-wrap;
}

/* Markdown styling */
.message-content h1,
.message-content h2,
.message-content h3,
.message-content h4,
.message-content h5,
.message-content h6 {
  margin: 16px 0 8px 0;
  font-weight: 600;
  line-height: 1.3;
}

.message-content h1 { font-size: 1.5em; }
.message-content h2 { font-size: 1.3em; }
.message-content h3 { font-size: 1.2em; }
.message-content h4 { font-size: 1.1em; }
.message-content h5 { font-size: 1.05em; }
.message-content h6 { font-size: 1em; }

.message-content p {
  margin: 8px 0;
}

.message-content ul,
.message-content ol {
  margin: 8px 0;
  padding-left: 20px;
}

.message-content li {
  margin: 4px 0;
}

.message-content code {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
}

.message-content pre {
  background: rgba(0, 0, 0, 0.1);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
  line-height: 1.4;
}

.message-content pre code {
  background: none;
  padding: 0;
  border-radius: 0;
}

.message-content blockquote {
  border-left: 4px solid rgba(0, 0, 0, 0.2);
  margin: 12px 0;
  padding-left: 16px;
  font-style: italic;
}

.message-content table {
  border-collapse: collapse;
  margin: 12px 0;
  width: 100%;
}

.message-content th,
.message-content td {
  border: 1px solid rgba(0, 0, 0, 0.2);
  padding: 8px 12px;
  text-align: left;
}

.message-content th {
  background: rgba(0, 0, 0, 0.1);
  font-weight: 600;
}

.message-content a {
  color: #10a37f;
  text-decoration: underline;
}

.message-content a:hover {
  color: #0d8a6b;
}

.message-content strong {
  font-weight: 600;
}

.message-content em {
  font-style: italic;
}

.message-content hr {
  border: none;
  border-top: 1px solid rgba(0, 0, 0, 0.2);
  margin: 16px 0;
}

.message.user .message-content {
  background: #2d3748;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: #f3f4f6;
  color: #374151;
  border-bottom-left-radius: 4px;
}

.message.system .message-content {
  background: #fef3c7;
  color: #92400e;
  border-radius: 8px;
  text-align: center;
  font-style: italic;
  margin: 0 auto;
  max-width: 90%;
}

.typing-indicator {
  display: block;
  margin-bottom: 24px;
  width: 100%;
  max-width: 768px;
  padding: 0 20px;
  text-align: left;
}

.typing-dots {
  display: inline-flex;
  gap: 4px;
  padding: 12px 16px;
  background: #f3f4f6;
  border-radius: 18px;
  border-bottom-left-radius: 4px;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

#chat-input-container {
  padding: 20px;
  background: #ffffff;
  width: 100%;
  max-width: 768px;
  margin: 0 auto;
  order: -1;
}

#assistant-container.conversation-state #chat-input-container {
  order: 1;
}

#input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  background: transparent;
  border: none;
  border-radius: 0;
  transition: none;
}

#input-wrapper:focus-within {
  border-color: transparent;
  box-shadow: none;
}

#chat-input {
  flex: 1;
  border: 2px solid #d1d5db;
  background: #f9fafb;
  outline: none;
  resize: none;
  font-size: 18px;
  line-height: 1.6;
  max-height: 120px;
  min-height: 32px;
  font-family: inherit;
  padding: 8px 12px;
  border-radius: 8px;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

#chat-input:focus {
  border-color: #3b82f6;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

#chat-input::placeholder {
  color: #9ca3af;
}

#send-button {
  width: 36px;
  height: 36px;
  border: none;
  background: #2d3748;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
  margin-top: -2px;
}

#send-button:hover:not(:disabled) {
  background: #1a202c;
  transform: scale(1.05);
}

#send-button:disabled {
  background: #d1d5db;
  cursor: not-allowed;
  transform: none;
}

#send-button svg {
  transform: rotate(90deg);
}

.error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 16px 0;
  font-size: 14px;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .message {
    padding: 0 16px;
  }
  
  .message-content {
    max-width: 90%;
  }
  
  .typing-indicator {
    padding: 0 16px;
  }
  
  #chat-input-container {
    padding: 16px;
  }
}
</style>

<script>
// AI Assistant Configuration - Embedded to avoid loading issues
const AI_ASSISTANT_CONFIG = {
    // API URL - For local development
    API_URL: 'http://localhost:5001',

    // Environment detection
    isProduction: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',

    // Auto-detect production URL if on GitHub Pages
    getApiUrl: function () {
        if (this.isProduction) {
            // Replace with your ngrok URL
            return 'https://aa8c9e5294ad.ngrok-free.app';
        }
        return this.API_URL;
    }
};
</script>
<script>
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
      const response = await fetch(`${this.apiUrl}/health`);
      const data = await response.json();
      
      if (data.status === 'healthy') {
        // No welcome message
      } else {
        this.addSystemMessage('AI server is not responding properly.');
      }
    } catch (error) {
      this.addSystemMessage('⚠️ Cannot connect to the AI server. Please make sure the backend server is running on localhost:5001');
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
  
  async streamResponse(response) {
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    
    // Create a message container for streaming
    const messageContent = this.addMessage('', 'assistant', true);
    
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line in buffer
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              return messageContent.textContent;
            }
            
            try {
              const parsed = JSON.parse(data);
              const content = parsed.choices?.[0]?.delta?.content || '';
              if (content) {
                messageContent.textContent += content;
                this.scrollToBottom();
              }
            } catch (e) {
              // Ignore parsing errors for incomplete chunks
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
    
    return messageContent.textContent;
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
});
</script>

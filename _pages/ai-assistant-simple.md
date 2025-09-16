---
title: "AI Assistant - Simple Test"
permalink: /ai-assistant-simple/
---

# AI Assistant - Simple Test

This is a simplified version to test the JavaScript.

<div id="assistant-container">
  <div id="chat-messages"></div>
  <div id="chat-input-container">
    <div id="input-wrapper">
      <textarea id="chat-input" placeholder="Ask anything..." rows="1"></textarea>
      <button id="send-button">Send</button>
    </div>
  </div>
</div>

<script>
// Simple config
const AI_ASSISTANT_CONFIG = {
  getApiUrl: function() {
    return 'https://b94872810836.ngrok-free.app';
  }
};

// Simple test
document.addEventListener('DOMContentLoaded', function() {
  console.log('Page loaded, config:', AI_ASSISTANT_CONFIG);
  
  const chatInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatMessages = document.getElementById('chat-messages');
  
  sendButton.addEventListener('click', function() {
    const message = chatInput.value.trim();
    if (message) {
      chatMessages.innerHTML += '<p>You: ' + message + '</p>';
      chatInput.value = '';
      
      // Test API call
      fetch(AI_ASSISTANT_CONFIG.getApiUrl() + '/health')
        .then(response => response.json())
        .then(data => {
          chatMessages.innerHTML += '<p>API Response: ' + JSON.stringify(data) + '</p>';
        })
        .catch(error => {
          chatMessages.innerHTML += '<p>Error: ' + error.message + '</p>';
        });
    }
  });
});
</script>

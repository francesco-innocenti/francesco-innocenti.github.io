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
      
      // Show loading
      chatMessages.innerHTML += '<p>Loading...</p>';
      
      // Test API call with better error handling
      const apiUrl = AI_ASSISTANT_CONFIG.getApiUrl();
      console.log('Making request to:', apiUrl + '/health');
      
      fetch(apiUrl + '/health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors'
      })
        .then(response => {
          console.log('Response status:', response.status);
          if (!response.ok) {
            throw new Error('HTTP ' + response.status + ': ' + response.statusText);
          }
          return response.json();
        })
        .then(data => {
          console.log('API Response:', data);
          chatMessages.innerHTML += '<p>✅ API Response: ' + JSON.stringify(data) + '</p>';
        })
        .catch(error => {
          console.error('Fetch error:', error);
          chatMessages.innerHTML += '<p>❌ Error: ' + error.message + '</p>';
        });
    }
  });
});
</script>

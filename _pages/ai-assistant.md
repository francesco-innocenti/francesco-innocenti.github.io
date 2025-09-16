---
permalink: /ai-assistant/
layout: single
author_profile: true
---

The following is a prototype Gemma-based AI assistant that should be able to 
answer questions about my professional experience. Note that it can make 
mistakes and hallucinate facts, so please refer to my CV for fact-checking.

<!-- Include marked.js for markdown rendering -->
<script src="https://cdn.jsdelivr.net/npm/marked@9.1.6/marked.min.js"></script>

<!-- Include AI Assistant JavaScript -->
<script src="{{ '/assets/js/ai-assistant.js' | relative_url }}"></script>

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


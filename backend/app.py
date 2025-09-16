#!/usr/bin/env python3
"""
AI Assistant Backend Server - Ollama Version
Uses Ollama for local AI model inference
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama-service:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "phi3:mini")
PORT = int(os.getenv("PORT", 5001))

# Load system prompt from file
def load_system_prompt():
    """Load system prompt from file"""
    try:
        with open('system_prompt.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Warning: system_prompt.txt not found, using default prompt")
        return "You are a helpful AI assistant."
    except Exception as e:
        print(f"Error loading system prompt: {e}")
        return "You are a helpful AI assistant."

SYSTEM_PROMPT = load_system_prompt()

def reload_system_prompt():
    """Reload system prompt from file"""
    global SYSTEM_PROMPT
    SYSTEM_PROMPT = load_system_prompt()
    return SYSTEM_PROMPT 

class OllamaClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = MODEL_NAME
    
    def check_model_availability(self):
        """Check if the model is available in Ollama"""
        try:
            # First check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json()
                available_models = [model['name'] for model in models.get('models', [])]
                if self.model in available_models:
                    return True
                else:
                    print(f"Model {self.model} not found. Available models: {available_models[:5]}...")
                    return False
            else:
                print(f"Ollama check failed: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ollama check error: {e}")
            return False
    
    def generate_response(self, message, conversation_history=None):
        """Generate a response using Ollama API"""
        try:
            # Prepare messages for Ollama API
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-5:]:  # Keep last 5 messages
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Prepare payload for Ollama API
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "num_predict": 300
                }
            }
            
            # Make request to Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60  # Ollama can take longer than external APIs
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'message' in result and 'content' in result['message']:
                    return result['message']['content']
                else:
                    return "Sorry, I could not generate a response."
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                if response.status_code == 404:
                    return "Sorry, the AI model is not available. Please try again later or contact support."
                else:
                    return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Sorry, an unexpected error occurred. Please try again."

# Initialize Ollama client
ollama_client = OllamaClient()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "ollama_available": ollama_client.check_model_availability()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get conversation history if provided
        conversation_history = data.get('history', [])
        
        # Generate response
        response = ollama_client.generate_response(message, conversation_history)
        
        return jsonify({
            "response": response,
            "model": MODEL_NAME
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """List available models in Ollama"""
    try:
        response = requests.get(f"{ollama_client.base_url}/api/tags")
        if response.status_code == 200:
            models = response.json()
            available_models = [model['name'] for model in models.get('models', [])]
            return jsonify({
                "current_model": MODEL_NAME,
                "available_models": available_models,
                "total_models": len(available_models)
            })
        else:
            return jsonify({"error": f"Failed to fetch models: {response.text}"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to Ollama: {e}"}), 500

@app.route('/system-prompt', methods=['GET', 'POST'])
def system_prompt():
    """Get or update the system prompt"""
    global SYSTEM_PROMPT
    
    if request.method == 'GET':
        return jsonify({"system_prompt": SYSTEM_PROMPT})
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data or 'system_prompt' not in data:
                return jsonify({"error": "system_prompt is required"}), 400
            
            new_prompt = data['system_prompt'].strip()
            if not new_prompt:
                return jsonify({"error": "system_prompt cannot be empty"}), 400
            
            # Save to file
            try:
                with open('system_prompt.txt', 'w', encoding='utf-8') as f:
                    f.write(new_prompt)
            except Exception as e:
                return jsonify({"error": f"Error saving system prompt to file: {e}"}), 500
            
            # Update global variable
            SYSTEM_PROMPT = new_prompt
            return jsonify({"message": "System prompt updated successfully", "system_prompt": SYSTEM_PROMPT})
            
        except Exception as e:
            return jsonify({"error": f"Error updating system prompt: {e}"}), 500

@app.route('/system-prompt/reload', methods=['POST'])
def reload_system_prompt_endpoint():
    """Reload system prompt from file"""
    try:
        reloaded_prompt = reload_system_prompt()
        return jsonify({"message": "System prompt reloaded from file", "system_prompt": reloaded_prompt})
    except Exception as e:
        return jsonify({"error": f"Error reloading system prompt: {e}"}), 500

if __name__ == '__main__':
    print("Starting AI Assistant Backend Server (Ollama Version)...")
    print(f"Model: {MODEL_NAME}")
    print(f"Ollama URL: {OLLAMA_BASE_URL}")
    print(f"System Prompt: Loaded ({len(SYSTEM_PROMPT)} characters)")
    
    # Check if Ollama is available
    if ollama_client.check_model_availability():
        print("✅ Ollama access verified")
    else:
        print("⚠️  Could not verify Ollama access - make sure Ollama is running and model is available")
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=PORT, debug=False)

#!/usr/bin/env python3
"""
AI Assistant Backend Server - Hugging Face Version
Uses Hugging Face Inference API for AI model inference
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
HF_API_URL = "https://api-inference.huggingface.co/models"
MODEL_NAME = os.getenv("MODEL_NAME", "microsoft/DialoGPT-medium")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
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

class HuggingFaceClient:
    def __init__(self, api_token=None):
        self.api_token = api_token or HF_API_TOKEN
        self.model = MODEL_NAME
        self.api_url = f"{HF_API_URL}/{self.model}"
    
    def check_model_availability(self):
        """Check if the model is available via Hugging Face API"""
        try:
            if not self.api_token:
                print("Warning: HF_API_TOKEN not set. Some models may not be accessible.")
                return False
            
            # Check if we can access the model
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(self.api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print("Invalid Hugging Face API token")
                return False
            elif response.status_code == 404:
                print(f"Model {self.model} not found on Hugging Face")
                return False
            else:
                print(f"Hugging Face API check failed: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Hugging Face API check error: {e}")
            return False
    
    def generate_response(self, message, conversation_history=None):
        """Generate a response using Hugging Face Inference API"""
        try:
            # Prepare the input text
            # For conversational models, we'll format the conversation
            if conversation_history:
                # Build conversation context
                context = SYSTEM_PROMPT + "\n\n"
                for msg in conversation_history[-5:]:  # Keep last 5 messages
                    if msg["role"] == "user":
                        context += f"Human: {msg['content']}\n"
                    else:
                        context += f"Assistant: {msg['content']}\n"
                context += f"Human: {message}\nAssistant:"
            else:
                context = f"{SYSTEM_PROMPT}\n\nHuman: {message}\nAssistant:"
            
            # Prepare headers
            headers = {}
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            
            # Prepare payload for Hugging Face API
            payload = {
                "inputs": context,
                "parameters": {
                    "max_length": 300,
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            # Make request to Hugging Face API
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        return result[0]['generated_text'].strip()
                    elif 'text' in result[0]:
                        return result[0]['text'].strip()
                return "Sorry, I could not generate a response."
            elif response.status_code == 503:
                # Model is loading
                return "The AI model is currently loading. Please try again in a few moments."
            elif response.status_code == 401:
                return "Authentication failed. Please check the API token configuration."
            elif response.status_code == 429:
                return "Rate limit exceeded. Please try again later."
            else:
                print(f"Hugging Face API error: {response.status_code} - {response.text}")
                return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Sorry, an unexpected error occurred. Please try again."

# Initialize Hugging Face client
hf_client = HuggingFaceClient()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "hf_api_available": hf_client.check_model_availability()
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
        response = hf_client.generate_response(message, conversation_history)
        
        return jsonify({
            "response": response,
            "model": MODEL_NAME
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/models', methods=['GET'])
def list_models():
    """Get current model information"""
    try:
        return jsonify({
            "current_model": MODEL_NAME,
            "model_type": "Hugging Face Inference API",
            "api_url": f"{HF_API_URL}/{MODEL_NAME}",
            "note": "This endpoint shows the current model. To change models, update the MODEL_NAME environment variable."
        })
    except Exception as e:
        return jsonify({"error": f"Error getting model info: {e}"}), 500

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
    print("Starting AI Assistant Backend Server (Hugging Face Version)...")
    print(f"Model: {MODEL_NAME}")
    print(f"Hugging Face API URL: {HF_API_URL}/{MODEL_NAME}")
    print(f"System Prompt: Loaded ({len(SYSTEM_PROMPT)} characters)")
    
    # Check if Hugging Face API is available
    if hf_client.check_model_availability():
        print("✅ Hugging Face API access verified")
    else:
        print("⚠️  Could not verify Hugging Face API access - make sure HF_API_TOKEN is set and model is available")
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=PORT, debug=False)

#!/usr/bin/env python3
"""
AI Assistant Backend Server - Hugging Face Version
Uses Hugging Face Inference API (free tier: 30,000 requests/month)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY")  # Optional, but recommended for higher limits
MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-2b-it")
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
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = MODEL_NAME
        self.base_url = "https://api-inference.huggingface.co"
    
    def check_model_availability(self):
        """Check if the model is available in Hugging Face"""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            response = requests.get(f"{self.base_url}/models/{self.model}", headers=headers, timeout=10)
            if response.status_code == 200:
                return True
            else:
                print(f"Model check failed: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Model check error: {e}")
            return False
    
    def generate_response(self, message, conversation_history=None):
        """Generate a response using Hugging Face API"""
        try:
            # Prepare the prompt for Gemma (instruction-tuned conversational model)
            prompt = f"<start_of_turn>user\n{message}<end_of_turn>\n<start_of_turn>model\n"
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
                "Content-Type": "application/json"
            }
            
            # Remove None values from headers
            headers = {k: v for k, v in headers.items() if v is not None}
            
            # Prepare payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.8,
                    "do_sample": True,
                    "return_full_text": False,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            }
            
            # Make request to Hugging Face
            response = requests.post(
                f"{self.base_url}/models/{self.model}",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', 'Sorry, I could not generate a response.')
                else:
                    return "Sorry, I could not generate a response."
            else:
                print(f"Hugging Face API error: {response.status_code} - {response.text}")
                if response.status_code == 404:
                    return "Sorry, the AI model is not available. Please try again later or contact support."
                elif response.status_code == 401:
                    return "Sorry, there's an authentication issue with the AI service. Please try again later."
                else:
                    return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Sorry, an unexpected error occurred. Please try again."

# Initialize Hugging Face client
hf_client = HuggingFaceClient(HF_API_KEY)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "api_available": hf_client.check_model_availability()
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
    """List available models in Hugging Face"""
    try:
        headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
        response = requests.get(f"https://api-inference.huggingface.co/models/{MODEL_NAME}", headers=headers)
        if response.status_code == 200:
            return jsonify({"models": [MODEL_NAME]})
        else:
            return jsonify({"error": "Could not fetch model information"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Could not connect to Hugging Face: {e}"}), 500

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
    print(f"API: Hugging Face (Free tier: 30,000 requests/month)")
    print(f"System Prompt: Loaded ({len(SYSTEM_PROMPT)} characters)")
    
    # Check if Hugging Face API is available
    if hf_client.check_model_availability():
        print("✓ Hugging Face API is accessible")
    else:
        print("⚠ Could not verify Hugging Face API access")
    
    if not HF_API_KEY:
        print("⚠ Warning: HF_API_KEY not set. Using anonymous access (lower rate limits)")
    
    # Start the Flask server
    app.run(host='0.0.0.0', port=PORT, debug=False)

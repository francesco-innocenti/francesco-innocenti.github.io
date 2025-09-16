#!/bin/bash

# Start script for AI Assistant Backend
# This script handles the startup process for the Flask application

set -e

echo "🚀 Starting AI Assistant Backend (Ollama Version)..."

# Set default environment variables if not provided
export MODEL_NAME=${MODEL_NAME:-"llama3.2:3b"}
export PORT=${PORT:-5001}
export OLLAMA_API_URL=${OLLAMA_API_URL:-"http://localhost:11434"}

echo "Configuration:"
echo "  Model: $MODEL_NAME"
echo "  Port: $PORT"
echo "  Ollama API URL: $OLLAMA_API_URL"

# Check if we're in a Railway environment
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Running in Railway environment"
    echo "   Make sure the Ollama service is deployed and accessible"
else
    echo "🏠 Running in local environment"
    echo "   Make sure Ollama is running locally on port 11434"
fi

# Start the Flask application
echo "🎯 Starting Flask application..."
exec python app.py

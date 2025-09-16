#!/bin/bash

# Start script for AI Assistant Backend
# This script handles the startup process for the Flask application

set -e

echo "🚀 Starting AI Assistant Backend..."

# Set default environment variables if not provided
export MODEL_NAME=${MODEL_NAME:-"phi3:mini"}
export PORT=${PORT:-5001}

echo "Configuration:"
echo "  Model: $MODEL_NAME"
echo "  Port: $PORT"
echo "  Ollama URL: ${OLLAMA_BASE_URL:-http://localhost:11434}"

# Check if we're in a Railway environment
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Running in Railway environment"
    # In Railway, we expect Ollama to be running as a separate service
    # The OLLAMA_BASE_URL should be set to the Ollama service URL
    if [ -z "$OLLAMA_BASE_URL" ]; then
        echo "⚠️  OLLAMA_BASE_URL not set in Railway environment"
        echo "   Please set OLLAMA_BASE_URL to your Ollama service URL"
    fi
else
    echo "🏠 Running in local environment"
    # For local development, default to localhost
    export OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-"http://localhost:11434"}
fi

# Start the Flask application
echo "🎯 Starting Flask application..."
exec python app.py

#!/bin/bash

# Start script for AI Assistant Backend
# This script handles the startup process for the Flask application

set -e

echo "🚀 Starting AI Assistant Backend (Hugging Face Version)..."

# Set default environment variables if not provided
export MODEL_NAME=${MODEL_NAME:-"microsoft/DialoGPT-medium"}
export PORT=${PORT:-5001}

echo "Configuration:"
echo "  Model: $MODEL_NAME"
echo "  Port: $PORT"
echo "  Hugging Face API Token: ${HF_API_TOKEN:+[SET]}"

# Check if we're in a Railway environment
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Running in Railway environment"
    if [ -z "$HF_API_TOKEN" ]; then
        echo "⚠️  HF_API_TOKEN not set in Railway environment"
        echo "   Please set HF_API_TOKEN to your Hugging Face API token"
        echo "   You can get one from: https://huggingface.co/settings/tokens"
    fi
else
    echo "🏠 Running in local environment"
    if [ -z "$HF_API_TOKEN" ]; then
        echo "⚠️  HF_API_TOKEN not set - some models may not be accessible"
        echo "   You can get a free token from: https://huggingface.co/settings/tokens"
    fi
fi

# Start the Flask application
echo "🎯 Starting Flask application..."
exec python app.py

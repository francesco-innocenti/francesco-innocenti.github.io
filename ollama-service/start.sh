#!/bin/bash

# Start script for Ollama Service
# This script handles the startup process for the Ollama server

set -e

echo "🚀 Starting Ollama Service..."

# Set default environment variables if not provided
export OLLAMA_HOST=${OLLAMA_HOST:-"0.0.0.0"}
export OLLAMA_PORT=${OLLAMA_PORT:-11434}

echo "Configuration:"
echo "  Host: $OLLAMA_HOST"
echo "  Port: $OLLAMA_PORT"

# Check if we're in a Railway environment
if [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo "✅ Running in Railway environment"
else
    echo "🏠 Running in local environment"
fi

# Start Ollama server
echo "🎯 Starting Ollama server..."
exec ollama serve
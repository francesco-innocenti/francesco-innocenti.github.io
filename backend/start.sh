#!/bin/bash

# Exit on any error
set -e

echo "Starting Ollama AI Assistant..."

# Start Ollama in the background
echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Shutting down..."
    kill $OLLAMA_PID 2>/dev/null || true
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Wait for Ollama to start
echo "Waiting for Ollama to start..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
    fi
    echo "Waiting for Ollama... ($i/30)"
    sleep 2
done

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Failed to start Ollama service"
    exit 1
fi

# Pull the model if not already available
echo "Ensuring model ${MODEL_NAME} is available..."
ollama pull ${MODEL_NAME} || {
    echo "Failed to pull model ${MODEL_NAME}"
    exit 1
}

echo "Model ${MODEL_NAME} is ready!"

# Start the Flask application
echo "Starting Flask application..."
python3 app.py

#!/bin/bash

set -e

echo "Starting Ollama service..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found, trying to install..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Verify Ollama installation
if ! command -v ollama &> /dev/null; then
    echo "Failed to install Ollama"
    exit 1
fi

echo "Ollama found at: $(which ollama)"

# Start Ollama in the background
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

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
echo "Ollama service is running on port 11434"

# Keep the service running
wait $OLLAMA_PID

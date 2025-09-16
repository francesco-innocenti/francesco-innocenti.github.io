#!/bin/bash

# AI Assistant Local Setup Script
# This script sets up the local development environment

set -e

echo "🔧 Setting up AI Assistant for local development..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📥 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✅ Ollama installed successfully"
else
    echo "✅ Ollama is already installed"
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if jq is installed (for JSON parsing)
if ! command -v jq &> /dev/null; then
    echo "📥 Installing jq..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install jq
        else
            echo "❌ Please install jq manually: https://stedolan.github.io/jq/"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y jq
    else
        echo "❌ Please install jq manually: https://stedolan.github.io/jq/"
        exit 1
    fi
    echo "✅ jq installed successfully"
else
    echo "✅ jq is already installed"
fi

# Create virtual environment for backend
echo "📦 Setting up Python virtual environment..."
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python dependencies installed"

cd ..

# Make startup script executable
chmod +x start-local.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Pull a model: ollama pull llama3.2:3b"
echo "2. Start the services: ./start-local.sh"
echo ""
echo "Available models to try:"
echo "  - llama3.2:3b (good balance)"
echo "  - llama3.2:7b (higher quality)"
echo "  - gemma2:9b (Google's model)"
echo "  - qwen2.5:7b (alternative)"
echo ""
echo "Run './start-local.sh' to start the AI Assistant!"

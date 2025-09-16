#!/bin/bash

# AI Assistant Local Startup Script
# This script starts both Ollama and the backend service locally

set -e

echo "🚀 Starting AI Assistant Locally..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it first:"
    echo "   curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Start Ollama in background
echo "🤖 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Failed to start Ollama. Please check if port 11434 is available."
    kill $OLLAMA_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Ollama is running on http://localhost:11434"

# Check if a model is available
MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "")
if [ -z "$MODELS" ]; then
    echo "⚠️  No models found. Please pull a model first:"
    echo "   ollama pull llama3.2:3b"
    echo "   or"
    echo "   ollama pull gemma2:9b"
    echo ""
    echo "Continuing anyway - you can pull models later..."
fi

# Set environment variables
export OLLAMA_API_URL="http://localhost:11434"
export MODEL_NAME="llama3.2:3b"
export PORT="5001"

# Start the backend
echo "🌐 Starting backend server..."
cd backend

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "🎯 Starting Flask backend..."
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if ! curl -s http://localhost:5001/health > /dev/null; then
    echo "❌ Failed to start backend. Please check if port 5001 is available."
    kill $OLLAMA_PID $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Backend is running on http://localhost:5001"
echo ""
echo "🎉 AI Assistant is ready!"
echo "   - Ollama: http://localhost:11434"
echo "   - Backend: http://localhost:5001"
echo "   - Health: http://localhost:5001/health"
echo ""
echo "To test the chat:"
echo "   curl -X POST http://localhost:5001/chat \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"message\":\"Hello, how are you?\"}'"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $OLLAMA_PID $BACKEND_PID 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait

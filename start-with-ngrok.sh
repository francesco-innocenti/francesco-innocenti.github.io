#!/bin/bash

# AI Assistant with ngrok Public Access
# This script starts the AI Assistant and exposes it publicly via ngrok

set -e

echo "🌐 Starting AI Assistant with public access..."

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it first:"
    echo "   brew install ngrok"
    echo "   or download from https://ngrok.com/download"
    exit 1
fi

# Check if ngrok is authenticated
if ! ngrok config check &> /dev/null; then
    echo "❌ ngrok is not authenticated. Please run:"
    echo "   ngrok config add-authtoken YOUR_AUTHTOKEN"
    exit 1
fi

# Start the AI Assistant in background
echo "🚀 Starting AI Assistant..."
./start-local.sh &
AI_PID=$!

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is running
if ! curl -s http://localhost:5001/health > /dev/null; then
    echo "❌ Backend is not running. Please check the logs."
    kill $AI_PID 2>/dev/null || true
    exit 1
fi

echo "✅ AI Assistant is running locally"

# Start ngrok tunnel
echo "🌐 Starting ngrok tunnel..."
ngrok http 5001 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 5

# Get the public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url' 2>/dev/null || echo "")

if [ -z "$PUBLIC_URL" ] || [ "$PUBLIC_URL" = "null" ]; then
    echo "❌ Failed to get ngrok URL. Please check ngrok status."
    kill $AI_PID $NGROK_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "🎉 AI Assistant is now publicly accessible!"
echo "   - Local: http://localhost:5001"
echo "   - Public: $PUBLIC_URL"
echo ""
echo "📝 Update your frontend config:"
echo "   Replace 'YOUR_NGROK_URL.ngrok.io' in _pages/ai-assistant-config.js with:"
echo "   $PUBLIC_URL"
echo ""
echo "🧪 Test the public endpoint:"
echo "   curl -X POST $PUBLIC_URL/chat \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"message\":\"Hello, how are you?\"}'"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $AI_PID $NGROK_PID 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait

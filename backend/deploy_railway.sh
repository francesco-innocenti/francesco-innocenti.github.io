#!/bin/bash

# Railway Deployment Script for Ollama AI Assistant
# This script helps deploy the AI assistant to Railway

set -e

echo "🚀 Deploying AI Assistant with Ollama to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed. Please install it first:"
    echo "   npm install -g @railway/cli"
    echo "   or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

# Check if user is logged in to Railway
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please login first:"
    echo "   railway login"
    exit 1
fi

echo "✅ Railway CLI is ready"

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if all required files exist
required_files=("app.py" "Dockerfile" "start.sh" "requirements.txt" "system_prompt.txt" "railway.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Required file missing: $file"
        exit 1
    fi
done

echo "✅ All required files present"

# Set environment variables for Railway
echo "🔧 Setting up environment variables..."

# You can customize these values
MODEL_NAME=${MODEL_NAME:-"gemma3:1b"}
OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-"http://localhost:11434"}
PORT=${PORT:-5001}

echo "Model: $MODEL_NAME"
echo "Ollama URL: $OLLAMA_BASE_URL"
echo "Port: $PORT"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your Railway dashboard to monitor the deployment"
echo "2. Set environment variables in Railway dashboard if needed:"
echo "   - MODEL_NAME: $MODEL_NAME"
echo "   - OLLAMA_BASE_URL: $OLLAMA_BASE_URL"
echo "   - PORT: $PORT"
echo "3. Wait for the deployment to complete (this may take several minutes)"
echo "4. Test your deployment with: curl https://your-app.railway.app/health"
echo ""
echo "⚠️  Note: The first deployment may take longer as Ollama needs to download the model."
echo "   Monitor the logs in Railway dashboard for progress."

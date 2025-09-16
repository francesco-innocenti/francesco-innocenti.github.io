# Ollama Service for AI Assistant
FROM ubuntu:22.04

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_PORT=11434

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose Ollama port
EXPOSE 11434

# Start Ollama server as root (required for Railway networking)
CMD ["/usr/local/bin/ollama", "serve", "--host", "0.0.0.0:11434"]
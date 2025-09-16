# Ollama Service for AI Assistant
FROM ubuntu:22.04

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create a non-root user
RUN useradd -m -s /bin/bash ollama

# Switch to ollama user
USER ollama

# Expose Ollama port
EXPOSE 11434

# Let Railway handle health checks

# Start Ollama server
CMD ["/usr/local/bin/ollama", "serve"]
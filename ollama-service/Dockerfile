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

# Create a simple health check script
RUN echo '#!/bin/bash\ncurl -f http://localhost:11434/api/tags || exit 1' > /healthcheck.sh && chmod +x /healthcheck.sh

# Expose Ollama port
EXPOSE 11434

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /healthcheck.sh

# Start Ollama server
CMD ["/usr/local/bin/ollama", "serve"]
# Ollama-only service
FROM alpine:3.18

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV MODEL_NAME=phi3:mini

# Install system dependencies
RUN apk add --no-cache \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama service..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to start\n\
echo "Waiting for Ollama to start..."\n\
for i in {1..30}; do\n\
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then\n\
        echo "Ollama is ready!"\n\
        break\n\
    fi\n\
    echo "Waiting for Ollama... ($i/30)"\n\
    sleep 2\n\
done\n\
\n\
# Pull the model\n\
echo "Pulling model ${MODEL_NAME}..."\n\
ollama pull ${MODEL_NAME}\n\
\n\
echo "Ollama service ready with model ${MODEL_NAME}"\n\
\n\
# Keep the service running\n\
wait $OLLAMA_PID\n\
' > /start-ollama.sh && chmod +x /start-ollama.sh

# Expose Ollama port
EXPOSE 11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Start Ollama
CMD ["/start-ollama.sh"]

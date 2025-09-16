# Ollama Service
FROM alpine:3.18

ENV OLLAMA_HOST=0.0.0.0:11434
ENV MODEL_NAME=phi3:mini

RUN apk add --no-cache curl bash && rm -rf /var/cache/apk/*

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
for i in {1..30}; do\n\
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then\n\
        echo "Ollama ready!"\n\
        break\n\
    fi\n\
    echo "Waiting... ($i/30)"\n\
    sleep 2\n\
done\n\
\n\
echo "Pulling model ${MODEL_NAME}..."\n\
ollama pull ${MODEL_NAME}\n\
\n\
echo "Service ready!"\n\
wait $OLLAMA_PID\n\
' > /start.sh && chmod +x /start.sh

EXPOSE 11434

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

CMD ["/start.sh"]

# Ollama Service
FROM alpine:3.18

ENV OLLAMA_HOST=0.0.0.0:11434
ENV MODEL_NAME=phi3:mini

RUN apk add --no-cache curl bash && rm -rf /var/cache/apk/*

RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 11434

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

CMD ["/start.sh"]

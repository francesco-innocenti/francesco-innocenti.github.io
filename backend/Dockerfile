# AI Assistant Backend Service
FROM python:3.11-alpine

# Set environment variables
ENV MODEL_NAME=llama3.2:3b
ENV PORT=5001
ENV OLLAMA_API_URL=http://localhost:11434

# Install system dependencies
RUN apk add --no-cache \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY system_prompt.txt .
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Expose Flask port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start the Flask application using the start script
CMD ["./start.sh"]

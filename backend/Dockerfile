# Lightweight Flask-only service
FROM python:3.11-alpine

# Set environment variables
ENV MODEL_NAME=phi3:mini
ENV PORT=5001

# Install system dependencies
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend/app.py .
COPY backend/system_prompt.txt .

# Expose Flask port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5001/health || exit 1

# Start the Flask application
CMD ["python", "app.py"]

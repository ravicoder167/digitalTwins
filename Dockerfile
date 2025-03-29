# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    STATIC_ROOT=/app/staticfiles \
    STATIC_URL=/static/ \
    DEBUG=0 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        netcat-traditional \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Set permissions for Cloud Run
RUN chmod -R 755 /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Set proper permissions for startup script
COPY startup.sh .
RUN sed -i 's/\r$//' startup.sh && \
    chmod +x startup.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health/ || exit 1

# Use the startup script as entrypoint
ENTRYPOINT ["./startup.sh"]

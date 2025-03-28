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

# Create and switch to a non-root user
RUN useradd -m -s /bin/bash app \
    && chown -R app:app /app
USER app

# Create necessary directories with correct permissions
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app/staticfiles /app/media

# Install Python dependencies with retry logic
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    for i in {1..5}; do pip install --no-cache-dir -r requirements.txt && break || sleep 15; done

# Install gunicorn separately
RUN pip install gunicorn

# Set PATH to include the local bin directory
ENV PATH="/home/app/.local/bin:${PATH}"

# Copy project files
COPY --chown=app:app . .

# Create a startup script with proper line endings
COPY --chown=app:app startup.sh .
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

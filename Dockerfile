# Use Python 3.11 slim image
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user
RUN useradd -m -s /bin/bash app \
    && chown -R app:app /app
USER app

# Create necessary directories with correct permissions
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R app:app /app/staticfiles /app/media

# Install Python dependencies
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=app:app . .

# Create a startup script
COPY --chown=app:app startup.sh .
RUN chmod +x startup.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Use the startup script as entrypoint
ENTRYPOINT ["./startup.sh"]

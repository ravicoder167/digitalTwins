# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    STATIC_ROOT=/app/staticfiles \
    STATIC_URL=/static/ \
    DEBUG=False \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=digital_twins.settings

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

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8080

# Install Gunicorn
RUN pip install gunicorn

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Environment variables:"\n\
env | sort\n\
echo "Starting Gunicorn..."\n\
exec gunicorn digital_twins.wsgi:application --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level debug \
    --access-logfile "-" \
    --error-logfile "-" \
    --capture-output \
    --enable-stdio-inheritance \
    --max-requests 1200 \
    --max-requests-jitter 50 \
    --graceful-timeout 30' > /app/startup.sh && \
    chmod +x /app/startup.sh

# Start using the startup script
CMD ["/app/startup.sh"]

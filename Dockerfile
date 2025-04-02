# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    STATIC_ROOT=/app/staticfiles \
    STATIC_URL=/static/ \
    DEBUG=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=digital_twins.settings \
    PATH="/app:${PATH}" \
    HOME=/app

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

# Create necessary directories and set permissions
RUN mkdir -p /app/staticfiles /app/media \
    && chown -R 1000:1000 /app \
    && chmod -R 755 /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy project files
COPY . .

# Convert line endings and set permissions
RUN find /app -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; && \
    find /app -type f -name "*.sh" -exec chmod +x {} \; && \
    chmod +x /app/startup.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Use gunicorn directly
CMD exec gunicorn digital_twins.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 2 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output

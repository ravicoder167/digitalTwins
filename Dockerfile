# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    STATIC_ROOT=/app/staticfiles \
    STATIC_URL=/static/ \
    DEBUG=0

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a non-root user
RUN useradd -m -s /bin/bash app \
    && chown -R app:app /app
USER app

# Create directory for static files
RUN mkdir -p /app/staticfiles && chown -R app:app /app/staticfiles

# Install Python dependencies
COPY --chown=app:app requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=app:app . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Start Gunicorn
CMD exec gunicorn digital_twins.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 0

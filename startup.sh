#!/bin/bash
set -e  # Exit on error

# Function to log messages with timestamps
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Handle SIGTERM gracefully
handle_sigterm() {
    log "Received SIGTERM signal"
    kill -TERM "$child" 2>/dev/null
    wait "$child"
    exit 0
}
trap handle_sigterm SIGTERM

# Set startup time
export STARTUP_TIME=$(date +%s)
log "Setting STARTUP_TIME to: ${STARTUP_TIME}"

log "Starting application setup..."
log "Current working directory: $(pwd)"
log "Python version: $(python --version)"

# Check required environment variables
log "Checking environment variables..."
for var in PORT STATIC_ROOT DATABASE_URL SECRET_KEY; do
    if [ -z "${!var}" ]; then
        log "Warning: $var is not set"
    else
        log "$var is set"
    fi
done

# Ensure PORT is set
if [ -z "$PORT" ]; then
    export PORT=8080
    log "PORT not set, defaulting to 8080"
fi

# Wait for the database if needed
if [ -n "$DATABASE_URL" ]; then
    log "Waiting for database..."
    HOST=$(echo $DATABASE_URL | awk -F[@//] '{print $4}')
    DB_PORT=$(echo $DATABASE_URL | awk -F[:] '{print $4}' | awk -F[/] '{print $1}')
    
    if [ -n "$HOST" ] && [ -n "$DB_PORT" ]; then
        log "Checking database connection: $HOST:$DB_PORT"
        RETRIES=30
        COUNTER=0
        until nc -z $HOST $DB_PORT; do
            COUNTER=$((COUNTER+1))
            if [ $COUNTER -eq $RETRIES ]; then
                log "Database connection failed after $RETRIES attempts"
                exit 1
            fi
            log "Database is unavailable - sleeping (attempt $COUNTER/$RETRIES)"
            sleep 2
        done
        log "Database is up and running!"
    fi
fi

# Apply database migrations
log "Applying database migrations..."
python manage.py migrate --noinput

# Verify static files
log "Checking static files..."
if [ ! -d "$STATIC_ROOT" ]; then
    log "Static root directory not found, creating..."
    mkdir -p $STATIC_ROOT
fi

log "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
log "Starting Gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn digital_twins.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --threads 2 \
    --timeout 120 \
    --graceful-timeout 60 \
    --keep-alive 65 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output \
    --preload \
    --worker-tmp-dir /dev/shm \
    --worker-class gthread

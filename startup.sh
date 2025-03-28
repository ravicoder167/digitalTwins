#!/bin/bash
set -e  # Exit on error

# Add user-specific Python scripts to PATH
export PATH="$PATH:$HOME/AppData/Roaming/Python/Python310/Scripts"

echo "Starting application setup..."

# Ensure PORT is set
if [ -z "$PORT" ]; then
    export PORT=8080
    echo "PORT not set, defaulting to 8080"
fi

# Wait for the database if needed
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    HOST=$(echo $DATABASE_URL | awk -F[@//] '{print $4}')
    DB_PORT=$(echo $DATABASE_URL | awk -F[:] '{print $4}' | awk -F[/] '{print $1}')
    
    if [ -n "$HOST" ] && [ -n "$DB_PORT" ]; then
        echo "Checking database connection: $HOST:$DB_PORT"
        until nc -z $HOST $DB_PORT; do
            echo "Database is unavailable - sleeping"
            sleep 1
        done
        echo "Database is up and running!"
    fi
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Verify static files
echo "Checking static files..."
if [ ! -d "$STATIC_ROOT" ]; then
    echo "Static root directory not found, creating..."
    mkdir -p $STATIC_ROOT
    python manage.py collectstatic --noinput
fi

# Start Gunicorn
echo "Starting Gunicorn on 0.0.0.0:${PORT}..."
exec gunicorn digital_twins.wsgi:application \
    --name digital_twins \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --threads 2 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --capture-output \
    --enable-stdio-inheritance \
    --preload

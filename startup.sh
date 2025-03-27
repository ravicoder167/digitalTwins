#!/bin/bash

# Wait for the database if needed (useful when database is starting up)
if [ -n "$DATABASE_URL" ]; then
    echo "Waiting for database..."
    HOST=$(echo $DATABASE_URL | awk -F[@//] '{print $4}')
    PORT=$(echo $DATABASE_URL | awk -F[:] '{print $4}' | awk -F[/] '{print $1}')
    
    if [ -n "$HOST" ] && [ -n "$PORT" ]; then
        while ! nc -z $HOST $PORT; do
            sleep 1
        done
    fi
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn digital_twins.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 2 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance

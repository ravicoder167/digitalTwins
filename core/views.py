from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

from django.shortcuts import render, redirect
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        # For now, just redirect back to the home page
        # You can add form processing logic here later
        return redirect('core:home')
    return render(request, 'core/home.html')

def health_check(request):
    """
    Health check endpoint for Cloud Run
    Checks:
    1. Application is responding
    2. Database connection is working
    """
    try:
        # Test database connection
        db_conn = connections['default']
        db_conn.cursor()
        db_status = True
    except OperationalError:
        db_status = False

    status = {
        'status': 'healthy',
        'database': 'connected' if db_status else 'disconnected'
    }
    
    # Return 503 if database is not connected
    status_code = 200 if db_status else 503
    
    return JsonResponse(status, status=status_code)

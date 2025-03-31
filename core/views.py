from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                # Send email
                subject = f"New contact form submission from {name}"
                email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
                
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                messages.error(request, "Failed to send email. Please try again later.")
            return redirect('core:home')  # Add back the namespace
    
    form = ContactForm()  # Move form creation outside if/else
    return render(request, 'core/home.html', {'form': form})

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

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    logger.info("Home view accessed")
    if request.method == 'POST':
        logger.info("POST request received")
        form = ContactForm(request.POST)
        if form.is_valid():
            logger.info("Form is valid")
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                # Send email
                subject = f"New contact form submission from {name}"
                email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
                
                logger.info("Email sent successfully")
                messages.success(request, "Your message has been sent successfully!")
            except Exception as e:
                logger.error(f"Failed to send email: {str(e)}")
                messages.error(request, "Failed to send email. Please try again later.")
            
            logger.info("Redirecting after form submission")
            return redirect('core:home')
        else:
            logger.warning(f"Form is invalid. Errors: {form.errors}")
    else:
        logger.info("GET request received")
        form = ContactForm()
    
    logger.info("Rendering home template")
    context = {
        'form': form,
        'debug': settings.DEBUG
    }
    logger.debug(f"Template context: {context}")
    return render(request, 'core/home.html', context)

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

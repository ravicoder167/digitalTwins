from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def home(request):
    logger.info("Home view accessed")
    if request.method == 'POST':
        logger.info("POST request received")
        form = ContactForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if form.is_valid():
            logger.info("Form is valid")
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                # Log all form data
                logger.info("Processing contact form submission:")
                logger.info(f"Name: {name}")
                logger.info(f"Email: {email}")
                logger.info(f"Message length: {len(message)} characters")

                # Log email settings before sending
                logger.info("Email configuration:")
                logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
                logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
                logger.info(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
                logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
                logger.info(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
                logger.info(f"CONTACT_EMAIL: {settings.CONTACT_EMAIL}")

                # Prepare email
                subject = f"New contact form submission from {name}"
                email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                logger.info("Attempting to send email...")
                logger.info(f"Subject: {subject}")
                logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}")
                logger.info(f"To: {settings.CONTACT_EMAIL}")

                # Send email with detailed logging
                try:
                    send_mail(
                        subject,
                        email_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.CONTACT_EMAIL],
                        fail_silently=False,
                    )
                    logger.info("Email sent successfully")
                except Exception as mail_error:
                    logger.error(f"Email sending failed with error: {str(mail_error)}")
                    logger.error("Email error details:", exc_info=True)
                    raise  # Re-raise the exception to be caught by the outer try block
                
                # Check if it's an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success'})
                else:
                    messages.success(request, "Your message has been sent successfully!")
                    return redirect('core:home')
                    
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Failed to send email: {error_msg}", exc_info=True)
                logger.error(f"Email settings: DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}, CONTACT_EMAIL: {settings.CONTACT_EMAIL}")
                
                # Check if it's an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    error_details = {
                        'status': 'error',
                        'message': 'Failed to send email',
                        'details': error_msg,
                        'email_settings': {
                            'host': settings.EMAIL_HOST,
                            'port': settings.EMAIL_PORT,
                            'use_tls': settings.EMAIL_USE_TLS,
                            'from_email': settings.DEFAULT_FROM_EMAIL,
                            'contact_email': settings.CONTACT_EMAIL
                        }
                    }
                    return JsonResponse(error_details, status=500)
                else:
                    messages.error(request, f"Failed to send email. Error: {error_msg}")
                    return redirect('core:home')
        else:
            logger.warning(f"Form is invalid. Errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
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
    2. Database connection is working (if not in startup phase)
    """
    import os
    
    # Always return 200 in the first 30 seconds to allow for startup
    import time
    startup_time = int(os.getenv('STARTUP_TIME', time.time()))
    current_time = int(time.time())
    in_startup_phase = (current_time - startup_time) < 30

    if in_startup_phase:
        return JsonResponse({
            'status': 'starting',
            'message': 'Application is starting up'
        })

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
    
    # Return 503 if database is not connected (after startup phase)
    status_code = 200 if db_status else 503
    
    return JsonResponse(status, status=status_code)

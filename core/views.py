from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactForm
import logging
import requests
import os
import json

logger = logging.getLogger(__name__)

def send_outlook_email(subject, body, cc_recipients=None, bcc_recipients=None):
    """
    Send email using Microsoft Graph API (Outlook)
    """
    try:
        # Get credentials from environment variables (GitHub secrets)
        tenant_id = os.environ.get('MS_TENANT_ID')
        client_id = os.environ.get('MS_CLIENT_ID')
        client_secret = os.environ.get('MS_CLIENT_SECRET')
        licensed_user = os.environ.get('MS_LICENSED_USER')
        from_email = 'noreply@cognitosparks.com'

        if not all([tenant_id, client_id, client_secret, licensed_user]):
            raise ValueError("Missing required Microsoft Graph API credentials")

        # Get access token
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }

        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")

        if not access_token:
            raise ValueError("Failed to retrieve access token")

        # Prepare email message
        email_message = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body
                },
                "from": {
                    "emailAddress": {
                        "address": from_email
                    }
                },
                "ccRecipients": [
                    {"emailAddress": {"address": cc}} for cc in (cc_recipients or [])
                ],
                "bccRecipients": [
                    {"emailAddress": {"address": bcc}} for bcc in (bcc_recipients or [])
                ]
            },
            "saveToSentItems": False
        }

        # Send email
        send_email_url = f"https://graph.microsoft.com/v1.0/users/{licensed_user}/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        send_response = requests.post(send_email_url, headers=headers, json=email_message)
        send_response.raise_for_status()
        logger.info(f"Email sent successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to send email via Outlook: {str(e)}", exc_info=True)
        raise

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

                # Prepare email
                subject = f"New contact form submission from {name}"
                email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                logger.info("Attempting to send email...")
                logger.info(f"Subject: {subject}")

                # Send emails using Outlook
                try:
                    # Send to admin (as BCC) with CC
                    send_outlook_email(
                        subject=subject,
                        body=email_message,
                        cc_recipients=[email],  # Use the user's email as CC
                        bcc_recipients=['info@cognitosparks.com']  # Add BCC recipient from HTML
                    )
                    
                    # Send confirmation email to sender
                    confirmation_subject = "Thank you for contacting Cognito Sparks"
                    confirmation_message = f"""Dear {name},

Thank you for reaching out to Cognito Sparks. We have received your message and will get back to you shortly.

Best regards,
The Cognito Sparks Team"""

                    send_outlook_email(
                        subject=confirmation_subject,
                        body=confirmation_message,
                        bcc_recipients=[email]  # Send to user as BCC
                    )
                    
                    logger.info("Emails sent successfully")
                    messages.success(request, "Your message has been sent successfully! A confirmation email has been sent to your inbox.")
                except Exception as mail_error:
                    error_msg = str(mail_error)
                    logger.error(f"Email sending failed with error: {error_msg}")
                    logger.error("Email error details:", exc_info=True)
                    messages.error(request, f"Failed to send email. Please try again later. Error: {error_msg}")
                
                return redirect('core:home')
                    
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Failed to process form: {error_msg}", exc_info=True)
                messages.error(request, f"An error occurred while processing your message. Please try again later.")
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

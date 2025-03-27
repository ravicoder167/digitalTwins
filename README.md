# Digital Twins Website

A modern, responsive website for DigitalTwins, showcasing IT consultancy and digital transformation services.

## Features

- Django-based web application
- Clean, organized project structure
- Key sections:
  - Home page with company overview
  - About Us section
  - Services showcase
  - Industries We Serve section
  - Contact form with server-side validation
  - Dynamic template-based pages

## Technologies Used

- Django (Python web framework)
- HTML5 (in Django templates)
- Docker for containerization
- Google Cloud Run for deployment
- PostgreSQL for production database
- Redis for caching
- WhiteNoise for static file serving

## Project Structure

```
DigitalTwins/
├── core/                   # Django app core functionality
├── digital_twins/          # Django project settings
├── static/                 # Static files
│   ├── css/               # CSS files
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
├── templates/             # HTML templates
│   └── core/             # Core app templates
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore rules
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ravicoder167/digitalTwins.git
   cd digitalTwins
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://localhost:8000` in your browser

## Docker Setup

### Build and Run Locally

1. Build the Docker image:
   ```bash
   docker build -t digital-twins .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 \
     -e SECRET_KEY=your-secret-key \
     -e DATABASE_URL=postgresql://user:password@host:5432/dbname \
     -e ALLOWED_HOSTS=localhost,127.0.0.1 \
     digital-twins
   ```

## Google Cloud Run Deployment

### Prerequisites

1. Install Google Cloud SDK
2. Configure gcloud authentication:
   ```bash
   gcloud auth configure-docker
   ```

### Deployment Steps

1. Tag the image for Google Container Registry:
   ```bash
   docker tag digital-twins gcr.io/[PROJECT-ID]/digital-twins
   ```

2. Push to Container Registry:
   ```bash
   docker push gcr.io/[PROJECT-ID]/digital-twins
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy digital-twins \
     --image gcr.io/[PROJECT-ID]/digital-twins \
     --platform managed \
     --region [REGION] \
     --allow-unauthenticated
   ```

### Environment Variables

Required environment variables for production:

```plaintext
SECRET_KEY=your-django-secret-key
DATABASE_URL=postgresql://user:password@host:5432/dbname
ALLOWED_HOSTS=your-app-url.run.app
DEBUG=0
GS_BUCKET_NAME=your-storage-bucket
REDIS_URL=redis://your-redis-host:6379/0
SENTRY_DSN=your-sentry-dsn
```

## Production Configuration

### Database Setup

1. Create a Cloud SQL PostgreSQL instance
2. Configure the connection using DATABASE_URL environment variable
3. Run migrations on deployment

### Static Files

- Configured with WhiteNoise for serving static files
- Set STATIC_ROOT and STATIC_URL in settings
- Run collectstatic during deployment

### Caching

- Redis cache backend configuration
- Cloud Memorystore instance setup
- Cache middleware configuration

### Monitoring

- Health check endpoints
- Sentry for error tracking
- Prometheus metrics
- Cloud Run monitoring and logging

## Django App Structure

### Views
- Home view: Renders the main landing page
- About view: Displays company information
- Services view: Lists IT solutions offered
- Industries view: Shows industries served
- Contact view: Handles contact form submission

### Models
- Service: Stores information about IT services
- Industry: Represents industries the company serves
- ContactSubmission: Stores submitted contact form data

### Templates
- Base template with common structure
- Page-specific templates extending the base
- Reusable components for consistent design

### Forms
- ContactForm: Handles user inquiries with validation

### URL Configuration
- Mapped views to URL patterns for easy navigation

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact:
- Email: info@digitaltwins.com
- Phone: (555) 123-4567

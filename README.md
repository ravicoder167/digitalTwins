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

## Project Structure

```
DigitalTwins/
├── core/                   # Django app core functionality
├── digital_twins/          # Django project settings
├── static/                 # Static files (if any)
├── templates/              # HTML templates
│   └── core/
└── manage.py               # Django management script
```

## Setup Instructions

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

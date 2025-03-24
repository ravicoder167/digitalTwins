# Digital Twins Website

A modern, responsive website for DigitalTwins, showcasing IT consultancy and digital transformation services.

## Features

- Responsive design that works on all devices
- Modern UI with smooth animations
- Interactive sections:
  - Hero section with call-to-action
  - About Us with company highlights
  - Services showcase with hover effects
  - Industries We Serve section
  - Contact form with validation
  - Footer with social links

## Technologies Used

- HTML5
- CSS3 (with modern features like Grid and Flexbox)
- JavaScript (ES6+)
- Django (Python web framework)
- Font Awesome for icons

## Project Structure

```
DigitalTwins/
├── core/                   # Django app core functionality
├── digital_twins/          # Django project settings
├── static/                 # Static files (CSS, JS)
│   ├── css/
│   └── js/
├── templates/             # HTML templates
│   └── core/
└── manage.py             # Django management script
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

## Features Overview

### Home Page
- Hero section with animated text and call-to-action button
- About Us section highlighting company values and expertise
- Services grid showcasing IT solutions
- Industries section with detailed service offerings

### Interactive Elements
- Smooth scroll navigation
- Hover effects on cards and buttons
- Form validation
- Responsive navigation menu

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Optimized for all screen sizes
- Touch-friendly interface

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

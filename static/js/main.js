document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    
    // Handle contact form submission
    const contactForm = document.getElementById('contactForm');
    console.log('Contact form element:', contactForm);
    
    if (contactForm) {
        // Log form submission
        contactForm.addEventListener('submit', function(e) {
            console.log('Form submission event triggered');
            console.log('Form action:', this.action);
            console.log('Form method:', this.method);
            const formData = new FormData(this);
            console.log('Final form data:', Object.fromEntries(formData));
            // Let the form submit normally
        });
    } else {
        console.error('Contact form not found in the DOM');
    }

    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

    // Learn More button scroll
    const learnMoreBtn = document.querySelector('#learn-more-btn');
    learnMoreBtn.addEventListener('click', () => {
        const aboutSection = document.querySelector('#about');
        const navHeight = document.querySelector('nav').offsetHeight;
        const targetPosition = aboutSection.offsetTop - navHeight;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    });
});

function smoothScroll(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    const targetElement = document.querySelector(targetId);
    const navHeight = document.querySelector('nav').offsetHeight;
    const targetPosition = targetElement.offsetTop - navHeight;

    window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
    });
}

// Simple animation for service cards
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

const serviceCards = document.querySelectorAll('.service-card');
serviceCards.forEach(card => {
    observer.observe(card);
});

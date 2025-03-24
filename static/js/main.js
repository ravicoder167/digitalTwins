document.addEventListener('DOMContentLoaded', () => {
    // Handle contact form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                name: this.name.value,
                email: this.email.value,
                message: this.message.value
            };

            // For now, just show an alert. This can be connected to a backend service later
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        });
    }
    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

    // Learn More button scroll
    const learnMoreBtn = document.querySelector('.cta-button');
    learnMoreBtn.addEventListener('click', () => {
        const learnMoreSection = document.querySelector('#learn-more');
        const navHeight = document.querySelector('nav').offsetHeight;
        const targetPosition = learnMoreSection.offsetTop - navHeight;

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

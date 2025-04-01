document.addEventListener('DOMContentLoaded', () => {
    // Handle contact form submission
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });
                
                if (response.ok) {
                    alert('Thank you! Your message has been sent successfully.');
                    this.reset();
                    window.location.href = '/#contact';
                } else {
                    alert('Sorry, there was an error sending your message. Please try again.');
                }
            } catch (error) {
                alert('Sorry, there was an error sending your message. Please try again.');
                console.error('Error:', error);
            }
        });
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

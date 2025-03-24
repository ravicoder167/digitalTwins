document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for navigation links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', smoothScroll);
    });

    // Learn More button animation
    const learnMoreBtn = document.querySelector('.cta-button');
    learnMoreBtn.addEventListener('click', () => {
        learnMoreBtn.classList.add('clicked');
        setTimeout(() => {
            learnMoreBtn.classList.remove('clicked');
        }, 300);
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

/**
 * HBnB Web Client - Scroll Animations
 * Professional scroll reveal animations for smooth user experience
 */

/**
 * Initialize scroll reveal animations
 */
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                // Optional: Stop observing after reveal for performance
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all scroll-reveal elements
    document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .scroll-reveal-scale').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Add scroll reveal classes to elements
 */
function addScrollRevealClasses() {
    // Add to place cards
    document.querySelectorAll('.place-card').forEach((card, index) => {
        card.classList.add('scroll-reveal');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add to review cards
    document.querySelectorAll('.review-card').forEach((card, index) => {
        card.classList.add('scroll-reveal');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add to filter section
    const filterSection = document.querySelector('.filter-section');
    if (filterSection) {
        filterSection.classList.add('scroll-reveal');
    }

    // Add to place details
    const placeDetails = document.querySelector('.place-details');
    if (placeDetails) {
        placeDetails.classList.add('scroll-reveal-scale');
    }
}

/**
 * Smooth scroll to element
 */
function smoothScrollTo(element, offset = 0) {
    const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;
    const offsetPosition = elementPosition - offset;

    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

/**
 * Parallax effect for hero section (subtle)
 */
function initParallax() {
    const hero = document.querySelector('main h1');
    if (!hero) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.3;
        
        if (hero && scrolled < 500) {
            hero.style.transform = `translateY(${rate}px)`;
            hero.style.opacity = 1 - (scrolled / 500) * 0.3;
        }
    });
}

/**
 * Add loading shimmer effect
 */
function addShimmerEffect(element) {
    if (!element) return;
    
    element.style.background = 'linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)';
    element.style.backgroundSize = '200% 100%';
    element.style.animation = 'shimmer 1.5s infinite';
}

/**
 * Remove shimmer effect
 */
function removeShimmerEffect(element) {
    if (!element) return;
    
    element.style.background = '';
    element.style.backgroundSize = '';
    element.style.animation = '';
}

/**
 * Add scroll effect to header
 */
function initHeaderScroll() {
    let lastScroll = 0;
    const header = document.querySelector('header');
    
    if (!header) return;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initScrollReveal();
        addScrollRevealClasses();
        initParallax();
        initHeaderScroll();
    });
} else {
    initScrollReveal();
    addScrollRevealClasses();
    initParallax();
    initHeaderScroll();
}

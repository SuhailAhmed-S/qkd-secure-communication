/* ============================================================================
   QUANTUM CIPHER - INTERACTIVE JAVASCRIPT
   Smooth interactions, animations, and microinteractions
   ============================================================================ */

document.addEventListener('DOMContentLoaded', function() {
    initializeInteractions();
    addScrollEffects();
    enhanceButtons();
});

/**
 * Initialize general page interactions
 */
function initializeInteractions() {
    // Add smooth transitions to all links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

/**
 * Add scroll effects for elements
 */
function addScrollEffects() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe cards and timeline items
    document.querySelectorAll('.about-card, .feature, .timeline-content').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 600ms ease-out, transform 600ms ease-out';
        observer.observe(element);
    });
}

/**
 * Enhance button interactions
 */
function enhanceButtons() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // Add ripple effect
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.width = '1px';
            ripple.style.height = '1px';
            ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.6)';
            ripple.style.borderRadius = '50%';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple-expand 600ms ease-out';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

/**
 * Add scroll position indicator (optional enhancement)
 */
function addScrollIndicator() {
    const scrollIndicator = document.createElement('div');
    scrollIndicator.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d9ff, #da00ff);
        z-index: 2000;
        width: 0%;
        transition: width 100ms ease-out;
    `;
    document.body.appendChild(scrollIndicator);
    
    window.addEventListener('scroll', () => {
        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
        scrollIndicator.style.width = scrollPercent + '%';
    });
}

// Add scroll indicator on load
window.addEventListener('load', addScrollIndicator);

/* ──────────────────────────────────────────────────────────────────────────
   CSS animation for ripple effect (added dynamically)
   ────────────────────────────────────────────────────────────────────────── */

const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-expand {
        to {
            transform: scale(100);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('Quantum Cipher - Interactive features enabled');

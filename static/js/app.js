
// --- Safe JSON Fetch Wrapper ---
async function safeJsonFetch(response) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return await response.json();
    } else {
        const text = await response.text();
        console.error("Non-JSON response received:", text.substring(0, 200));
        throw new Error("Server returned an invalid or HTML response. (Possible Network/Server Error)");
    }
}

/**
 * AI Career Companion - Global App Router & Shared Utilities
 */

// Global Application State
window.AppState = {
    currentSection: 'home',
    theme: 'light',
    analyzedResumeText: '',
    analyzedSkills: {},
    sampleResumes: {},
    currentQuizQuestions: [],
    userQuizAnswers: {}
};

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    fetchSampleResumes();
    initDropZone();
    initHeroDarkElementsParallax();

    // Default load faculty and alumni data
    if (typeof fetchAlumniExperiences === 'function') fetchAlumniExperiences();
    if (typeof initFacultyDashboard === 'function') initFacultyDashboard();
});

/* ==========================================================================
   ROUTING & SECTION SWITCHING
   ========================================================================== */
function navigateTo(sectionId) {
    window.AppState.currentSection = sectionId;

    // Auto-close mobile drawer if open
    const navMenu = document.getElementById('nav-menu');
    const mobileBtn = document.getElementById('mobile-toggle');
    if (navMenu && navMenu.classList.contains('mobile-open')) {
        navMenu.classList.remove('mobile-open');
        if (mobileBtn) mobileBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
    }

    // Update active navbar links
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Update active section visibility
    document.querySelectorAll('.app-section').forEach(sec => {
        sec.classList.remove('active');
    });

    const targetSec = document.getElementById(`section-${sectionId}`);
    if (targetSec) {
        targetSec.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Module-specific initializers when navigating
    if (sectionId === 'prep') {
        if (typeof renderTopScorerCards === 'function') renderTopScorerCards();
        // Do NOT autostart test - student initiates test manually
    }
}

function initNavigation() {
    // Handle URL hash changes
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash.replace('#', '') || 'home';
        navigateTo(hash);
    });

    // Mobile menu toggle
    const mobileBtn = document.getElementById('mobile-toggle');
    const navMenu = document.getElementById('nav-menu');
    if (mobileBtn && navMenu) {
        mobileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = navMenu.classList.toggle('mobile-open');
            mobileBtn.innerHTML = isOpen ? '<i class="fa-solid fa-xmark"></i>' : '<i class="fa-solid fa-bars"></i>';
        });

        // Close on clicking anywhere outside
        document.addEventListener('click', (e) => {
            if (navMenu.classList.contains('mobile-open') && !navMenu.contains(e.target) && !mobileBtn.contains(e.target)) {
                navMenu.classList.remove('mobile-open');
                mobileBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            }
        });
    }

    // Set initial section from hash if present
    const initialHash = window.location.hash.replace('#', '');
    if (initialHash) {
        navigateTo(initialHash);
    }
}


/* ==========================================================================
   TOAST NOTIFICATION SYSTEM
   ========================================================================== */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-circle-check';
    if (type === 'error') icon = 'fa-triangle-exclamation';

    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/* ==========================================================================
   SAMPLE RESUME LOADER
   ========================================================================== */
async function fetchSampleResumes() {
    try {
        const res = await fetch('/api/sample-resumes');
        const data = await safeJsonFetch(res);
        if (data.success) {
            window.AppState.sampleResumes = data.resumes;
        }
    } catch (err) {
        console.warn('Could not pre-fetch sample resumes:', err);
    }
}

function toggleSampleMenu() {
    const menu = document.getElementById('sample-menu');
    if (menu) menu.classList.toggle('show');
}

// Close sample dropdown on outside click
document.addEventListener('click', (e) => {
    const sampleDropdown = document.querySelector('.sample-loader-dropdown');
    if (sampleDropdown && !sampleDropdown.contains(e.target)) {
        const menu = document.getElementById('sample-menu');
        if (menu) menu.classList.remove('show');
    }
});

function loadSampleResume(key) {
    const sample = window.AppState.sampleResumes ? window.AppState.sampleResumes[key] : null;
    if (!sample) {
        showToast('Loading sample profile...', 'info');
        return;
    }

    // Create a virtual PDF blob file from sample content
    const blob = new Blob([sample.content], { type: 'text/plain' });
    const sampleFile = new File([blob], `${sample.title.replace(/[^a-zA-Z0-9]/g, '_')}_Resume.pdf`, { type: 'application/pdf' });
    
    // Assign to selected file in resume_analyzer
    if (typeof handleFile === 'function') {
        handleFile(sampleFile);
    }
    window.AppState.selectedSampleText = sample.content;

    const menu = document.getElementById('sample-menu');
    if (menu) menu.classList.remove('show');

    showToast(`Loaded sample PDF profile: ${sample.title}`, 'success');
}

/* ==========================================================================
   HERO INTERACTIVE DARK ELEMENTS - ULTRA-SMOOTH MOUSE CURSOR PARALLAX
   ========================================================================== */
function initHeroDarkElementsParallax() {
    const heroes = document.querySelectorAll('.analyzer-hero, .saas-hero');
    if (!heroes.length) return;

    heroes.forEach(hero => {
        const layer = hero.querySelector('.hero-dark-elements-layer');
        if (!layer) return;

        const elements = layer.querySelectorAll('.hero-dark-element');
        const spotlight = layer.querySelector('.hero-dark-spotlight');

        let targetX = 0;
        let targetY = 0;
        let currentX = 0;
        let currentY = 0;

        let targetSpotX = 50;
        let targetSpotY = 50;
        let currentSpotX = 50;
        let currentSpotY = 50;

        let isHovered = false;
        let isLoopRunning = false;

        function onMouseMove(e) {
            const rect = hero.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return;

            // Normalized coordinates (-1 to +1 from hero center)
            const normX = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
            const normY = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

            targetX = Math.max(-1, Math.min(1, normX));
            targetY = Math.max(-1, Math.min(1, normY));

            targetSpotX = ((e.clientX - rect.left) / rect.width) * 100;
            targetSpotY = ((e.clientY - rect.top) / rect.height) * 100;

            isHovered = true;
            if (!isLoopRunning) {
                isLoopRunning = true;
                requestAnimationFrame(updateLoop);
            }
        }

        function onMouseLeave() {
            isHovered = false;
            targetX = 0;
            targetY = 0;
            targetSpotX = 50;
            targetSpotY = 50;
            if (!isLoopRunning) {
                isLoopRunning = true;
                requestAnimationFrame(updateLoop);
            }
        }

        function updateLoop() {
            // Extreme smooth damping factor (0.055 provides silky smooth inertia and glide)
            const ease = 0.055;
            currentX += (targetX - currentX) * ease;
            currentY += (targetY - currentY) * ease;
            currentSpotX += (targetSpotX - currentSpotX) * 0.07;
            currentSpotY += (targetSpotY - currentSpotY) * 0.07;

            // Update each dark element
            elements.forEach(el => {
                const depthX = parseFloat(el.getAttribute('data-depth-x') || 25);
                const depthY = parseFloat(el.getAttribute('data-depth-y') || 25);
                const rot = parseFloat(el.getAttribute('data-rotate') || 0);

                const tx = (currentX * depthX).toFixed(2);
                const ty = (currentY * depthY).toFixed(2);
                const r = rot ? ` rotate(${(currentX * rot).toFixed(2)}deg)` : '';

                el.style.transform = `translate3d(${tx}px, ${ty}px, 0px)${r}`;
            });

            // Update ambient spotlight
            if (spotlight) {
                spotlight.style.background = `radial-gradient(460px circle at ${currentSpotX.toFixed(1)}% ${currentSpotY.toFixed(1)}%, rgba(15, 23, 42, 0.045) 0%, rgba(15, 23, 42, 0.012) 48%, transparent 75%)`;
            }

            // Continue loop if still hovering or still smoothly returning towards rest position
            const diff = Math.abs(targetX - currentX) + Math.abs(targetY - currentY);
            if (isHovered || diff > 0.0008) {
                requestAnimationFrame(updateLoop);
            } else {
                isLoopRunning = false;
            }
        }

        hero.addEventListener('mousemove', onMouseMove, { passive: true });
        hero.addEventListener('mouseleave', onMouseLeave, { passive: true });
    });
}


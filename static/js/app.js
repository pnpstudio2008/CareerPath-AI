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
    initTheme();
    initNavigation();
    fetchSampleResumes();
    initDropZone();

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
   THEME CONFIGURATION (LOCKED IN LIGHT NEUMORPHIC THEME)
   ========================================================================== */
function initTheme() {
    window.AppState.theme = 'light';
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
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
        const data = await res.json();
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

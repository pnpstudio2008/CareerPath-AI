/**
 * AI Career Companion - Advanced Client-Side Security Guard
 * Intellectual Property & Source Code Anti-Inspection Protection
 * 
 * Protects against:
 * - View Page Source (Ctrl+U)
 * - Developer Tools (F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C)
 * - Right-Click Context Menu Inspection
 * - Page Saving & Scraping (Ctrl+S, Drag & Drop)
 * - DevTools Console Tampering & Reverse Engineering
 */

(function () {
    'use strict';

    // Hard Refresh Security Policy State
    let hardRefreshLockoutEnabled = localStorage.getItem('hard_refresh_lockout_enabled') !== 'false';

    // Synchronize policy dynamically from backend
    try {
        fetch('/api/security/policy')
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (data && typeof data.hard_refresh_lockout === 'boolean') {
                    hardRefreshLockoutEnabled = data.hard_refresh_lockout;
                    localStorage.setItem('hard_refresh_lockout_enabled', data.hard_refresh_lockout ? 'true' : 'false');
                }
            })
            .catch(function () {});
    } catch (_) {}

    function isLockoutActive() {
        var localFlag = localStorage.getItem('hard_refresh_lockout') === 'true';
        var sessionFlag = sessionStorage.getItem('hard_refresh_lockout') === 'true';
        var cookieFlag = document.cookie.split(';').some(function (c) {
            return c.trim().startsWith('hard_refresh_lockout=1');
        });
        return localFlag || sessionFlag || cookieFlag;
    }

    var currentPath = (window.location.pathname || '').toLowerCase();
    var isAuthPage = currentPath === '/student/login' || 
                     currentPath === '/login' || 
                     currentPath === '/admin/login' || 
                     currentPath.indexOf('/login') !== -1;

    // IMMEDIATE LOCKOUT ENFORCEMENT: If locked out, prevent accessing the software until login
    if (!isAuthPage && isLockoutActive() && hardRefreshLockoutEnabled) {
        window.location.replace('/student/login?locked=hard_refresh');
        return;
    }

    // Expose unlock helper for login callbacks
    window.PlatformSecurity = {
        unlockSession: function () {
            localStorage.removeItem('hard_refresh_lockout');
            sessionStorage.removeItem('hard_refresh_lockout');
            document.cookie = 'hard_refresh_lockout=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax';
        },
        isLockoutActive: isLockoutActive
    };

    // Last toast notification timestamp to prevent alert flood
    let lastToastTime = 0;

    function showSecurityToast(message) {
        const now = Date.now();
        if (now - lastToastTime < 2500) return;
        lastToastTime = now;

        let container = document.getElementById('security-toast-box');
        if (!container) {
            container = document.createElement('div');
            container.id = 'security-toast-box';
            container.style.cssText = `
                position: fixed;
                bottom: 24px;
                left: 50%;
                transform: translateX(-50%) translateY(20px);
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                color: #FFFFFF;
                border: 1px solid rgba(239, 68, 68, 0.4);
                box-shadow: 0 10px 30px rgba(0,0,0,0.4), 0 0 20px rgba(239, 68, 68, 0.25);
                padding: 12px 24px;
                border-radius: 999px;
                font-family: -apple-system, BlinkMacSystemFont, 'Plus Jakarta Sans', sans-serif;
                font-size: 13px;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 10px;
                z-index: 10000000;
                pointer-events: none;
                opacity: 0;
                transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            `;
            container.innerHTML = `<span style="color:#EF4444; font-size:16px;">🛡️</span> <span id="sec-toast-msg"></span>`;
            document.body.appendChild(container);
        }

        const msgSpan = document.getElementById('sec-toast-msg');
        if (msgSpan) msgSpan.textContent = message;

        // Animate in
        requestAnimationFrame(() => {
            container.style.opacity = '1';
            container.style.transform = 'translateX(-50%) translateY(0)';
        });

        // Animate out
        setTimeout(() => {
            if (container) {
                container.style.opacity = '0';
                container.style.transform = 'translateX(-50%) translateY(15px)';
            }
        }, 2200);
    }

    // 1. DISABLE RIGHT-CLICK CONTEXT MENU (ANTI-INSPECT)
    document.addEventListener('contextmenu', function (e) {
        // Allow right-click ONLY on editable inputs/textareas for pasting
        const tag = (e.target.tagName || '').toLowerCase();
        if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) {
            return true;
        }
        e.preventDefault();
        e.stopPropagation();
        showSecurityToast('Source inspection and context menus are restricted for security.');
        return false;
    }, true);

    // 2. DISABLE DEVELOPER KEYBOARD SHORTCUTS
    document.addEventListener('keydown', function (e) {
        // HARD REFRESH SHORTCUT DETECTION (Ctrl+Shift+R / Cmd+Shift+R / Ctrl+F5 / Shift+F5)
        const ctrlOrMeta = e.ctrlKey || e.metaKey;
        const key = (e.key || '').toUpperCase();
        const isHardRefresh = 
            (ctrlOrMeta && e.shiftKey && (key === 'R' || e.code === 'KeyR')) ||
            ((e.ctrlKey || e.shiftKey) && (key === 'F5' || e.keyCode === 116)) ||
            (ctrlOrMeta && (key === 'F5' || e.keyCode === 116));

        if (isHardRefresh) {
            if (hardRefreshLockoutEnabled) {
                e.preventDefault();
                e.stopPropagation();

                // 1. Mark lockout indicators everywhere
                localStorage.setItem('hard_refresh_lockout', 'true');
                sessionStorage.setItem('hard_refresh_lockout', 'true');
                document.cookie = 'hard_refresh_lockout=1; path=/; max-age=86400; SameSite=Lax';

                // 2. Dispatch server logout beacon
                try {
                    if (navigator.sendBeacon) {
                        navigator.sendBeacon('/api/security/hard-refresh-logout');
                    } else {
                        fetch('/api/security/hard-refresh-logout', { method: 'POST', keepalive: true });
                    }
                } catch (_) {}

                // 3. Clear session storage
                try {
                    sessionStorage.clear();
                } catch (_) {}

                // 4. Alert user and redirect immediately to login portal
                showSecurityToast('Hard refresh (Ctrl+Shift+R) detected. Session locked. Redirecting to login...');
                setTimeout(function () {
                    window.location.replace('/student/login?locked=hard_refresh');
                }, 120);
                return false;
            }
        }

        // F12 key
        if (e.keyCode === 123) {
            e.preventDefault();
            e.stopPropagation();
            showSecurityToast('Developer Tools access is locked by security policy.');
            return false;
        }

        const ctrlOrMeta = e.ctrlKey || e.metaKey;

        // Ctrl + Shift + I (Inspect)
        // Ctrl + Shift + J (Console)
        // Ctrl + Shift + C (Element picker)
        // Ctrl + Shift + K (Firefox console)
        if (ctrlOrMeta && e.shiftKey) {
            const key = (e.key || '').toUpperCase();
            if (key === 'I' || key === 'J' || key === 'C' || key === 'K') {
                e.preventDefault();
                e.stopPropagation();
                showSecurityToast('Developer Tools shortcut is disabled.');
                return false;
            }
        }

        // Ctrl + U (View Source)
        if (ctrlOrMeta && (e.key === 'u' || e.key === 'U')) {
            e.preventDefault();
            e.stopPropagation();
            showSecurityToast('Viewing page source is protected.');
            return false;
        }

        // Ctrl + S (Save Page As)
        if (ctrlOrMeta && (e.key === 's' || e.key === 'S')) {
            e.preventDefault();
            e.stopPropagation();
            showSecurityToast('Saving platform source code is blocked.');
            return false;
        }

        // Ctrl + P (Print Page - except when user clicks explicit print buttons)
        if (ctrlOrMeta && (e.key === 'p' || e.key === 'P')) {
            const isInput = ['input', 'textarea'].includes((e.target.tagName || '').toLowerCase());
            if (!isInput) {
                e.preventDefault();
                e.stopPropagation();
                showSecurityToast('Document export is protected.');
                return false;
            }
        }
    }, true);

    // 3. DISABLE DRAG & DROP FILE/IMAGE SCRAPING
    document.addEventListener('dragstart', function (e) {
        const tag = (e.target.tagName || '').toLowerCase();
        if (tag === 'img' || tag === 'svg' || tag === 'a') {
            e.preventDefault();
            return false;
        }
    }, true);

    // 4. OVERRIDE CONSOLE IN PRODUCTION (HIDE INTERNAL LOGS / CREDENTIALS)
    try {
        const noop = function () {};
        const isLocalDev = window.location.hostname === 'localhost' && window.location.port === '99999'; // disabled in normal runs
        if (!isLocalDev) {
            window.console.log = noop;
            window.console.info = noop;
            window.console.warn = noop;
            window.console.debug = noop;
            window.console.table = noop;
        }
    } catch (_) {}

    // 5. DEVTOOLS OPEN DETECTION & SECURITY BLUR
    let devToolsOpen = false;
    const threshold = 160;

    function checkDevToolsDimensions() {
        const widthDiff = window.outerWidth - window.innerWidth > threshold;
        const heightDiff = window.outerHeight - window.innerHeight > threshold;
        
        // If DevTools is docked
        if (widthDiff || heightDiff) {
            if (!devToolsOpen) {
                devToolsOpen = true;
                handleDevToolsOpen();
            }
        } else {
            if (devToolsOpen) {
                devToolsOpen = false;
                handleDevToolsClosed();
            }
        }
    }

    function handleDevToolsOpen() {
        let shield = document.getElementById('security-tamper-shield');
        if (!shield) {
            shield = document.createElement('div');
            shield.id = 'security-tamper-shield';
            shield.className = 'security-tamper-shield';
            shield.innerHTML = `
                <div style="max-width: 440px; background: #1E293B; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 20px; padding: 2rem; box-shadow: 0 20px 50px rgba(0,0,0,0.6);">
                    <div style="width: 64px; height: 64px; border-radius: 50%; background: rgba(239, 68, 68, 0.15); color: #EF4444; font-size: 2rem; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.25rem;">
                        <i class="fa-solid fa-shield-halved"></i>
                    </div>
                    <h3 style="font-size: 1.2rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.5rem;">Security Shield Active</h3>
                    <p style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 1.25rem;">
                        Source code inspection and developer debugging are locked to prevent intellectual property theft and unauthorized tampering.
                    </p>
                    <p style="font-size: 0.78rem; color: #64748B;">Please close Developer Tools to continue using AI Career Companion.</p>
                </div>
            `;
            document.body.appendChild(shield);
        }
        shield.classList.add('active');
    }

    function handleDevToolsClosed() {
        const shield = document.getElementById('security-tamper-shield');
        if (shield) shield.classList.remove('active');
    }

    // Back-Forward Cache (bfcache) lockout enforcement
    window.addEventListener('pageshow', function (event) {
        if (event.persisted && !isAuthPage && isLockoutActive() && hardRefreshLockoutEnabled) {
            window.location.replace('/student/login?locked=hard_refresh');
        }
    });

    // DevTools docked check disabled to avoid false positives on scaled or zoomed displays
    // Keyboard shortcuts (F12, Ctrl+Shift+I/J/C, Ctrl+U, Ctrl+S) provide strict, non-intrusive protection

    // Initial console banner for curious inspectors
    try {
        const styles = [
            'color: #EF4444',
            'font-size: 18px',
            'font-weight: bold',
            'padding: 8px 12px',
            'background: #1E293B',
            'border-radius: 8px'
        ].join(';');
        console.clear();
    } catch (_) {}

})();

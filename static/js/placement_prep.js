
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
 * AI Career Companion - Placement Preparation & Quizzes (Module 2)
 * Features Best Scorers' Benchmark Challenges (Hall of Fame)
 */

let quizQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};
let quizTimerInterval = null;
let secondsRemaining = 600; // 10 minutes
let activeTopScorer = null; // Track current benchmark senior

// Company Logo Vector Helper (retina-ready SVG)
function getCompanyLogoSvg(company) {
    const comp = (company || '').toLowerCase();
    if (comp.includes('google')) {
        return `<svg viewBox="0 0 48 48" width="32" height="32">
            <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
            <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
            <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
            <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
        </svg>`;
    }
    if (comp.includes('amazon')) {
        return `<svg viewBox="0 0 48 48" width="34" height="34">
            <path fill="#111827" d="M22.5 14.2c-5.2 0-9.4 3.1-9.4 8.2 0 4.2 2.7 6.8 6.5 6.8 3.3 0 5.8-1.8 7.1-3.7v3.2h4.5V14.7h-4.5v2.8c-1.3-2-3.8-3.3-6.2-3.3zm2.5 9.8c-.8 1.8-2.6 3.1-4.7 3.1-2.6 0-4.3-1.8-4.3-4.5 0-3.1 2-4.9 4.8-4.9 2 0 3.6 1.1 4.2 2.7v3.6z"/>
            <path fill="#FF9900" d="M37.5 33.2c-7.8 5.7-19.1 7.2-28.5 2.5-.4-.2-.5-.7-.1-1 .3-.3.8-.3 1.2-.1 8.7 4.3 19.1 2.9 26.4-2.3.5-.4 1.1.2 1 1z"/>
            <path fill="#FF9900" d="M38.8 30.8c-.4-.5-2.6-.2-3.9.1-.4.1-.4-.3-.1-.5 1.8-1.3 4.8-1 5.3-.4.5.6-.2 3.6-1.9 5.1-.3.3-.6.1-.5-.2.4-1.2 1.5-3.6 1.1-4.1z"/>
        </svg>`;
    }
    if (comp.includes('general') || comp.includes('ge')) {
        return `<svg viewBox="0 0 48 48" width="36" height="36">
            <circle cx="24" cy="24" r="22" fill="#005EB8"/>
            <circle cx="24" cy="24" r="20" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.8"/>
            <text x="24" y="30" font-family="'Brush Script MT', 'Segoe Script', cursive, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF" text-anchor="middle" font-style="italic">GE</text>
        </svg>`;
    }
    if (comp.includes('microsoft')) {
        return `<svg viewBox="0 0 48 48" width="30" height="30">
            <rect x="7" y="7" width="15" height="15" fill="#F25022"/>
            <rect x="26" y="7" width="15" height="15" fill="#7FBA00"/>
            <rect x="7" y="26" width="15" height="15" fill="#00A4EF"/>
            <rect x="26" y="26" width="15" height="15" fill="#FFB900"/>
        </svg>`;
    }
    if (comp.includes('tcs')) {
        return `<svg viewBox="0 0 60 48" width="42" height="34">
            <text x="30" y="32" font-family="'Inter', 'Helvetica Neue', Arial, sans-serif" font-size="25" font-weight="900" fill="#E61C24" text-anchor="middle" letter-spacing="-1">tcs</text>
        </svg>`;
    }
    if (comp.includes('infosys')) {
        return `<svg viewBox="0 0 66 48" width="48" height="32">
            <text x="33" y="30" font-family="'Trebuchet MS', Arial, sans-serif" font-size="19" font-weight="800" fill="#007CC3" text-anchor="middle" letter-spacing="-0.5">Infosys</text>
        </svg>`;
    }
    if (comp.includes('accenture')) {
        return `<svg viewBox="0 0 54 48" width="36" height="32">
            <path d="M14 30L27 16L40 30" fill="none" stroke="#A100FF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>`;
    }
    if (comp.includes('wipro')) {
        return `<svg viewBox="0 0 48 48" width="32" height="32">
            <circle cx="17" cy="17" r="6" fill="#F48024"/>
            <circle cx="31" cy="17" r="6" fill="#3AA655"/>
            <circle cx="17" cy="31" r="6" fill="#994D99"/>
            <circle cx="31" cy="31" r="6" fill="#0072CE"/>
            <circle cx="24" cy="24" r="3" fill="#FFFFFF"/>
        </svg>`;
    }
    return `<div class="generic-company-icon" style="color:#2563EB; font-size:1.4rem;"><i class="fa-solid fa-building"></i></div>`;
}

// ==========================================
// BEST SCORERS' HALL OF FAME BENCHMARK DATA
// ==========================================
const TOP_SCORERS = [
    {
        id: 'priya',
        name: 'Priya Patel',
        designation: 'SDE-1 at Google',
        company: 'Google',
        ctc: '₹35.00 LPA',
        batch: 'Batch of 2024',
        subject: 'all',
        companyFilter: 'Google',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '3m 48s',
        testTitle: "Google High-Bar Systems & Logic Challenge",
        avatarIcon: 'fa-user-graduate',
        goldenTip: 'Clarify all edge cases, state transitions in DP, and test with empty/boundary inputs.',
        tags: ['Algorithms', 'OS Internals', 'Networks', 'Graphs']
    },
    {
        id: 'aarav',
        name: 'Aarav Sharma',
        designation: 'SDE-1 at Amazon',
        company: 'Amazon',
        ctc: '₹28.50 LPA',
        batch: 'Batch of 2024',
        subject: 'DSA',
        companyFilter: 'Amazon',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 12s',
        testTitle: "Amazon SDE-I Elite Algorithm Challenge",
        avatarIcon: 'fa-robot',
        goldenTip: 'Always think about memory constraints & worst-case time complexity before locking answers!',
        tags: ['Trees', 'Graphs', 'DP', 'System Design']
    },
    {
        id: 'karan',
        name: 'Karan Mehta',
        designation: 'Senior Software Engineer at General Electric',
        company: 'General',
        ctc: '₹14.00 LPA',
        batch: 'Batch of 2023',
        subject: 'Python',
        companyFilter: 'General',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 45s',
        testTitle: "General Engineering Architecture & Code Test",
        avatarIcon: 'fa-code',
        goldenTip: 'Focus on clean architecture, OOP principles, and test-driven code execution.',
        tags: ['Architecture', 'Python', 'System Design', 'Testing']
    },
    {
        id: 'sneha',
        name: 'Sneha Kulkarni',
        designation: 'Software Engineer at Microsoft',
        company: 'Microsoft',
        ctc: '₹32.00 LPA',
        batch: 'Batch of 2024',
        subject: 'Operating Systems',
        companyFilter: 'Microsoft',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 18s',
        testTitle: "Microsoft Systems & Cloud Infrastructure Test",
        avatarIcon: 'fa-microchip',
        goldenTip: 'Master OS concurrency, virtual memory paging, and cloud microservices.',
        tags: ['Operating Systems', 'Cloud', 'Distributed Systems', 'C++']
    },
    {
        id: 'rohan',
        name: 'Rohan Deshmukh',
        designation: 'TCS Digital Developer at TCS',
        company: 'TCS',
        ctc: '₹9.00 LPA',
        batch: 'Batch of 2023',
        subject: 'Python',
        companyFilter: 'TCS',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 30s',
        testTitle: "TCS Digital & Advanced Aptitude Challenge",
        avatarIcon: 'fa-code',
        goldenTip: 'Speed is critical for TCS Digital. Practice quick pseudocode interpretation and aptitude formulas.',
        tags: ['Python', 'Aptitude', 'Cloud', 'SQL']
    },
    {
        id: 'ananya',
        name: 'Ananya Joshi',
        designation: 'Specialist Programmer (SP) at Infosys',
        company: 'Infosys',
        ctc: '₹10.50 LPA',
        batch: 'Batch of 2024',
        subject: 'Java',
        companyFilter: 'Infosys',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '5m 04s',
        testTitle: "Infosys SP & OOP Architecture Benchmark",
        avatarIcon: 'fa-laptop-code',
        goldenTip: 'Master Java collection internals, JVM memory model, and SQL join indexes.',
        tags: ['Java OOP', 'DBMS', 'Collections', 'Logic']
    }
];

// Placement Practice Initialization
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('top-scorers-grid')) {
        fetchAndRenderLiveTopScorers();
    }
    loadMainAlumniPracticeQuestions();
});

async function fetchAndRenderLiveTopScorers() {
    try {
        const res = await fetch('/api/alumni/experiences');
        const data = await safeJsonFetch(res);
        if (data.experiences && data.experiences.length > 0) {
            // Update or enrich benchmark challenges with live DB data while preserving the curated priority order
            data.experiences.forEach(exp => {
                const existing = TOP_SCORERS.find(s => s.name.toLowerCase() === (exp.student_name || '').toLowerCase());
                if (existing) {
                    if (exp.role) {
                        let cleanRole = exp.role;
                        cleanRole = cleanRole.replace(/Software Development Engineer\s*\((SDE-?[1I])\)/i, '$1');
                        cleanRole = cleanRole.replace(/Software Development Engineer/i, 'SDE');
                        cleanRole = cleanRole.replace(/Senior Software Engineer/i, 'Senior Software Engineer');
                        existing.designation = (cleanRole + ' at ' + (exp.company || '')).trim();
                    }
                    if (exp.company) existing.company = exp.company;
                    if (exp.package_lpa) existing.ctc = `₹${parseFloat(exp.package_lpa).toFixed(2)} LPA`;
                    if (exp.advice_to_juniors || exp.preparation_tips) {
                        existing.goldenTip = exp.advice_to_juniors || exp.preparation_tips;
                    }
                }
            });
        }
    } catch (e) {
        console.log('Using default benchmark challenges:', e);
    }
    renderTopScorerCards();
    syncTopScorerDropdown();
}

function syncTopScorerDropdown() {
    const select = document.getElementById('quiz-top-scorer-select');
    if (!select) return;
    select.innerHTML = '<option value="">-- Choose an Alumni / Benchmark Challenge --</option>';
    TOP_SCORERS.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = `${s.name} (${s.company} ${s.ctc} - ${s.score})`;
        select.appendChild(opt);
    });
}

function renderTopScorerCards(records = TOP_SCORERS) {
    const grid = document.getElementById('top-scorers-grid');
    if (!grid) return;

    grid.innerHTML = '';
    records.forEach((scorer, idx) => {
        const row = document.createElement('div');
        row.className = 'scorer-row';
        row.onclick = () => startTopScorerChallenge(scorer.id);

        // Format CTC cleanly (e.g. ₹35.00 LPA)
        let formattedCtc = scorer.ctc || '';
        const numMatch = String(formattedCtc).match(/[\d.]+/);
        if (numMatch) {
            const numVal = parseFloat(numMatch[0]);
            if (!isNaN(numVal)) {
                formattedCtc = `₹${numVal.toFixed(2)} LPA`;
            }
        }

        // Clean role / designation to match concise mockup titles
        let displayRole = scorer.designation || '';
        displayRole = displayRole.replace(/Software Development Engineer\s*\((SDE-?[1I])\)/i, '$1');
        displayRole = displayRole.replace(/Software Development Engineer/i, 'SDE');
        displayRole = displayRole.replace(/Senior Software Engineer at General/i, 'Senior Software Engineer at GE');
        if (scorer.company && !displayRole.toLowerCase().includes(scorer.company.toLowerCase()) && !displayRole.toLowerCase().includes('ge')) {
            displayRole = `${displayRole} at ${scorer.company}`;
        }

        const rankNum = idx + 1;
        let rankBadgeHtml = '';
        if (rankNum === 1) {
            rankBadgeHtml = `
                <div class="scorer-rank-wrap rank-1">
                    <span class="rank-crown"><i class="fa-solid fa-crown"></i></span>
                    <span class="rank-num">1</span>
                </div>
            `;
        } else if (rankNum === 2) {
            rankBadgeHtml = `
                <div class="scorer-rank-wrap rank-2">
                    <span class="rank-num">2</span>
                </div>
            `;
        } else if (rankNum === 3) {
            rankBadgeHtml = `
                <div class="scorer-rank-wrap rank-3">
                    <span class="rank-num">3</span>
                </div>
            `;
        } else {
            rankBadgeHtml = `
                <div class="scorer-rank-wrap rank-other">
                    <span class="rank-num">${rankNum}</span>
                </div>
            `;
        }

        row.innerHTML = `
            <!-- Desktop Layout Elements (min-width: 992px) -->
            <div class="scorer-rank-col desktop-only">
                ${rankBadgeHtml}
            </div>
            <div class="scorer-logo-card desktop-only">
                ${getCompanyLogoSvg(scorer.company)}
            </div>

            <!-- Mobile Layout Elements: Trophy Circle (max-width: 991px) -->
            <div class="scorer-badge-col mobile-only">
                <div class="scorer-trophy-circle">
                    <i class="fa-solid fa-trophy"></i>
                    <span class="scorer-floating-crown"><i class="fa-solid fa-crown"></i></span>
                </div>
            </div>

            <!-- Content Column -->
            <div class="scorer-info-card">
                <h4 class="scorer-name">${scorer.name}</h4>
                <div class="scorer-role">${displayRole}</div>
                <div class="scorer-bottom-row">
                    <span class="scorer-package">${formattedCtc}</span>
                    <button type="button" class="scorer-btn-solve mobile-only" onclick="event.stopPropagation(); startTopScorerChallenge('${scorer.id}')">
                        <i class="fa-solid fa-play"></i> Solve Test
                    </button>
                </div>
            </div>

            <!-- Desktop Arrow Button (min-width: 992px) -->
            <div class="scorer-arrow-col desktop-only">
                <button type="button" class="scorer-arrow-btn" aria-label="Solve Test">
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        `;

        grid.appendChild(row);
    });
}

window.filterScorersTimeRange = function(range, btn) {
    document.querySelectorAll('.tsh-tab-pill').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    
    let filtered = [...TOP_SCORERS];
    if (range === 'month') {
        filtered = TOP_SCORERS.slice(0, 4);
    } else if (range === 'semester') {
        filtered = TOP_SCORERS.slice(0, 6);
    }
    renderTopScorerCards(filtered);
};

// ==========================================
// START SPECIFIC TOP SCORER CHALLENGE
// ==========================================
function startTopScorerChallenge(scorerId) {
    const scorer = TOP_SCORERS.find(s => s.id === scorerId) || TOP_SCORERS[0];
    activeTopScorer = scorer;

    // Sync dropdowns
    const subSelect = document.getElementById('quiz-subject-select');
    const compSelect = document.getElementById('quiz-company-select');
    const topSelect = document.getElementById('quiz-top-scorer-select');

    if (subSelect) subSelect.value = scorer.subject;
    if (compSelect) compSelect.value = scorer.companyFilter;
    if (topSelect) topSelect.value = scorer.id;

    startNewQuiz(scorer);
}

function loadTopScorerChallengeFromDropdown() {
    const select = document.getElementById('quiz-top-scorer-select');
    const scorerId = select.value;
    if (scorerId) {
        startTopScorerChallenge(scorerId);
    } else {
        activeTopScorer = null;
        startNewQuiz();
    }
}

// ==========================================
// QUIZ ENGINE FUNCTIONS
// ==========================================

async function startNewQuiz(presetScorer = null) {
    const subject = document.getElementById('quiz-subject-select')?.value || 'all';
    const company = document.getElementById('quiz-company-select')?.value || 'all';
    const difficulty = document.getElementById('quiz-difficulty-select')?.value || 'all';
    const count = parseInt(document.getElementById('quiz-count-select')?.value || '10');

    try {
        let apiUrl = `/api/quiz/questions?subject=${encodeURIComponent(subject)}&company=${encodeURIComponent(company)}&difficulty=${encodeURIComponent(difficulty)}&limit=${count}`;
        const res = await fetch(apiUrl);
        const data = await safeJsonFetch(res);

        if (!data.success || !data.questions || data.questions.length === 0) {
            showToast('No practice questions found matching your filter criteria. Try broader filters.', 'info');
            return;
        }

        quizQuestions = data.questions;
        currentQuestionIndex = 0;
        userAnswers = {};
        secondsRemaining = quizQuestions.length * 60;

        const idlePrompt = document.getElementById('quiz-idle-prompt');
        if (idlePrompt) idlePrompt.style.display = 'none';

        document.getElementById('quiz-active-wrapper').style.display = 'block';
        document.getElementById('quiz-results-wrapper').style.display = 'none';

        const totalCntEl = document.getElementById('quiz-total-count');
        if (totalCntEl) totalCntEl.innerText = quizQuestions.length;

        // Hide alumni benchmark banner if present on practice page
        const banner = document.getElementById('quiz-scorer-banner');
        if (banner) banner.style.display = 'none';

        initQuizTimer();
        renderQuizIndicators();
        renderCurrentQuestion();
        showToast(`🎯 Practice Assessment Started: ${quizQuestions.length} Questions (${Math.round(secondsRemaining/60)} Mins)`, 'success');

        // Smooth scroll to quiz interface
        document.getElementById('quiz-active-wrapper').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
        showToast('Error loading practice questions: ' + err.message, 'error');
    }
}

function renderScorerLiveBanner(scorer) {
    if (!scorer) scorer = TOP_SCORERS[0];

    const nameEl = document.getElementById('scorer-banner-name');
    const desigEl = document.getElementById('scorer-banner-designation');
    const scoreEl = document.getElementById('scorer-banner-score');
    const timeEl = document.getElementById('scorer-banner-time');
    const quoteEl = document.getElementById('scorer-banner-quote');

    if (nameEl) nameEl.innerText = scorer.name;
    if (desigEl) desigEl.innerText = `${scorer.designation} (${scorer.ctc})`;
    if (scoreEl) scoreEl.innerText = `${scorer.score} (${scorer.scoreFraction})`;
    if (timeEl) timeEl.innerText = scorer.timeTaken;
    if (quoteEl) quoteEl.innerText = scorer.goldenTip;
}

function reloadQuiz() {
    startNewQuiz();
}

function initQuizTimer() {
    if (quizTimerInterval) clearInterval(quizTimerInterval);

    const timerEl = document.getElementById('quiz-timer-text');
    quizTimerInterval = setInterval(() => {
        secondsRemaining--;
        if (secondsRemaining <= 0) {
            clearInterval(quizTimerInterval);
            showToast('Time is up! Submitting quiz answers...', 'info');
            submitQuizAnswers();
            return;
        }

        const mins = Math.floor(secondsRemaining / 60);
        const secs = secondsRemaining % 60;
        timerEl.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }, 1000);
}

function renderQuizIndicators() {
    const wrap = document.getElementById('quiz-indicator-pills');
    wrap.innerHTML = '';

    quizQuestions.forEach((q, idx) => {
        const pill = document.createElement('div');
        pill.className = `quiz-pill-indicator ${idx === currentQuestionIndex ? 'active' : ''} ${userAnswers[q.id] ? 'answered' : ''}`;
        pill.innerText = idx + 1;
        pill.onclick = () => jumpToQuestion(idx);
        wrap.appendChild(pill);
    });
}

function renderCurrentQuestion() {
    if (quizQuestions.length === 0) return;

    const q = quizQuestions[currentQuestionIndex];
    document.getElementById('quiz-current-idx').innerText = currentQuestionIndex + 1;
    document.getElementById('quiz-total-count').innerText = quizQuestions.length;
    document.getElementById('quiz-topic-badge').innerText = `${q.subject} (${q.difficulty})`;
    document.getElementById('quiz-question-text').innerText = q.question;

    // Render 4 Options
    const optionsContainer = document.getElementById('quiz-options-container');
    optionsContainer.innerHTML = '';

    const options = [
        { key: 'A', text: q.option_a },
        { key: 'B', text: q.option_b },
        { key: 'C', text: q.option_c },
        { key: 'D', text: q.option_d }
    ];

    options.forEach(opt => {
        const btn = document.createElement('button');
        const isSelected = userAnswers[q.id] === opt.key;
        btn.className = `quiz-option-btn ${isSelected ? 'selected' : ''}`;
        btn.innerHTML = `<span class="option-prefix">${opt.key}</span> <span>${opt.text}</span>`;
        btn.onclick = () => selectOption(q.id, opt.key);
        optionsContainer.appendChild(btn);
    });

    // Update Nav buttons
    document.getElementById('quiz-btn-prev').disabled = (currentQuestionIndex === 0);

    const isLast = (currentQuestionIndex === quizQuestions.length - 1);
    document.getElementById('quiz-btn-next').style.display = isLast ? 'none' : 'inline-flex';
    document.getElementById('quiz-btn-submit').style.display = isLast ? 'inline-flex' : 'none';

    renderQuizIndicators();
}

function selectOption(questionId, optionKey) {
    userAnswers[questionId] = optionKey;
    renderCurrentQuestion();
}

function prevQuizQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderCurrentQuestion();
    }
}

function nextQuizQuestion() {
    if (currentQuestionIndex < quizQuestions.length - 1) {
        currentQuestionIndex++;
        renderCurrentQuestion();
    }
}

function jumpToQuestion(idx) {
    currentQuestionIndex = idx;
    renderCurrentQuestion();
}

async function submitQuizAnswers() {
    if (quizTimerInterval) clearInterval(quizTimerInterval);

    // Check if any answers selected
    const totalAnswered = Object.keys(userAnswers).length;
    if (totalAnswered === 0) {
        showToast('Please answer at least one question before submitting.', 'error');
        return;
    }

    try {
        const response = await fetch('/api/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: userAnswers })
        });

        const data = await safeJsonFetch(response);
        if (!response.ok || !data.success) {
            showToast(data.error || 'Failed to submit quiz.', 'error');
            return;
        }

        renderQuizResults(data);
        showToast(`Quiz completed! Score: ${data.score_percentage}%`, 'success');

    } catch (err) {
        showToast('Error submitting quiz: ' + err.message, 'error');
    }
}

function renderQuizResults(data) {
    document.getElementById('quiz-active-wrapper').style.display = 'none';
    const resultsWrapper = document.getElementById('quiz-results-wrapper');
    resultsWrapper.style.display = 'block';

    document.getElementById('quiz-result-score-pct').innerText = `${data.score_percentage}%`;
    document.getElementById('quiz-result-fraction').innerText = `${data.correct_count} / ${data.total_questions} Correct`;

    let headline = 'Great Effort!';
    if (data.score_percentage >= 80) headline = '🏆 Outstanding Placement Readiness!';
    else if (data.score_percentage >= 60) headline = '👍 Good Performance - Polish Minor Gaps';
    else headline = '📚 Needs Focused Preparation';
    document.getElementById('quiz-result-headline').innerText = headline;

    // Benchmark Comparison Update
    const scorer = activeTopScorer || TOP_SCORERS[0];
    const compareTitle = document.getElementById('benchmark-compare-title');
    const compareDesc = document.getElementById('benchmark-compare-desc');

    if (compareTitle && compareDesc) {
        if (data.score_percentage === 100) {
            compareTitle.innerHTML = `<span class="text-success"><i class="fa-solid fa-crown text-amber"></i> Perfect Match! You Tied the Hall of Fame Record!</span>`;
            compareDesc.innerHTML = `Incredible performance! You achieved a 100% score, matching the benchmark record set by <strong>${scorer.name}</strong> (${scorer.designation}). You are fully placement ready!`;
        } else if (data.score_percentage >= 80) {
            compareTitle.innerHTML = `<span><i class="fa-solid fa-medal text-amber"></i> High Performance Tier vs ${scorer.name}</span>`;
            compareDesc.innerHTML = `You scored <strong>${data.score_percentage}%</strong>! You are just a few points away from ${scorer.name}'s perfect 100% record (${scorer.designation}). Review the explanations below to master the edge cases.`;
        } else {
            compareTitle.innerHTML = `<span><i class="fa-solid fa-bullseye text-primary"></i> Benchmark Target: ${scorer.name} (100%)</span>`;
            compareDesc.innerHTML = `Your score: <strong>${data.score_percentage}%</strong>. Previous record by <strong>${scorer.name}</strong> (${scorer.designation}) is <strong>100%</strong> in ${scorer.timeTaken}. Practice the weak areas identified below!`;
        }
    }

    // Topic breakdown
    const topicContainer = document.getElementById('quiz-topic-breakdown-list');
    topicContainer.innerHTML = '';
    for (const [topic, stat] of Object.entries(data.topic_breakdown)) {
        const pct = Math.round((stat.correct / stat.total) * 100);
        const row = document.createElement('div');
        row.className = 'topic-bar-row';
        row.innerHTML = `
            <div class="card-header-flex" style="margin-bottom:0.25rem;">
                <strong>${topic}</strong>
                <span>${stat.correct}/${stat.total} (${pct}%)</span>
            </div>
            <div class="progress-bar-bg" style="margin:0;">
                <div class="progress-bar-fill" style="width: ${pct}%;"></div>
            </div>
        `;
        topicContainer.appendChild(row);
    }

    // Detailed Review Accordion
    const reviewList = document.getElementById('quiz-review-list');
    reviewList.innerHTML = '';
    data.detailed_results.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = `quiz-review-card ${item.is_correct ? 'correct' : 'incorrect'}`;
        card.innerHTML = `
            <div class="card-header-flex">
                <span class="badge ${item.is_correct ? 'badge-success' : 'badge-danger'}">
                    ${item.is_correct ? '<i class="fa-solid fa-check"></i> Correct' : '<i class="fa-solid fa-xmark"></i> Incorrect'}
                </span>
                <span class="badge badge-outline">${item.subject}</span>
            </div>
            <h4 class="mt-2">Q${idx + 1}. ${item.question}</h4>
            <div class="mt-2" style="font-size:0.88rem;">
                <div><strong>Your Answer:</strong> Option ${item.user_option || 'None'} - ${item.options[item.user_option] || 'Unanswered'}</div>
                <div class="text-success"><strong>Correct Answer:</strong> Option ${item.correct_option} - ${item.options[item.correct_option]}</div>
            </div>
            <div class="mt-2 p-2" style="background:var(--bg-surface); border-radius:var(--radius-sm); font-size:0.86rem; color:var(--text-secondary);">
                <strong><i class="fa-solid fa-lightbulb text-amber"></i> Explanation:</strong> ${item.explanation}
            </div>
        `;
        reviewList.appendChild(card);
    });

    resultsWrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/* ==========================================================================
   ALUMNI CONTRIBUTED PRACTICE TEST QUESTIONS SECTION (PRACTICE PAGE)
   ========================================================================== */
let mainAlumniQuestionsData = [];
let mainPrepAnsweredCount = 0;
let mainPrepCorrectCount = 0;

async function loadMainAlumniPracticeQuestions() {
    const skill = document.getElementById('main-prep-filter-skill')?.value || 'all';
    const company = document.getElementById('main-prep-filter-company')?.value || 'all';
    const difficulty = document.getElementById('main-prep-filter-difficulty')?.value || 'all';
    const alumni = document.getElementById('main-prep-filter-alumni')?.value || 'all';

    const container = document.getElementById('main-alumni-questions-list');
    if (!container) return;

    container.innerHTML = '<div class="text-center p-4 text-muted"><div class="spinner"></div> Loading placement questions contributed by alumni mentors...</div>';

    try {
        const params = new URLSearchParams({ subject: skill, company: company, difficulty: difficulty, alumni: alumni, limit: 25 });
        const res = await fetch(`/api/student/alumni-questions?${params.toString()}`);
        const data = await safeJsonFetch(res);

        if (data.alumni_list && data.alumni_list.length > 0) {
            updateMainAlumniFilterOptions(data.alumni_list);
        }

        if (!data.success || !data.questions || data.questions.length === 0) {
            container.innerHTML = `
                <div class="text-center p-5 text-muted">
                    <i class="fa-solid fa-folder-open fa-2x mb-2 text-muted"></i>
                    <p style="font-weight:600;">No alumni-contributed questions found for the selected filter criteria.</p>
                    <button class="btn btn-outline btn-sm mt-2" onclick="resetMainAlumniPracticeFilters()">
                        <i class="fa-solid fa-rotate-left"></i> Reset Filters
                    </button>
                </div>
            `;
            if (document.getElementById('main-prep-q-total')) document.getElementById('main-prep-q-total').textContent = '0';
            return;
        }

        mainAlumniQuestionsData = data.questions;
        if (document.getElementById('main-prep-q-total')) document.getElementById('main-prep-q-total').textContent = mainAlumniQuestionsData.length;
        renderMainAlumniPracticeQuestions(mainAlumniQuestionsData);
    } catch (err) {
        container.innerHTML = `<div class="text-center p-4 text-danger">Error loading questions: ${err.message}</div>`;
    }
}

function updateMainAlumniFilterOptions(alumniList) {
    const sel = document.getElementById('main-prep-filter-alumni');
    if (!sel || !alumniList) return;
    const currentVal = sel.value || 'all';

    // Only update if options list changed to avoid unnecessary re-rendering
    const optionsHtml = ['<option value="all">🌟 All Alumni Mentors</option>'];
    alumniList.forEach(item => {
        const compBadge = item.company && item.company !== 'General' ? ` (${item.company})` : '';
        optionsHtml.push(`<option value="${item.name}">🎓 ${item.name}${compBadge}</option>`);
    });

    const newHtml = optionsHtml.join('');
    if (sel.innerHTML !== newHtml) {
        sel.innerHTML = newHtml;
        sel.value = currentVal;
        if (sel.selectedIndex === -1) {
            sel.value = 'all';
        }
    }
}

function renderMainAlumniPracticeQuestions(questions) {
    const container = document.getElementById('main-alumni-questions-list');
    if (!container) return;

    container.innerHTML = '';
    questions.forEach((q, idx) => {
        const card = document.createElement('div');
        card.className = 'question-card';
        card.id = `main-alumni-q-${q.id}`;

        const diffClass = q.difficulty === 'Easy' ? 'badge-success' : (q.difficulty === 'Hard' ? 'badge-danger' : 'badge-warning');

        card.innerHTML = `
            <div class="question-meta-row">
                <div class="question-meta-left">
                    <span class="alumni-badge">
                        <i class="fa-solid fa-user-graduate"></i> Contributed by ${escapePrepText(q.alumni_name)}
                    </span>
                    <span class="badge badge-primary">${escapePrepText(q.subject || 'Core CS')}</span>
                    <span class="badge badge-outline"><i class="fa-solid fa-building"></i> ${escapePrepText(q.company || 'Tech')}</span>
                </div>
                <span class="badge ${diffClass}">${escapePrepText(q.difficulty || 'Medium')}</span>
            </div>

            <div class="question-title">
                <span style="color:var(--primary); margin-right:6px;">Q${idx + 1}.</span> ${escapePrepText(q.question)}
            </div>

            <div class="options-grid" id="main-prep-options-grid-${q.id}">
                <button type="button" class="option-btn" onclick="checkMainAlumniPracticeOption(${q.id}, 'A', '${q.correct_option}')" id="main-opt-${q.id}-A">
                    <span class="option-letter">A</span>
                    <span>${escapePrepText(q.option_a)}</span>
                </button>
                <button type="button" class="option-btn" onclick="checkMainAlumniPracticeOption(${q.id}, 'B', '${q.correct_option}')" id="main-opt-${q.id}-B">
                    <span class="option-letter">B</span>
                    <span>${escapePrepText(q.option_b)}</span>
                </button>
                <button type="button" class="option-btn" onclick="checkMainAlumniPracticeOption(${q.id}, 'C', '${q.correct_option}')" id="main-opt-${q.id}-C">
                    <span class="option-letter">C</span>
                    <span>${escapePrepText(q.option_c || 'N/A')}</span>
                </button>
                <button type="button" class="option-btn" onclick="checkMainAlumniPracticeOption(${q.id}, 'D', '${q.correct_option}')" id="main-opt-${q.id}-D">
                    <span class="option-letter">D</span>
                    <span>${escapePrepText(q.option_d || 'N/A')}</span>
                </button>
            </div>

            <div class="question-explanation-box" id="main-prep-explanation-${q.id}">
                <div style="font-weight:700; color:var(--text-primary); margin-bottom:4px;">
                    <i class="fa-solid fa-lightbulb text-warning"></i> Mentor Solution & Explanation:
                </div>
                <div>${escapePrepText(q.explanation || 'The correct option is ' + q.correct_option + '. Review core fundamentals for this topic.')}</div>
            </div>
        `;
        container.appendChild(card);
    });
}

function checkMainAlumniPracticeOption(questionId, selectedOpt, correctOpt) {
    const grid = document.getElementById(`main-prep-options-grid-${questionId}`);
    if (!grid) return;

    // Disable all option buttons for this question
    const buttons = grid.querySelectorAll('.option-btn');
    buttons.forEach(btn => btn.disabled = true);

    const selectedBtn = document.getElementById(`main-opt-${questionId}-${selectedOpt}`);
    const correctBtn = document.getElementById(`main-opt-${questionId}-${correctOpt}`);

    mainPrepAnsweredCount++;
    if (selectedOpt === correctOpt) {
        mainPrepCorrectCount++;
        if (selectedBtn) selectedBtn.classList.add('option-correct');
        if (typeof showToast === 'function') showToast('Correct answer! Well done! 🎉', 'success');
    } else {
        if (selectedBtn) selectedBtn.classList.add('option-incorrect');
        if (correctBtn) correctBtn.classList.add('option-correct');
        if (typeof showToast === 'function') showToast(`Incorrect. Correct answer is Option ${correctOpt}.`, 'info');
    }

    if (document.getElementById('main-prep-q-answered')) document.getElementById('main-prep-q-answered').textContent = mainPrepAnsweredCount;
    if (document.getElementById('main-prep-q-correct')) document.getElementById('main-prep-q-correct').textContent = mainPrepCorrectCount;

    // Reveal explanation
    const explBox = document.getElementById(`main-prep-explanation-${questionId}`);
    if (explBox) explBox.classList.add('show');
}

function shuffleMainAlumniPracticeQuestions() {
    if (!mainAlumniQuestionsData || mainAlumniQuestionsData.length === 0) {
        loadMainAlumniPracticeQuestions();
        return;
    }
    const shuffled = [...mainAlumniQuestionsData].sort(() => Math.random() - 0.5);
    renderMainAlumniPracticeQuestions(shuffled);
    if (typeof showToast === 'function') showToast('Questions shuffled!', 'info');
}

function resetMainAlumniPracticeFilters() {
    if (document.getElementById('main-prep-filter-skill')) document.getElementById('main-prep-filter-skill').value = 'all';
    if (document.getElementById('main-prep-filter-company')) document.getElementById('main-prep-filter-company').value = 'all';
    if (document.getElementById('main-prep-filter-difficulty')) document.getElementById('main-prep-filter-difficulty').value = 'all';
    if (document.getElementById('main-prep-filter-alumni')) document.getElementById('main-prep-filter-alumni').value = 'all';
    loadMainAlumniPracticeQuestions();
}

function escapePrepText(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

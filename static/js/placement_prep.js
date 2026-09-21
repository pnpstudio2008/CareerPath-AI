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

// ==========================================
// BEST SCORERS' HALL OF FAME BENCHMARK DATA
// ==========================================
const TOP_SCORERS = [
    {
        id: 'aarav',
        name: 'Aarav Sharma',
        designation: 'Software Development Engineer (SDE-1) at Amazon',
        company: 'Amazon',
        ctc: '₹44.5 LPA',
        batch: 'Batch of 2024',
        subject: 'DSA',
        companyFilter: 'Amazon',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 12s',
        testTitle: "Amazon SDE-1 Elite Algorithm Challenge",
        avatarIcon: 'fa-robot',
        goldenTip: 'Always think about memory constraints & worst-case time complexity before locking answers!',
        tags: ['Trees', 'Graphs', 'DP', 'System Design']
    },
    {
        id: 'sneha',
        name: 'Sneha Kulkarni',
        designation: 'Software Engineer (SWE) at Google',
        company: 'Google',
        ctc: '₹55.0 LPA',
        batch: 'Batch of 2024',
        subject: 'all',
        companyFilter: 'Google',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '3m 48s',
        testTitle: "Google High-Bar Systems & Logic Challenge",
        avatarIcon: 'fa-microchip',
        goldenTip: 'Clarify all edge cases, state transitions in DP, and test with empty/boundary inputs.',
        tags: ['Algorithms', 'OS Internals', 'Networks', 'Graphs']
    },
    {
        id: 'priya',
        name: 'Priya Patel',
        designation: 'Specialist Programmer (SP) at Infosys',
        company: 'Infosys',
        ctc: '₹9.5 LPA',
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
    },
    {
        id: 'rohan',
        name: 'Rohan Deshmukh',
        designation: 'TCS Digital Developer at TCS',
        company: 'TCS',
        ctc: '₹7.5 LPA',
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
        name: 'Ananya Gupta',
        designation: 'Cloud Solutions Engineer at Microsoft',
        company: 'Microsoft',
        ctc: '₹38.0 LPA',
        batch: 'Batch of 2024',
        subject: 'Operating Systems',
        companyFilter: 'Microsoft',
        score: '100%',
        scoreFraction: '10 / 10',
        timeTaken: '4m 18s',
        testTitle: "Microsoft Systems & Cloud Infrastructure Test",
        avatarIcon: 'fa-cloud',
        goldenTip: 'Understand thread synchronization, virtual memory paging, and deadlock handling inside out.',
        tags: ['OS Internals', 'Concurrency', 'Networks', 'DSA']
    }
];

// Initialize Top Scorers showcase from live Alumni Hub database & load Alumni practice questions
document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderLiveTopScorers();
    loadMainAlumniPracticeQuestions();
});

async function fetchAndRenderLiveTopScorers() {
    try {
        const res = await fetch('/api/alumni/experiences');
        const data = await res.json();
        if (data.experiences && data.experiences.length > 0) {
            TOP_SCORERS.length = 0;
            data.experiences.forEach(exp => {
                TOP_SCORERS.push({
                    id: 'exp_' + exp.id,
                    name: exp.student_name,
                    designation: `${exp.role} at ${exp.company}`,
                    company: exp.company,
                    ctc: `₹${exp.package_lpa} LPA`,
                    batch: `Batch of ${exp.batch_year}`,
                    subject: 'all',
                    companyFilter: exp.company,
                    score: '100%',
                    scoreFraction: '10 / 10',
                    timeTaken: '4m 30s',
                    testTitle: `${exp.company} ${exp.role} Placement Challenge`,
                    avatarIcon: 'fa-user-graduate',
                    goldenTip: exp.advice_to_juniors || exp.preparation_tips || 'Master core CS concepts and practice coding rounds with speed and accuracy.',
                    tags: ['Interview Prep', exp.company, exp.role, 'Assessment']
                });
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

function renderTopScorerCards() {
    const grid = document.getElementById('top-scorers-grid');
    if (!grid) return;

    grid.innerHTML = '';
    TOP_SCORERS.forEach(scorer => {
        const card = document.createElement('div');
        card.className = 'scorer-card';
        card.onclick = () => startTopScorerChallenge(scorer.id);

        card.innerHTML = `
            <div>
                <div class="scorer-card-header">
                    <div class="scorer-avatar">
                        <i class="fa-solid ${scorer.avatarIcon}"></i>
                        <span class="scorer-avatar-crown"><i class="fa-solid fa-crown"></i></span>
                    </div>
                    <div class="scorer-info">
                        <h4>${scorer.name}</h4>
                        <span class="desig">${scorer.designation} (${scorer.ctc})</span>
                    </div>
                </div>

                <div class="scorer-stats-row">
                    <span><i class="fa-solid fa-trophy text-amber"></i> ${scorer.testTitle}</span>
                    <span class="record-score"><i class="fa-solid fa-star"></i> ${scorer.score}</span>
                </div>
            </div>

            <button class="btn btn-primary btn-sm scorer-card-btn" onclick="event.stopPropagation(); startTopScorerChallenge('${scorer.id}')">
                <i class="fa-solid fa-play"></i> Solve ${scorer.name.split(' ')[0]}'s Test
            </button>
        `;

        grid.appendChild(card);
    });
}

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
    const subject = document.getElementById('quiz-subject-select').value;
    const company = document.getElementById('quiz-company-select').value;

    // Determine top scorer to display
    if (presetScorer) {
        activeTopScorer = presetScorer;
    } else {
        // Find best match by company or subject
        const match = TOP_SCORERS.find(s => s.companyFilter.toLowerCase() === company.toLowerCase() || s.subject.toLowerCase() === subject.toLowerCase());
        activeTopScorer = match || TOP_SCORERS[0];
    }

    try {
        const res = await fetch(`/api/quiz/questions?subject=${encodeURIComponent(subject)}&company=${encodeURIComponent(company)}&limit=10`);
        const data = await res.json();

        if (!data.success || data.questions.length === 0) {
            showToast('No questions found for the selected filter. Loading general practice bank.', 'info');
            return;
        }

        quizQuestions = data.questions;
        currentQuestionIndex = 0;
        userAnswers = {};
        secondsRemaining = 600;

        const idlePrompt = document.getElementById('quiz-idle-prompt');
        if (idlePrompt) idlePrompt.style.display = 'none';

        document.getElementById('quiz-active-wrapper').style.display = 'block';
        document.getElementById('quiz-results-wrapper').style.display = 'none';

        // Update Live Best Scorer Benchmark Banner
        renderScorerLiveBanner(activeTopScorer);

        initQuizTimer();
        renderQuizIndicators();
        renderCurrentQuestion();
        showToast(`Challenge initiated! Benchmark: ${activeTopScorer.name} (${activeTopScorer.score})`, 'info');

        // Smooth scroll to quiz interface
        document.getElementById('quiz-active-wrapper').scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
        showToast('Error loading quiz questions: ' + err.message, 'error');
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

        const data = await response.json();
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
        const data = await res.json();

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

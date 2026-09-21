/**
 * AI Career Companion - Tailored Skill & Certification Mock Test (Module 4)
 * Generates and conducts 10-15 question online assessments based on
 * candidate resume skills, certifications, and live internet tech question feeds.
 */

let mockQuestions = [];
let currentMockIndex = 0;
let userMockAnswers = {}; // { '1': 'B', '2': 'A' }
let flaggedMockQuestions = new Set();
let mockTimerInterval = null;
let mockTimeRemaining = 720; // seconds (default 12 mins for 12 questions)
let mockTotalTime = 720;
let mockActiveSkills = [];
let mockActiveCertifications = [];
let mockTargetRole = 'Software Engineer';

document.addEventListener('DOMContentLoaded', () => {
    initMockTestModule();
});

/**
 * Initializes Mock Test tags and default parameters.
 */
function initMockTestModule() {
    updateMockSkillsPreview();
}

/**
 * Gathers skills from AppState or defaults and renders preview tags.
 */
function updateMockSkillsPreview() {
    const container = document.getElementById('mocktest-tags-container');
    const indicator = document.getElementById('mocktest-skills-count-text');
    if (!container) return;

    let skillsList = [];
    if (window.AppState && window.AppState.analyzedSkills) {
        for (const [cat, list] of Object.entries(window.AppState.analyzedSkills)) {
            skillsList.push(...list);
        }
    }

    let certsList = (window.AppState && window.AppState.analyzedCertifications) ? window.AppState.analyzedCertifications : [];

    mockActiveSkills = skillsList;
    mockActiveCertifications = certsList;

    container.innerHTML = '';

    if (skillsList.length === 0 && certsList.length === 0) {
        // Default core tech stack if no resume is scanned yet
        const defaultTags = ['Python', 'DSA & Problem Solving', 'Java / OOP', 'SQL & Databases', 'React / Web', 'Cloud & Docker', 'Core CS Fundamentals'];
        defaultTags.forEach(tag => {
            const pill = document.createElement('span');
            pill.className = 'badge badge-outline';
            pill.innerHTML = `<i class="fa-solid fa-code"></i> ${tag}`;
            container.appendChild(pill);
        });
        if (indicator) indicator.innerHTML = 'Using Comprehensive Core Tech Stack (Upload resume for custom test)';
    } else {
        // Show detected skills
        skillsList.slice(0, 15).forEach(skill => {
            const pill = document.createElement('span');
            pill.className = 'badge badge-primary';
            pill.innerHTML = `<i class="fa-solid fa-check"></i> ${skill}`;
            container.appendChild(pill);
        });

        // Show detected certifications
        certsList.forEach(cert => {
            const pill = document.createElement('span');
            pill.className = 'badge badge-warning';
            pill.innerHTML = `<i class="fa-solid fa-certificate"></i> ${cert}`;
            container.appendChild(pill);
        });

        if (indicator) {
            indicator.innerHTML = `<strong>${skillsList.length} Skills & ${certsList.length} Certifications</strong> Detected from Resume`;
        }
    }
}

/**
 * One-click trigger from Resume ATS results.
 * Transfers candidate skills & certifications into Mock Test and immediately starts the assessment.
 */
function launchTailoredMockTestFromResume() {
    // 1. Navigate to Mock Test section
    navigateTo('mocktest');

    // 2. Refresh skills preview from analyzed state
    updateMockSkillsPreview();

    // 3. Automatically initiate test generation
    setTimeout(() => {
        generateAndStartMockTest();
    }, 400);
}

/**
 * Calls backend API to fetch/generate 10-15 tailored questions.
 */
async function generateAndStartMockTest() {
    const countSelect = document.getElementById('mocktest-count-select');
    const diffSelect = document.getElementById('mocktest-difficulty-select');
    const roleSelect = document.getElementById('mocktest-role-select');

    const count = parseInt(countSelect ? countSelect.value : 12);
    const difficulty = diffSelect ? diffSelect.value : 'all';
    const targetRole = roleSelect ? roleSelect.value : 'Software Engineer';
    mockTargetRole = targetRole;

    // Show loading state
    document.getElementById('mocktest-config-wrapper').style.display = 'none';
    document.getElementById('mocktest-active-wrapper').style.display = 'none';
    document.getElementById('mocktest-scorecard-wrapper').style.display = 'none';
    document.getElementById('mocktest-loading').style.display = 'block';

    try {
        const payload = {
            skills: mockActiveSkills,
            certifications: mockActiveCertifications,
            target_role: targetRole,
            difficulty: difficulty,
            count: count
        };

        const res = await fetch('/api/mocktest/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        document.getElementById('mocktest-loading').style.display = 'none';

        if (!res.ok || !data.success || !data.questions || data.questions.length === 0) {
            showToast(data.error || 'Failed to generate mock test questions. Please try again.', 'error');
            document.getElementById('mocktest-config-wrapper').style.display = 'block';
            return;
        }

        // Initialize exam state
        mockQuestions = data.questions;
        currentMockIndex = 0;
        userMockAnswers = {};
        flaggedMockQuestions.clear();

        // Configure timer (1 minute per question)
        mockTotalTime = mockQuestions.length * 60;
        mockTimeRemaining = mockTotalTime;

        // Render Active Exam View
        document.getElementById('mocktest-active-wrapper').style.display = 'block';
        startMockTimer();
        renderMockQuestion(0);
        renderMockPalette();

        showToast(`🎯 Test Started: ${mockQuestions.length} Questions (${mockQuestions.length} Minutes)`, 'success');

    } catch (err) {
        document.getElementById('mocktest-loading').style.display = 'none';
        document.getElementById('mocktest-config-wrapper').style.display = 'block';
        showToast('Network error while generating mock test: ' + err.message, 'error');
    }
}

/**
 * Starts the live countdown timer.
 */
function startMockTimer() {
    if (mockTimerInterval) clearInterval(mockTimerInterval);
    updateMockTimerDisplay();

    mockTimerInterval = setInterval(() => {
        mockTimeRemaining--;
        updateMockTimerDisplay();

        if (mockTimeRemaining <= 0) {
            clearInterval(mockTimerInterval);
            showToast('⏰ Time is up! Submitting your assessment automatically...', 'warning');
            submitMockTest();
        }
    }, 1000);
}

function updateMockTimerDisplay() {
    const display = document.getElementById('mocktest-timer-display');
    const timerBox = document.getElementById('mocktest-timer-box');
    if (!display) return;

    const mins = Math.floor(Math.max(0, mockTimeRemaining) / 60);
    const secs = Math.max(0, mockTimeRemaining) % 60;
    display.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    if (timerBox) {
        if (mockTimeRemaining <= 60) {
            timerBox.classList.add('timer-danger');
        } else {
            timerBox.classList.remove('timer-danger');
        }
    }
}

/**
 * Renders the question at the specified index.
 */
function renderMockQuestion(index) {
    if (index < 0 || index >= mockQuestions.length) return;
    currentMockIndex = index;

    const q = mockQuestions[index];
    const qIdStr = q.id.toString();

    // Update Question Status Headers
    document.getElementById('mock-q-category').innerText = q.skill_tag || 'Core CS';
    document.getElementById('mock-q-difficulty').innerText = q.difficulty || 'Medium';
    document.getElementById('mock-current-q-num').innerText = (index + 1);
    document.getElementById('mock-total-q-num').innerText = mockQuestions.length;

    // Render Question Text
    document.getElementById('mocktest-question-text').innerText = q.question;

    // Render Options
    const optionsGrid = document.getElementById('mocktest-options-container');
    optionsGrid.innerHTML = '';

    const selectedOption = userMockAnswers[qIdStr] || null;

    for (const [key, val] of Object.entries(q.options)) {
        const optionCard = document.createElement('div');
        optionCard.className = `mock-option-card ${selectedOption === key ? 'selected' : ''}`;
        optionCard.onclick = () => selectMockOption(key);

        optionCard.innerHTML = `
            <div class="mock-option-letter">${key}</div>
            <div class="mock-option-text">${val}</div>
            <div class="mock-option-check"><i class="fa-solid fa-circle-check"></i></div>
        `;

        optionsGrid.appendChild(optionCard);
    }

    // Update Navigation Buttons
    const prevBtn = document.getElementById('mock-btn-prev');
    const nextBtn = document.getElementById('mock-btn-next');

    if (prevBtn) prevBtn.disabled = (index === 0);
    if (nextBtn) {
        if (index === mockQuestions.length - 1) {
            nextBtn.style.display = 'none';
        } else {
            nextBtn.style.display = 'inline-flex';
        }
    }

    // Update Flag Button
    const flagBtn = document.getElementById('mock-btn-flag');
    const flagText = document.getElementById('mock-flag-text');
    if (flaggedMockQuestions.has(q.id)) {
        if (flagBtn) flagBtn.classList.add('flagged-active');
        if (flagText) flagText.innerText = 'Flagged';
    } else {
        if (flagBtn) flagBtn.classList.remove('flagged-active');
        if (flagText) flagText.innerText = 'Mark for Review';
    }

    updateMockPaletteHighlights();
}

/**
 * Handles option selection.
 */
function selectMockOption(optionKey) {
    const q = mockQuestions[currentMockIndex];
    if (!q) return;

    const qIdStr = q.id.toString();
    userMockAnswers[qIdStr] = optionKey;

    // Re-render options to reflect selection
    renderMockQuestion(currentMockIndex);
}

/**
 * Clears option selection for current question.
 */
function clearMockOptionSelection() {
    const q = mockQuestions[currentMockIndex];
    if (!q) return;

    delete userMockAnswers[q.id.toString()];
    renderMockQuestion(currentMockIndex);
    showToast('Choice cleared.', 'info');
}

/**
 * Toggles review flag for current question.
 */
function toggleFlagMockQuestion() {
    const q = mockQuestions[currentMockIndex];
    if (!q) return;

    if (flaggedMockQuestions.has(q.id)) {
        flaggedMockQuestions.delete(q.id);
        showToast('Unmarked question.', 'info');
    } else {
        flaggedMockQuestions.add(q.id);
        showToast('Marked for review.', 'info');
    }

    renderMockQuestion(currentMockIndex);
}

function nextMockQuestion() {
    if (currentMockIndex < mockQuestions.length - 1) {
        renderMockQuestion(currentMockIndex + 1);
    }
}

function prevMockQuestion() {
    if (currentMockIndex > 0) {
        renderMockQuestion(currentMockIndex - 1);
    }
}

/**
 * Renders the interactive Question Palette Grid.
 */
function renderMockPalette() {
    const grid = document.getElementById('mocktest-palette-container');
    if (!grid) return;

    grid.innerHTML = '';

    mockQuestions.forEach((q, idx) => {
        const btn = document.createElement('button');
        btn.className = 'palette-btn';
        btn.id = `palette-btn-${idx}`;
        btn.innerText = (idx + 1);
        btn.onclick = () => renderMockQuestion(idx);
        grid.appendChild(btn);
    });

    updateMockPaletteHighlights();
}

/**
 * Updates palette button colors according to question status.
 */
function updateMockPaletteHighlights() {
    mockQuestions.forEach((q, idx) => {
        const btn = document.getElementById(`palette-btn-${idx}`);
        if (!btn) return;

        btn.className = 'palette-btn';

        const isCurrent = (idx === currentMockIndex);
        const isAnswered = Boolean(userMockAnswers[q.id.toString()]);
        const isFlagged = flaggedMockQuestions.has(q.id);

        if (isCurrent) btn.classList.add('current');
        else if (isFlagged) btn.classList.add('flagged');
        else if (isAnswered) btn.classList.add('answered');
        else btn.classList.add('unattempted');
    });
}

/**
 * Prompts user confirmation before submitting test.
 */
function confirmSubmitMockTest() {
    const answeredCount = Object.keys(userMockAnswers).length;
    const totalCount = mockQuestions.length;
    const unansweredCount = totalCount - answeredCount;
    const flaggedCount = flaggedMockQuestions.size;

    let msg = `You have answered ${answeredCount} of ${totalCount} questions.`;
    if (unansweredCount > 0) {
        msg += ` (${unansweredCount} unanswered)`;
    }
    if (flaggedCount > 0) {
        msg += ` [${flaggedCount} marked for review]`;
    }
    msg += `\n\nAre you ready to submit your test and view your detailed skill scorecard?`;

    if (confirm(msg)) {
        submitMockTest();
    }
}

/**
 * Submits answers to backend for comprehensive evaluation.
 */
async function submitMockTest() {
    if (mockTimerInterval) clearInterval(mockTimerInterval);

    const timeSpent = Math.max(1, mockTotalTime - mockTimeRemaining);

    // Show loading spinner
    document.getElementById('mocktest-active-wrapper').style.display = 'none';
    document.getElementById('mocktest-loading').style.display = 'block';

    try {
        const payload = {
            questions: mockQuestions,
            answers: userMockAnswers,
            time_taken_seconds: timeSpent
        };

        const res = await fetch('/api/mocktest/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        document.getElementById('mocktest-loading').style.display = 'none';

        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to submit test. Please retry.', 'error');
            document.getElementById('mocktest-active-wrapper').style.display = 'block';
            return;
        }

        // Render comprehensive scorecard
        renderMockScorecard(data);
        showToast(`🎉 Test Evaluated! Score: ${data.score_percentage}%`, 'success');

    } catch (err) {
        document.getElementById('mocktest-loading').style.display = 'none';
        document.getElementById('mocktest-active-wrapper').style.display = 'block';
        showToast('Error submitting test: ' + err.message, 'error');
    }
}

/**
 * Renders the post-test analytics scorecard and question-by-question review.
 */
function renderMockScorecard(data) {
    const wrapper = document.getElementById('mocktest-scorecard-wrapper');
    if (!wrapper) return;

    wrapper.style.display = 'block';

    let skillCardsHtml = '';
    for (const [skill, stats] of Object.entries(data.skill_breakdown)) {
        const barColor = stats.score_pct >= 75 ? '#10B981' : stats.score_pct >= 50 ? '#F59E0B' : '#EF4444';
        skillCardsHtml += `
            <div class="mock-skill-metric-card">
                <div class="metric-top">
                    <span class="skill-name font-bold">${skill}</span>
                    <span class="skill-score font-bold" style="color: ${barColor}">${stats.score_pct}% (${stats.correct}/${stats.total})</span>
                </div>
                <div class="mock-progress-bar-bg mt-2">
                    <div class="mock-progress-bar-fill" style="width: ${stats.score_pct}%; background: ${barColor};"></div>
                </div>
            </div>
        `;
    }

    let reviewHtml = '';
    data.detailed_review.forEach((q, idx) => {
        const statusBadge = q.is_correct 
            ? `<span class="badge badge-success"><i class="fa-solid fa-check"></i> Correct</span>`
            : q.is_attempted
                ? `<span class="badge badge-danger"><i class="fa-solid fa-xmark"></i> Incorrect</span>`
                : `<span class="badge badge-outline"><i class="fa-solid fa-minus"></i> Skipped</span>`;

        reviewHtml += `
            <div class="review-question-card ${q.is_correct ? 'card-correct' : q.is_attempted ? 'card-incorrect' : 'card-skipped'} mt-3">
                <div class="review-q-header">
                    <div>
                        <span class="font-bold">Q${idx + 1}.</span>
                        <span class="badge badge-primary ml-2">${q.skill}</span>
                        <span class="badge badge-outline ml-1">${q.difficulty}</span>
                    </div>
                    ${statusBadge}
                </div>
                <h4 class="mt-2 mb-3">${q.question}</h4>
                <div class="review-options-grid">
                    ${Object.entries(q.options).map(([k, v]) => `
                        <div class="review-opt ${k === q.correct_option ? 'opt-correct' : (k === q.user_option && !q.is_correct ? 'opt-user-wrong' : '')}">
                            <strong>${k}.</strong> ${v}
                            ${k === q.correct_option ? ' <i class="fa-solid fa-check text-success"></i>' : ''}
                            ${k === q.user_option && !q.is_correct ? ' <i class="fa-solid fa-xmark text-danger"></i> (Your Choice)' : ''}
                        </div>
                    `).join('')}
                </div>
                <div class="review-explanation-box mt-3">
                    <strong><i class="fa-solid fa-lightbulb text-amber"></i> Solution & Rationale:</strong>
                    <p class="mt-1 mb-0">${q.explanation}</p>
                </div>
            </div>
        `;
    });

    wrapper.innerHTML = `
        <div class="scorecard-header text-center p-4">
            <span class="badge badge-primary font-bold"><i class="fa-solid fa-trophy"></i> Assessment Result</span>
            <div class="scorecard-score-circle mt-3" style="border-color: ${data.rating_color};">
                <div class="score-num" style="color: ${data.rating_color};">${data.score_percentage}%</div>
                <div class="score-subtext">${data.correct_count} / ${data.total_questions} Correct</div>
            </div>
            <h2 class="mt-3 mb-1" style="color: ${data.rating_color};">${data.rating}</h2>
            <p class="text-muted">${data.badge} &bull; Time Spent: <strong>${data.time_taken_formatted}</strong></p>

            <div class="scorecard-quick-stats-row mt-4">
                <div class="quick-stat-box">
                    <div class="stat-num text-success">${data.correct_count}</div>
                    <div class="stat-lbl">Correct Answers</div>
                </div>
                <div class="quick-stat-box">
                    <div class="stat-num text-danger">${data.attempted_count - data.correct_count}</div>
                    <div class="stat-lbl">Incorrect Answers</div>
                </div>
                <div class="quick-stat-box">
                    <div class="stat-num text-muted">${data.total_questions - data.attempted_count}</div>
                    <div class="stat-lbl">Skipped Questions</div>
                </div>
                <div class="quick-stat-box">
                    <div class="stat-num text-primary">${Math.round((data.correct_count / max(1, data.attempted_count)) * 100)}%</div>
                    <div class="stat-lbl">Accuracy</div>
                </div>
            </div>
        </div>

        <!-- Skill by Skill Breakdown -->
        <div class="scorecard-skills-section mt-4 p-4" style="background:var(--bg-base); border-radius:var(--radius-lg);">
            <h3><i class="fa-solid fa-chart-pie text-primary"></i> Skill-by-Skill Performance Breakdown</h3>
            <p class="text-muted">Analyze your strengths and weak areas identified from this assessment:</p>
            <div class="mock-skills-breakdown-grid mt-3">
                ${skillCardsHtml}
            </div>
        </div>

        <!-- Question by Question Review -->
        <div class="scorecard-review-section mt-4 p-4">
            <h3><i class="fa-solid fa-list-check text-primary"></i> Detailed Question Review & Explanations</h3>
            <div class="review-questions-list mt-3">
                ${reviewHtml}
            </div>
        </div>

        <!-- Bottom Action Bar -->
        <div class="scorecard-bottom-actions mt-4 p-4 text-center" style="border-top:1px solid var(--border-color);">
            <button class="btn btn-outline btn-lg mr-2" onclick="retakeMockTest()">
                <i class="fa-solid fa-arrows-rotate"></i> Retake / Generate New Test Set
            </button>
            <button class="btn btn-primary btn-lg" onclick="navigateTo('analyzer')">
                <i class="fa-solid fa-file-invoice"></i> Back to Resume ATS
            </button>
        </div>
    `;

    wrapper.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function retakeMockTest() {
    document.getElementById('mocktest-scorecard-wrapper').style.display = 'none';
    document.getElementById('mocktest-active-wrapper').style.display = 'none';
    document.getElementById('mocktest-config-wrapper').style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function max(a, b) {
    return Math.max(a, b);
}

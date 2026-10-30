
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
 * Checks whether candidate has analyzed a resume in current session.
 * STRICT RULE: Mock assessment is exclusively accessible after a resume is analyzed.
 */
function isResumeAnalyzed() {
    if (window.currentResumeAnalysis && (window.currentResumeAnalysis.extracted_skills || window.currentResumeAnalysis.company_skills_intelligence)) {
        return true;
    }
    try {
        const cached = sessionStorage.getItem('activeResumeAnalysis');
        if (cached) {
            const parsed = JSON.parse(cached);
            if (parsed && (parsed.extracted_skills || parsed.company_skills_intelligence)) {
                window.currentResumeAnalysis = parsed;
                return true;
            }
        }
    } catch (_) {}
    if (window.AppState && window.AppState.analyzedSkills && Object.keys(window.AppState.analyzedSkills).length > 0) {
        return true;
    }
    if (window.AppState && Array.isArray(window.AppState.matchedCompanySkills) && window.AppState.matchedCompanySkills.length > 0) {
        return true;
    }
    return false;
}

/**
 * Initializes Mock Test tags and default parameters.
 */
function initMockTestModule() {
    updateMockSkillsPreview();
}

/**
 * Hero section action handlers enforcing strict resume analysis prerequisite
 */
window.handleHeroStartMockTest = function() {
    if (!isResumeAnalyzed()) {
        showToast('Mock Assessment Locked: You must upload and analyze your resume first.', 'warning');
        if (typeof navigateTo === 'function') navigateTo('analyzer');
        return;
    }
    generateAndStartMockTest();
};

window.handleHeroConfigMockTest = function() {
    if (!isResumeAnalyzed()) {
        showToast('Mock Assessment Locked: You must upload and analyze your resume first.', 'warning');
        if (typeof navigateTo === 'function') navigateTo('analyzer');
        return;
    }
    const cfg = document.getElementById('mocktest-config-wrapper');
    if (cfg) cfg.scrollIntoView({ behavior: 'smooth', block: 'start' });
};

/**
 * Gathers skills strictly from verified company requirements matched against resume.
 * STRICT RULE: No arbitrary custom skills, no un-matched defaults.
 */
function updateMockSkillsPreview() {
    const lockedWrapper = document.getElementById('mocktest-locked-wrapper');
    const configWrapper = document.getElementById('mocktest-config-wrapper');
    const container = document.getElementById('mocktest-tags-container');
    const indicator = document.getElementById('mocktest-skills-count-text');

    const analyzed = isResumeAnalyzed();

    if (!analyzed) {
        // Enforce Locked State
        if (lockedWrapper) lockedWrapper.style.display = 'block';
        if (configWrapper) configWrapper.style.display = 'none';
        return;
    }

    // Resume is analyzed -> Show Config
    if (lockedWrapper) lockedWrapper.style.display = 'none';
    if (configWrapper) configWrapper.style.display = 'block';

    if (!container) return;

    // Retrieve STRICTLY the skills matched with companies in the database from the resume
    let matchedSkills = [];
    if (window.currentResumeAnalysis) {
        const intel = window.currentResumeAnalysis.company_skills_intelligence;
        if (intel && Array.isArray(intel.matched_company_skills) && intel.matched_company_skills.length > 0) {
            matchedSkills = [...intel.matched_company_skills];
        } else if (window.currentResumeAnalysis.mandatory_mocktest && Array.isArray(window.currentResumeAnalysis.mandatory_mocktest.skills_to_test)) {
            matchedSkills = [...window.currentResumeAnalysis.mandatory_mocktest.skills_to_test];
        }
    }
    if (matchedSkills.length === 0 && window.AppState && Array.isArray(window.AppState.matchedCompanySkills)) {
        matchedSkills = [...window.AppState.matchedCompanySkills];
    }
    if (matchedSkills.length === 0 && window.AppState && window.AppState.analyzedSkills) {
        for (const [cat, list] of Object.entries(window.AppState.analyzedSkills)) {
            if (Array.isArray(list)) matchedSkills.push(...list);
        }
    }

    // Deduplicate
    matchedSkills = Array.from(new Set(matchedSkills.map(s => s.trim()).filter(Boolean)));

    mockActiveSkills = [...matchedSkills];
    container.innerHTML = '';

    if (matchedSkills.length === 0) {
        container.innerHTML = '<div style="color:var(--text-secondary); font-size:0.92rem; padding:0.5rem 0;"><i class="fa-solid fa-circle-exclamation text-amber"></i> No matching company tech skills identified. Basic CS fundamentals will be tested.</div>';
        if (indicator) indicator.innerHTML = 'Foundational CS Assessment';
        return;
    }

    matchedSkills.forEach(tag => {
        const isSelected = mockActiveSkills.includes(tag);
        const pill = document.createElement('div');
        pill.className = isSelected ? 'm-skill-chip selected' : 'm-skill-chip unselected';
        pill.innerHTML = isSelected 
            ? `<i class="fa-solid fa-check"></i> <span>${tag}</span> <span style="font-size:0.68rem; background:rgba(16,185,129,0.15); color:#059669; padding:2px 6px; border-radius:999px; margin-left:6px; font-weight:600;"><i class="fa-solid fa-building" style="font-size:0.6rem;"></i> Company Matched</span>`
            : `<i class="fa-regular fa-square"></i> <span>${tag}</span>`;
        
        pill.onclick = function() {
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                this.classList.add('unselected');
                this.innerHTML = `<i class="fa-regular fa-square"></i> <span>${tag}</span>`;
                mockActiveSkills = mockActiveSkills.filter(s => s !== tag);
            } else {
                this.classList.remove('unselected');
                this.classList.add('selected');
                this.innerHTML = `<i class="fa-solid fa-check"></i> <span>${tag}</span> <span style="font-size:0.68rem; background:rgba(16,185,129,0.15); color:#059669; padding:2px 6px; border-radius:999px; margin-left:6px; font-weight:600;"><i class="fa-solid fa-building" style="font-size:0.6rem;"></i> Company Matched</span>`;
                if (!mockActiveSkills.includes(tag)) mockActiveSkills.push(tag);
            }
        };
        container.appendChild(pill);
    });

    if (indicator) {
        indicator.innerHTML = `<i class="fa-solid fa-circle-check text-success"></i> ${matchedSkills.length} Verified Company-Matched Skills Ready`;
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

    // 3. Automatically initiate test generation (using pre-generated assessment if available)
    setTimeout(() => {
        if (window.currentResumeAnalysis && 
            window.currentResumeAnalysis.mandatory_mocktest && 
            window.currentResumeAnalysis.mandatory_mocktest.questions && 
            window.currentResumeAnalysis.mandatory_mocktest.questions.length > 0) {
            
            startMandatoryPreGeneratedTest(window.currentResumeAnalysis.mandatory_mocktest);
        } else {
            generateAndStartMockTest();
        }
    }, 400);
}

function startMandatoryPreGeneratedTest(mockData) {
    document.getElementById('mocktest-config-wrapper').style.display = 'none';
    document.getElementById('mocktest-loading').style.display = 'none';
    document.getElementById('mocktest-scorecard-wrapper').style.display = 'none';

    mockQuestions = mockData.questions;
    mockTargetRole = mockData.target_role || 'Software Engineer';
    currentMockIndex = 0;
    userMockAnswers = {};
    flaggedMockQuestions.clear();

    mockTotalTime = mockQuestions.length * 60;
    mockTimeRemaining = mockTotalTime;

    document.getElementById('mocktest-active-wrapper').style.display = 'block';
    startMockTimer();
    renderMockQuestion(0);
    renderMockPalette();

    showToast(`🎯 Mandatory Assessment Started: ${mockQuestions.length} Questions (${mockTargetRole})`, 'success');
}

/**
 * Calls backend API to fetch/generate 10-15 tailored questions.
 */
async function generateAndStartMockTest() {
    if (!isResumeAnalyzed()) {
        showToast('Mock Assessment Locked: Please upload and analyze your resume first.', 'warning');
        if (typeof navigateTo === 'function') navigateTo('analyzer');
        return;
    }
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

        const data = await safeJsonFetch(res);
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
        const activeRecId = window.currentResumeAnalysis?.history_record_id || 
                            window.currentResumeAnalysis?.mandatory_mocktest?.resume_record_id || 
                            (sessionStorage.getItem('activeResumeRecordId') ? parseInt(sessionStorage.getItem('activeResumeRecordId')) : null);

        const payload = {
            questions: mockQuestions,
            answers: userMockAnswers,
            time_taken_seconds: timeSpent,
            resume_record_id: activeRecId
        };

        const res = await fetch('/api/mocktest/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await safeJsonFetch(res);
        document.getElementById('mocktest-loading').style.display = 'none';

        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to submit test. Please retry.', 'error');
            document.getElementById('mocktest-active-wrapper').style.display = 'block';
            return;
        }

        // Update active resume analysis state to unlock report per Step 3 & 4
        if (!window.currentResumeAnalysis) {
            try {
                const cached = sessionStorage.getItem('activeResumeAnalysis');
                if (cached) window.currentResumeAnalysis = JSON.parse(cached);
            } catch (_) {}
        }
        if (!window.currentResumeAnalysis) {
            window.currentResumeAnalysis = {
                filename: 'Evaluated_Resume.pdf',
                extracted_skills: mockActiveSkills,
                matched_company_skills: mockActiveSkills,
                history_record_id: data.resume_record_id || activeRecId || 0
            };
        }

        window.currentResumeAnalysis.test_completed = true;
        window.currentResumeAnalysis.mocktest_score = (data.score_percentage !== undefined && data.score_percentage !== null) ? data.score_percentage : 0;
        window.currentResumeAnalysis.mocktest_rating = data.rating || 'Placement Ready';
        window.currentResumeAnalysis.mocktest_data = {
            score: data.score_percentage,
            rating: data.rating,
            total_questions: data.total_questions,
            correct_count: data.correct_count,
            accuracy: data.accuracy || data.score_percentage,
            role: mockTargetRole,
            skills: mockActiveSkills,
            skill_breakdown: data.skill_breakdown,
            time_taken_seconds: timeSpent,
            completed_at: new Date().toISOString()
        };
        if (!window.currentResumeAnalysis.report_status) {
            window.currentResumeAnalysis.report_status = {};
        }
        window.currentResumeAnalysis.report_status.unlocked = true;
        if (data.resume_record_id) {
            window.currentResumeAnalysis.history_record_id = data.resume_record_id;
            sessionStorage.setItem('activeResumeRecordId', String(data.resume_record_id));
        }

        sessionStorage.setItem('mocktest_completed', 'true');
        sessionStorage.setItem('activeMocktestScore', String((data.score_percentage !== undefined && data.score_percentage !== null) ? data.score_percentage : 0));
        if (window.AppState) {
            window.AppState.mockTestCompleted = true;
        }

        try {
            sessionStorage.setItem('activeResumeAnalysis', JSON.stringify(window.currentResumeAnalysis));
        } catch (_) {}

        if (typeof updateReportBannerStatus === 'function') {
            updateReportBannerStatus(window.currentResumeAnalysis);
        }

        // Render comprehensive scorecard
        renderMockScorecard(data);
        showToast(`🎉 Mandatory Assessment Evaluated! Score: ${data.score_percentage}% • Report Unlocked!`, 'success');

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

    const heroEl = document.querySelector('.mocktest-hero');
    if (heroEl) heroEl.style.display = 'none';

    const cfgEl = document.getElementById('mocktest-config-wrapper');
    if (cfgEl) cfgEl.style.display = 'none';

    wrapper.style.display = 'block';

    const resumeAts = window.currentResumeAnalysis?.ats_analysis?.ats_score 
        ? Math.round(window.currentResumeAnalysis.ats_analysis.ats_score) 
        : (data.resume_match_score || 80);
    const mockScore = data.score_percentage || 0;
    const combinedScore = Math.round((resumeAts + mockScore) / 2);

    // 1. Skill by Skill Breakdown Cards
    let skillCardsHtml = '';
    for (const [skill, stats] of Object.entries(data.skill_breakdown || {})) {
        const barColor = stats.score_pct >= 75 ? '#10B981' : stats.score_pct >= 50 ? '#F59E0B' : '#EF4444';
        const learnUrl = stats.learn_url || `https://learn-anything.xyz/${encodeURIComponent(skill.toLowerCase())}`;
        skillCardsHtml += `
            <div class="mock-skill-metric-card" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:1rem;">
                <div class="metric-top" style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="skill-name font-bold" style="color:var(--text-primary);">${skill}</span>
                    <span class="skill-score font-bold" style="color: ${barColor}">${stats.score_pct}% (${stats.correct}/${stats.total})</span>
                </div>
                <div class="mock-progress-bar-bg mt-2" style="height:7px; background:var(--border-color); border-radius:4px; overflow:hidden;">
                    <div class="mock-progress-bar-fill" style="width: ${stats.score_pct}%; height:100%; background: ${barColor};"></div>
                </div>
                <div class="mt-2 text-right">
                    <a href="${learnUrl}" target="_blank" rel="noopener" style="font-size:0.75rem; color:#2563EB; font-weight:600; text-decoration:none;">
                        <i class="fa-solid fa-arrow-up-right-from-square"></i> Learn on learn-anything.xyz
                    </a>
                </div>
            </div>
        `;
    }

    // 2. The Negative Side: Resume-Claimed Skills Unverified in Practical Test
    const negSkills = data.negative_skills || [];
    let negativeSideHtml = '';
    if (negSkills.length > 0) {
        negativeSideHtml = `
            <div class="card p-4 mt-4" style="background:#FEF2F2; border:2px solid #F87171; border-radius:16px;">
                <div style="display:flex; align-items:flex-start; gap:0.85rem;">
                    <div style="width:44px; height:44px; border-radius:12px; background:#EF4444; color:#fff; display:flex; align-items:center; justify-content:center; font-size:1.3rem; flex-shrink:0;">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <div style="flex:1;">
                        <h4 style="margin:0 0 0.3rem; color:#991B1B; font-size:1.05rem; font-weight:800;">
                            ⚠️ The Negative Side: Resume Claims Unverified in Practical Test
                        </h4>
                        <p style="margin:0 0 0.85rem; font-size:0.84rem; color:#7F1D1D; line-height:1.5;">
                            <strong>Critical Recruiter Vulnerability Identified:</strong> You listed these technical competencies on your resume, but could not answer related questions in the practical assessment. Technical recruiters and interviewers probe into claimed CV skills; unverified claims lead to immediate interview elimination.
                        </p>
                        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:0.75rem;">
                            ${negSkills.map(ns => `
                                <div style="background:#fff; border:1px solid #FECACA; border-radius:10px; padding:0.75rem 0.95rem;">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <strong style="color:#991B1B; font-size:0.9rem;">${ns.skill}</strong>
                                        <span class="badge" style="background:#FEE2E2; color:#B91C1C; font-size:0.75rem; font-weight:700;">${ns.score_pct}% (${ns.correct}/${ns.total})</span>
                                    </div>
                                    <p style="margin:0.35rem 0 0.5rem; font-size:0.78rem; color:#64748B;">${ns.assessment}</p>
                                    <a href="${ns.learn_url}" target="_blank" rel="noopener" style="display:inline-flex; align-items:center; gap:0.35rem; font-size:0.76rem; color:#2563EB; font-weight:700; text-decoration:none;">
                                        <i class="fa-solid fa-graduation-cap"></i> Remediate on learn-anything.xyz &rarr;
                                    </a>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    } else {
        negativeSideHtml = `
            <div class="card p-3 mt-4" style="background:#F0FDF4; border:1.5px solid #86EFAC; border-radius:14px;">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <i class="fa-solid fa-shield-check text-success" style="font-size:1.4rem;"></i>
                    <div>
                        <strong style="color:#166534; font-size:0.92rem;">Zero Critical Vulnerabilities Detected</strong>
                        <p style="margin:0; font-size:0.8rem; color:#15803D;">All skills claimed in your resume were successfully validated with passing scores in the technical examination.</p>
                    </div>
                </div>
            </div>
        `;
    }

    // 3. Target Industry Cluster Companies to Approach
    const topComps = window.currentResumeAnalysis?.dataset_matching?.top_matches || [];
    let companiesHtml = '';
    if (topComps.length > 0) {
        companiesHtml = `
            <div class="scorecard-companies-section mt-4 p-4" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:1rem;">
                    <div>
                        <h3 style="margin:0; font-size:1.05rem;"><i class="fa-solid fa-building-circle-check text-primary"></i> Target Campus Recruiters to Approach</h3>
                        <p class="text-muted" style="margin:0.2rem 0 0; font-size:0.82rem;">Companies actively hiring freshers under your verified technology cluster:</p>
                    </div>
                    <span class="badge badge-primary font-bold">12 Technology Clusters</span>
                </div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:0.85rem;">
                    ${topComps.slice(0, 4).map(c => `
                        <div style="background:var(--bg-base); border:1px solid var(--border-color); border-radius:12px; padding:0.9rem;">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <div>
                                    <h4 style="margin:0; font-size:0.95rem; font-weight:700;">${c.company}</h4>
                                    <span style="font-size:0.78rem; color:var(--text-secondary);">${c.role}</span>
                                </div>
                                <span class="badge badge-success font-bold" style="font-size:0.75rem;">${c.match_score}% Match</span>
                            </div>
                            <div style="margin-top:0.6rem; display:flex; justify-content:space-between; align-items:center; font-size:0.78rem;">
                                <span style="color:#059669; font-weight:600;"><i class="fa-solid fa-indian-rupee-sign"></i> ${c.indicative_ctc || '3.5 - 6.5 LPA'}</span>
                                <span class="badge badge-outline" style="font-size:0.7rem;">${c.fit_tier || 'High Fit'}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // 4. 3-5 Step Growth & Placement Action Plan
    const growthPlan = data.growth_plan || [
        "Correct Unverified Skills: Focus immediate practice on skills where test accuracy was below passing threshold.",
        "Demonstrate Hands-On Implementation: Build a portfolio repository on GitHub with unit tests proving competency.",
        "Target Verified Recruiter Clusters: Apply directly to campus recruiters hiring in your verified domain.",
        "Retake Technical Assessment: Elevate your hands-on accuracy across all tested skills above 85% to achieve Elite Placement Ready certification."
    ];
    const growthPlanHtml = `
        <div class="scorecard-growth-section mt-4 p-4" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:16px;">
            <h3 style="margin:0 0 0.4rem; font-size:1.05rem;"><i class="fa-solid fa-stairs text-primary"></i> 4-Step Strategic Placement Growth Plan</h3>
            <p class="text-muted" style="margin:0 0 1rem; font-size:0.82rem;">Personalized roadmap to correct weaknesses and maximize recruitment conversion:</p>
            <div style="display:flex; flex-direction:column; gap:0.65rem;">
                ${growthPlan.map((step, idx) => `
                    <div style="display:flex; align-items:flex-start; gap:0.75rem; background:var(--bg-base); border:1px solid var(--border-color); border-radius:10px; padding:0.75rem 1rem;">
                        <span style="width:26px; height:26px; border-radius:50%; background:#2563EB; color:#fff; display:flex; align-items:center; justify-content:center; font-size:0.78rem; font-weight:800; flex-shrink:0;">${idx + 1}</span>
                        <div style="font-size:0.83rem; line-height:1.45; color:var(--text-primary);">${step}</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    // 5. Interactive Remediation Resources from learn-anything.xyz
    const resources = data.learning_resources || [];
    let resourcesHtml = '';
    if (resources.length > 0) {
        resourcesHtml = `
            <div class="scorecard-resources-section mt-4 p-4" style="background: linear-gradient(135deg, #EFF6FF 0%, #F5F3FF 100%); border:1.5px solid #BFDBFE; border-radius:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.85rem;">
                    <div>
                        <h3 style="margin:0; font-size:1.05rem; color:#1E40AF;"><i class="fa-solid fa-compass text-primary"></i> Interactive Learning Roadmaps (Powered by learn-anything.xyz)</h3>
                        <p style="margin:0.2rem 0 0; font-size:0.82rem; color:#3B82F6;">Master lacking skills and advance your competencies with community-verified knowledge maps:</p>
                    </div>
                    <a href="https://learn-anything.xyz/" target="_blank" rel="noopener" class="badge badge-primary font-bold" style="padding:0.4rem 0.75rem; text-decoration:none;">Visit learn-anything.xyz &rarr;</a>
                </div>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:0.75rem;">
                    ${resources.slice(0, 6).map(res => `
                        <div style="background:#fff; border:1px solid #DBEAFE; border-radius:12px; padding:0.85rem; display:flex; flex-direction:column; justify-content:space-between;">
                            <div>
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                                    <strong style="color:#0F172A; font-size:0.9rem;">${res.skill}</strong>
                                    <span class="badge ${res.badge_class || 'badge-primary'}" style="font-size:0.68rem;">${res.status || 'Roadmap'}</span>
                                </div>
                                <p style="margin:0 0 0.65rem; font-size:0.76rem; color:#64748B;">Interactive topic tree, tutorials, and deep-dive conceptual guides.</p>
                            </div>
                            <a href="${res.url}" target="_blank" rel="noopener" class="btn btn-sm btn-outline" style="display:inline-flex; align-items:center; justify-content:center; gap:0.4rem; font-size:0.76rem; color:#1D4ED8; border-color:#93C5FD; text-decoration:none; font-weight:700;">
                                <i class="fa-solid fa-arrow-up-right-from-square"></i> Open Map on learn-anything.xyz
                            </a>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // 6. Question-by-Question Detailed Review
    let reviewHtml = '';
    (data.detailed_review || []).forEach((q, idx) => {
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
                    ${Object.entries(q.options || {}).map(([k, v]) => `
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
        <!-- Step 4: Official Report Unlocked Celebration Card -->
        <div class="card p-3 mb-4" style="background: linear-gradient(135deg, #ECFDF5 0%, #EFF6FF 100%); border: 2px solid #10B981; border-radius: 16px; margin: 0 0 1.5rem; width: 100%; box-shadow: 0 8px 24px -4px rgba(16, 185, 129, 0.2);">
            <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem;">
                <div style="display:flex; align-items:center; gap:0.85rem;">
                    <div style="width:48px; height:48px; border-radius:12px; background:#10B981; color:#fff; display:flex; align-items:center; justify-content:center; font-size:1.4rem; flex-shrink:0;">
                        <i class="fa-solid fa-lock-open"></i>
                    </div>
                    <div>
                        <h4 style="margin:0 0 0.2rem; color:#065F46; font-size:1.05rem; font-weight:800;">Step 4: Verified Performance Report Unlocked!</h4>
                        <p style="margin:0; font-size:0.84rem; color:#047857;">Resume Match: <strong>${resumeAts}%</strong> &bull; Mock Test: <strong>${data.score_percentage}% (${data.rating})</strong> &bull; Score attached to resume.</p>
                    </div>
                </div>
                <button class="btn btn-primary" onclick="downloadCurrentResumeReport()" style="background:#059669; border-color:#059669; font-weight:700; padding:0.65rem 1.35rem; display:inline-flex; align-items:center; gap:0.5rem; border-radius:12px; box-shadow:0 4px 12px rgba(5,150,105,0.35); cursor:pointer;">
                    <i class="fa-solid fa-file-arrow-down"></i> Download Verified Report (PDF)
                </button>
            </div>
        </div>

        <!-- Dual Gauge Scorecard Header -->
        <div class="scorecard-header p-4" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:16px; width:100%;">
            <div class="scorecard-gauges-grid" style="display:grid; grid-template-columns: 1fr 1.3fr 1fr; align-items:center; justify-items:center; gap:1.5rem; max-width:880px; margin:0 auto; text-align:center;">
                <!-- Resume Match Gauge -->
                <div style="display:flex; flex-direction:column; align-items:center;">
                    <span class="badge badge-secondary font-bold" style="font-size:0.75rem;"><i class="fa-solid fa-file-lines"></i> Resume Match</span>
                    <div class="scorecard-score-circle mt-2" style="border: 7px solid #2563EB; width:115px; height:115px; margin:0.5rem auto; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:50%; background:var(--bg-surface); box-shadow:0 4px 14px rgba(37,99,235,0.15);">
                        <div class="score-num" style="color: #2563EB; font-size:1.7rem; font-weight:800;">${resumeAts}%</div>
                        <div class="score-subtext" style="font-size:0.72rem; color:var(--text-muted);">ATS Match Index</div>
                    </div>
                </div>

                <!-- Combined Badge -->
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;">
                    <span class="badge badge-primary font-bold" style="padding:0.4rem 0.8rem; font-size:0.82rem;"><i class="fa-solid fa-award"></i> Combined Readiness</span>
                    <h2 class="mt-2 mb-0" style="color: ${data.rating_color}; font-size:2rem; font-weight:800; line-height:1.1;">${combinedScore}%</h2>
                    <p style="color: ${data.rating_color}; font-weight:700; font-size:0.92rem; margin:0.25rem 0;">${data.rating}</p>
                    <p class="text-muted" style="font-size:0.8rem; margin:0;">${data.badge} &bull; Time: <strong>${data.time_taken_formatted}</strong></p>
                </div>

                <!-- Mock Test Result Gauge -->
                <div style="display:flex; flex-direction:column; align-items:center;">
                    <span class="badge badge-secondary font-bold" style="font-size:0.75rem;"><i class="fa-solid fa-check-double"></i> Practical Test</span>
                    <div class="scorecard-score-circle mt-2" style="border: 7px solid ${data.rating_color}; width:115px; height:115px; margin:0.5rem auto; display:flex; flex-direction:column; align-items:center; justify-content:center; border-radius:50%; background:var(--bg-surface); box-shadow:0 4px 14px rgba(0,0,0,0.06);">
                        <div class="score-num" style="color: ${data.rating_color}; font-size:1.7rem; font-weight:800;">${data.score_percentage}%</div>
                        <div class="score-subtext" style="font-size:0.72rem; color:var(--text-muted);">${data.correct_count} / ${data.total_questions} Correct</div>
                    </div>
                </div>
            </div>

            <div class="scorecard-quick-stats-row mt-4" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:1rem; max-width:880px; margin:1.5rem auto 0;">
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
                    <div class="stat-num text-primary">${Math.round((data.correct_count / Math.max(1, data.attempted_count || 1)) * 100)}%</div>
                    <div class="stat-lbl">Accuracy</div>
                </div>
            </div>
        </div>

        <!-- Target Companies to Approach -->
        ${companiesHtml}

        <!-- The Negative Side / Vulnerability Assessment -->
        ${negativeSideHtml}

        <!-- 4-Step Strategic Placement Growth Plan -->
        ${growthPlanHtml}

        <!-- Interactive Remediation Resources from learn-anything.xyz -->
        ${resourcesHtml}

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
        <div class="scorecard-bottom-actions mt-4 p-4 text-center" style="border-top:1px solid var(--border-color); display:flex; justify-content:center; gap:0.75rem; flex-wrap:wrap;">
            <button class="btn btn-primary btn-lg" onclick="downloadCurrentResumeReport()" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); border-color:#059669; font-weight:700;">
                <i class="fa-solid fa-file-arrow-down"></i> Download Verified Report (PDF)
            </button>
            <button class="btn btn-outline btn-lg" onclick="retakeMockTest()">
                <i class="fa-solid fa-arrows-rotate"></i> Retake Assessment
            </button>
            <button class="btn btn-secondary btn-lg" onclick="navigateTo('analyzer')">
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

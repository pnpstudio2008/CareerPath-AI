/**
 * AI Career Companion - Resume Analyzer & ATS Optimizer (Module 1)
 */

let selectedResumeFile = null;

function switchInputMode(mode) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.input-mode-container').forEach(c => c.classList.remove('active'));

    const tabBtn = document.getElementById(`tab-${mode}`);
    const container = document.getElementById(`input-mode-${mode}`);

    if (tabBtn) tabBtn.classList.add('active');
    if (container) container.classList.add('active');
}

function initDropZone() {
    const dropZone = document.getElementById('drop-zone');
    if (!dropZone) return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
}

function handleFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    if (!file) return;

    const fileNameLower = file.name.toLowerCase();

    // 1. Strict Malware Protection: Prohibit all .docx and Word files
    if (fileNameLower.endsWith('.docx') || fileNameLower.endsWith('.doc') || fileNameLower.endsWith('.docm') ||
        (file.type && (file.type.includes('wordprocessingml') || file.type.includes('msword')))) {
        selectedResumeFile = null;
        const fileInput = document.getElementById('resume-file-input');
        if (fileInput) fileInput.value = '';
        const infoDiv = document.getElementById('selected-file-info');
        if (infoDiv) {
            infoDiv.style.display = 'inline-block';
            infoDiv.innerHTML = `<span style="color:#EF4444; font-weight:700;"><i class="fa-solid fa-shield-halved"></i> <strong>.docx files blocked:</strong> Prohibited due to malware security risks. Convert to PDF.</span>`;
        }
        showToast('Security Alert: .docx / Word files are blocked to prevent malware exploits. Please upload a PDF resume.', 'error');
        return;
    }

    // 2. Format Validation: Must be PDF
    if (!fileNameLower.endsWith('.pdf')) {
        selectedResumeFile = null;
        const fileInput = document.getElementById('resume-file-input');
        if (fileInput) fileInput.value = '';
        const infoDiv = document.getElementById('selected-file-info');
        if (infoDiv) {
            infoDiv.style.display = 'inline-block';
            infoDiv.innerHTML = `<span style="color:#EF4444; font-weight:700;"><i class="fa-solid fa-triangle-exclamation"></i> Only PDF format (.pdf) is supported.</span>`;
        }
        showToast('Invalid file format: Only standard PDF documents (.pdf) are accepted.', 'error');
        return;
    }

    selectedResumeFile = file;
    window.AppState.selectedSampleText = null; // Prioritize real uploaded file
    const infoDiv = document.getElementById('selected-file-info');
    if (infoDiv) {
        infoDiv.style.display = 'inline-block';
        infoDiv.innerHTML = `<i class="fa-solid fa-file-pdf text-danger"></i> Selected: <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB) <span class="badge badge-success ml-2" style="font-size:0.75rem;"><i class="fa-solid fa-shield-check"></i> PDF Verified</span>`;
    }
    showToast(`Loaded PDF: ${file.name}`, 'info');
}

async function submitResumeAnalysis() {
    if (!selectedResumeFile && !window.AppState.selectedSampleText) {
        showToast('Please select or drag-and-drop your Resume PDF file first.', 'error');
        return;
    }

    // Show loading spinner & hide old results / errors
    document.getElementById('analyzer-loading').style.display = 'block';
    document.getElementById('analyzer-results').style.display = 'none';
    const verifErrDiv = document.getElementById('analyzer-verification-error');
    if (verifErrDiv) verifErrDiv.style.display = 'none';

    try {
        let response;
        if (selectedResumeFile && !window.AppState.selectedSampleText) {
            const formData = new FormData();
            formData.append('resume_file', selectedResumeFile);
            response = await fetch('/api/resume/analyze', {
                method: 'POST',
                body: formData
            });
        } else if (window.AppState.selectedSampleText) {
            response = await fetch('/api/resume/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text: window.AppState.selectedSampleText })
            });
        } else {
            const formData = new FormData();
            formData.append('resume_file', selectedResumeFile);
            response = await fetch('/api/resume/analyze', {
                method: 'POST',
                body: formData
            });
        }

        const data = await response.json();
        document.getElementById('analyzer-loading').style.display = 'none';

        if (!response.ok || !data.success) {
            const errMsg = data.error || 'Failed to parse resume PDF. Please ensure your PDF is not password protected and contains readable text.';
            
            // Display structured verification rejection banner if non-resume document detected
            if (verifErrDiv) {
                verifErrDiv.style.display = 'block';
                const msgEl = document.getElementById('verif-error-msg');
                if (msgEl) msgEl.innerText = errMsg;

                verifErrDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            showToast(errMsg, 'error');
            return;
        }

        // Store in global state
        window.AppState.analyzedResumeText = data.raw_text_preview || '';
        window.AppState.analyzedSkills = data.extracted_skills;
        window.AppState.analyzedCertifications = data.extracted_certifications || [];
        window.AppState.generatedQuestions = data.interview_questions;

        // Render results UI
        renderAnalysisResults(data);
        if (typeof updateMockSkillsPreview === 'function') {
            updateMockSkillsPreview();
        }
        showToast('Resume verified & matched with 45-company dataset!', 'success');

    } catch (err) {
        document.getElementById('analyzer-loading').style.display = 'none';
        showToast('Network error while analyzing resume: ' + err.message, 'error');
    }
}

function renderAnalysisResults(data) {
    const resultsContainer = document.getElementById('analyzer-results');
    resultsContainer.style.display = 'block';

    // Show verified resume security badge
    const verifBadge = document.getElementById('resume-verified-badge');
    if (verifBadge) verifBadge.style.display = 'inline-flex';

    const ats = data.ats_analysis;

    // 1. ATS Score Gauge Animation
    animateGauge(ats.ats_score, ats.rating_color);
    document.getElementById('ats-rating-badge').innerText = `${ats.rating} (${ats.ats_score}/100)`;
    document.getElementById('ats-rating-badge').style.borderColor = ats.rating_color;
    document.getElementById('ats-rating-badge').style.color = ats.rating_color;
    document.getElementById('ats-feedback-text').innerText = ats.feedback_summary;

    // Metric counters
    document.getElementById('metric-word-count').innerText = ats.word_count;
    document.getElementById('metric-skills-count').innerText = data.total_skills_count;
    document.getElementById('metric-verbs-count').innerText = ats.action_verbs_found.length;
    document.getElementById('metric-metrics-count').innerText = ats.metrics_found_count;

    // 2. Section Completeness Checklist
    const checklistDiv = document.getElementById('section-checklist');
    checklistDiv.innerHTML = '';
    const sections = ats.section_breakdown.sections;
    for (const [secName, isPresent] of Object.entries(sections)) {
        const item = document.createElement('div');
        item.className = `check-item ${isPresent ? 'passed' : 'missing'}`;
        item.innerHTML = `<i class="fa-solid ${isPresent ? 'fa-circle-check' : 'fa-circle-xmark'}"></i> ${secName}`;
        checklistDiv.appendChild(item);
    }

    // Recommendations list
    const recList = document.getElementById('recommendation-list');
    recList.innerHTML = '';
    ats.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.innerText = rec;
        recList.appendChild(li);
    });

    // 3. Extracted Skills Taxonomy
    document.getElementById('skills-total-badge').innerText = `${data.total_skills_count} Skills Detected`;
    const skillsGrid = document.getElementById('skills-taxonomy-container');
    skillsGrid.innerHTML = '';

    const categoryIcons = {
        languages: 'fa-code',
        frameworks_libraries: 'fa-cubes',
        databases: 'fa-database',
        cloud_devops: 'fa-cloud',
        core_cs: 'fa-microchip',
        ai_ml_data: 'fa-brain',
        soft_skills: 'fa-comments'
    };

    const categoryNames = {
        languages: 'Programming Languages',
        frameworks_libraries: 'Frameworks & Libraries',
        databases: 'Databases & Storage',
        cloud_devops: 'Cloud, DevOps & Tools',
        core_cs: 'Core Computer Science',
        ai_ml_data: 'AI / ML & Data Science',
        soft_skills: 'Soft Skills & Leadership'
    };

    for (const [catKey, skillList] of Object.entries(data.extracted_skills)) {
        if (skillList.length === 0) continue;

        const block = document.createElement('div');
        block.className = 'skill-category-block';

        const title = document.createElement('div');
        title.className = 'skill-category-title';
        title.innerHTML = `<i class="fa-solid ${categoryIcons[catKey] || 'fa-tag'}"></i> ${categoryNames[catKey] || catKey} (${skillList.length})`;
        block.appendChild(title);

        const pillsWrap = document.createElement('div');
        pillsWrap.className = 'skill-pills-wrap';
        skillList.forEach(skill => {
            const pill = document.createElement('span');
            pill.className = 'skill-pill';
            pill.innerText = skill;
            pill.setAttribute('data-skill', skill);
            pill.setAttribute('title', `Click to filter 45-company matches for ${skill}`);
            pill.onclick = (e) => {
                e.stopPropagation();
                filterBySkill(skill);
            };
            pillsWrap.appendChild(pill);
        });

        block.appendChild(pillsWrap);
        skillsGrid.appendChild(block);
    }

    // 4. Career Role Recommendations
    const rolesGrid = document.getElementById('career-roles-container');
    rolesGrid.innerHTML = '';
    data.career_recommendations.slice(0, 6).forEach(role => {
        const card = document.createElement('div');
        card.className = 'career-role-card';
        card.innerHTML = `
            <div class="career-role-header">
                <h4>${role.role}</h4>
                <span class="match-pct-badge">${role.match_percentage}% Match</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: ${role.match_percentage}%"></div>
            </div>
            <p class="text-muted" style="font-size:0.84rem; margin-bottom:0.6rem;">${role.description}</p>
            <div style="font-size:0.8rem;">
                <strong class="text-success">Matched:</strong> ${role.matched_skills.slice(0, 4).join(', ') || 'Basic'}
                ${role.missing_skills.length ? `<br><strong class="text-warning">Missing:</strong> ${role.missing_skills.slice(0, 3).join(', ')}` : ''}
            </div>
        `;
        rolesGrid.appendChild(card);
    });

    // 4. 45-Company Hiring Dataset Matching & Benchmark
    if (data.cohort_benchmark) {
        const bm = data.cohort_benchmark;
        const headlineEl = document.getElementById('benchmark-headline');
        const subtextEl = document.getElementById('benchmark-subtext');
        
        if (headlineEl && subtextEl) {
            const topPct = Math.max(1, Math.round(100 - bm.percentile_rank));
            headlineEl.innerHTML = `<i class="fa-solid fa-trophy text-amber"></i> Top <strong>${topPct}%</strong> Candidate in 45-Company Recruitment Cohort`;
            if (bm.similar_candidate) {
                const sc = bm.similar_candidate;
                subtextEl.innerHTML = `Your resume profile aligns with <strong>${sc.name}</strong> (${sc.degree}) who was hired at <strong>${sc.employer}</strong> for <em>${sc.job_title}</em> (~${sc.indicative_ctc_lpa} LPA).`;
            } else {
                subtextEl.innerHTML = `Evaluated against ${bm.cohort_total} candidates with an average cohort ATS score of ${bm.cohort_avg_ats}%.`;
            }
        }
    }

    if (data.dataset_matching) {
        const allComps = data.dataset_matching.all_matches || [];
        window.AppState.allCompanyMatches = allComps;
        window.AppState.mixedCompanyList = createMixedDistribution(allComps);
        window.AppState.companyBatchIndex = 0;

        const countBadge = document.getElementById('dataset-evaluated-badge');
        if (countBadge) countBadge.innerText = `${data.dataset_matching.total_companies_evaluated} Recruiters Evaluated (15 per View)`;
        
        displayCurrentCompanyBatch();
    }

    // 5. Tailored Interview Questions Accordion
    const questionsContainer = document.getElementById('resume-questions-container');
    questionsContainer.innerHTML = '';
    data.interview_questions.forEach((q, idx) => {
        const qCard = document.createElement('div');
        qCard.className = 'question-card';
        qCard.innerHTML = `
            <div class="question-header" onclick="toggleQuestionBody(${idx})">
                <div class="question-title-wrap">
                    <span class="badge badge-primary">${q.type}</span>
                    <span>${q.question}</span>
                </div>
                <i class="fa-solid fa-chevron-down text-muted" id="q-icon-${idx}"></i>
            </div>
            <div class="question-body" id="q-body-${idx}">
                <div class="model-answer-badge"><i class="fa-solid fa-lightbulb"></i> Key Answering Points & Solution Concept</div>
                <p style="font-size:0.9rem; color:var(--text-secondary);">${q.model_answer}</p>
            </div>
        `;
        questionsContainer.appendChild(qCard);
    });

    // 6. Tailored Skill Mock Test Callout Banner Tags
    const mockCtaTags = document.getElementById('resume-mock-skills-tags');
    if (mockCtaTags) {
        mockCtaTags.innerHTML = '';
        const allSkills = [];
        for (const list of Object.values(data.extracted_skills || {})) {
            allSkills.push(...list);
        }
        allSkills.slice(0, 10).forEach(s => {
            const span = document.createElement('span');
            span.className = 'badge badge-primary';
            span.innerHTML = `<i class="fa-solid fa-code"></i> ${s}`;
            mockCtaTags.appendChild(span);
        });
        (data.extracted_certifications || []).forEach(c => {
            const span = document.createElement('span');
            span.className = 'badge badge-warning';
            span.innerHTML = `<i class="fa-solid fa-certificate"></i> ${c}`;
            mockCtaTags.appendChild(span);
        });
    }

    // Scroll smoothly to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Creates a balanced, mixed distribution of 45 companies across 3 batches of 15.
 * Interleaves Strong Matches, High CTC, Moderate Fits, and diverse industry domains.
 */
function createMixedDistribution(companies) {
    if (!companies || companies.length <= 15) return companies || [];

    const strongMatches = companies.filter(c => c.fit_tier === 'Strong Match');
    const moderateFits = companies.filter(c => c.fit_tier === 'Moderate Fit');
    const skillGaps = companies.filter(c => c.fit_tier === 'Skill Gap');

    const mixed = [];
    const pool = [...companies];

    // Interleave so that every slice of 15 has an exciting mix of matches
    const b1 = [], b2 = [], b3 = [];
    
    // Distribute strong matches evenly across the 3 batches
    strongMatches.forEach((c, idx) => {
        if (idx % 3 === 0) b1.push(c);
        else if (idx % 3 === 1) b2.push(c);
        else b3.push(c);
    });

    // Distribute moderate fits evenly
    moderateFits.forEach((c, idx) => {
        if (idx % 3 === 0) b1.push(c);
        else if (idx % 3 === 1) b2.push(c);
        else b3.push(c);
    });

    // Distribute remaining companies
    skillGaps.forEach((c, idx) => {
        if (idx % 3 === 0) b1.push(c);
        else if (idx % 3 === 1) b2.push(c);
        else b3.push(c);
    });

    // Pad each batch to exactly 15 if needed
    const batches = [b1, b2, b3];
    return [...b1, ...b2, ...b3];
}

function displayCurrentCompanyBatch() {
    const list = window.AppState.mixedCompanyList || window.AppState.allCompanyMatches || [];
    const batchIndex = window.AppState.companyBatchIndex || 0;
    const batchSize = 15;
    
    const start = batchIndex * batchSize;
    const current15 = list.slice(start, start + batchSize);

    const countEl = document.getElementById('company-matches-count');
    if (countEl) {
        countEl.innerHTML = `Showing <strong>${current15.length}</strong> of <strong>${list.length}</strong> Recruiters &bull; <span class="badge badge-primary" style="font-size:0.75rem;">Batch ${batchIndex + 1} of 3</span>`;
    }

    const indicatorEl = document.getElementById('company-batch-indicator');
    if (indicatorEl) {
        indicatorEl.innerHTML = `<i class="fa-solid fa-layer-group text-primary"></i> Batch ${batchIndex + 1} of 3 &bull; Showing ${current15.length} of ${list.length} Recruiters`;
    }

    renderCompanyMatches(current15);
}

function refreshCompanyMatches() {
    const list = window.AppState.mixedCompanyList || window.AppState.allCompanyMatches || [];
    if (!list || list.length === 0) return;

    // Cycle to next batch (0 -> 1 -> 2 -> 0)
    const nextBatch = ((window.AppState.companyBatchIndex || 0) + 1) % 3;
    window.AppState.companyBatchIndex = nextBatch;

    const btnBottom = document.getElementById('btn-refresh-companies-bottom');
    if (btnBottom) btnBottom.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin"></i> Loading Next 15 Companies...';

    setTimeout(() => {
        if (btnBottom) btnBottom.innerHTML = '<i class="fa-solid fa-arrows-rotate"></i> Refresh & Load Next 15 Companies';
    }, 350);

    displayCurrentCompanyBatch();
    showToast(`Loaded Batch ${nextBatch + 1} of 3 (15 mixed recruiter results)`, 'info');
}

function renderCompanyMatches(matches) {
    const container = document.getElementById('company-matches-container');
    if (!container) return;

    container.innerHTML = '';
    if (!matches || matches.length === 0) {
        container.innerHTML = '<div class="text-center text-muted p-4" style="grid-column:1/-1;">No companies match the selected filter.</div>';
        return;
    }

    matches.slice(0, 15).forEach(comp => {
        const card = document.createElement('div');
        card.className = 'company-match-card';
        
        const badgeStyle = comp.fit_tier === 'Strong Match' ? 'badge-success' :
                           comp.fit_tier === 'Moderate Fit' ? 'badge-primary' : 'badge-warning';

        card.innerHTML = `
            <div class="company-match-header">
                <div>
                    <h4 class="company-name">${comp.company}</h4>
                    <span class="company-role-title">${comp.role}</span>
                </div>
                <div class="match-score-badge-wrap">
                    <span class="badge ${badgeStyle}">${comp.fit_tier}</span>
                    <div class="match-score-num">${comp.match_score}%</div>
                </div>
            </div>

            <div class="progress-bar-bg" style="margin: 0.6rem 0;">
                <div class="progress-bar-fill" style="width: ${comp.match_score}%; background: ${comp.match_score >= 75 ? 'var(--success)' : comp.match_score >= 50 ? 'var(--primary)' : 'var(--warning)'};"></div>
            </div>

            <div class="company-ctc-row">
                <span><i class="fa-solid fa-indian-rupee-sign text-success"></i> Indicative CTC: <strong>${comp.indicative_ctc_range_lpa} LPA</strong></span>
                <span class="text-muted" style="font-size:0.78rem;"><code>${comp.job_id}</code></span>
            </div>

            <div class="company-skills-breakdown mt-2">
                <div style="font-size:0.8rem; margin-bottom:0.25rem;">
                    <strong class="text-success"><i class="fa-solid fa-circle-check"></i> Matched:</strong>
                    ${comp.matched_skills.length ? comp.matched_skills.map(s => `<span class="skill-mini-pill matched" onclick="filterBySkill('${s}')" title="Filter by ${s}">${s}</span>`).join('') : '<span class="text-muted" style="font-size:0.75rem;">None</span>'}
                </div>
                ${comp.missing_skills.length ? `
                <div style="font-size:0.8rem;">
                    <strong class="text-warning"><i class="fa-solid fa-circle-xmark"></i> Missing:</strong>
                    ${comp.missing_skills.map(s => `<span class="skill-mini-pill missing" onclick="filterBySkill('${s}')" title="Filter by ${s}">${s}</span>`).join('')}
                </div>` : ''}
            </div>
        `;
        container.appendChild(card);
    });
}

let currentActiveSkillFilter = null;

function filterBySkill(skillName) {
    if (!skillName) return;
    const cleanSkill = skillName.trim();
    const searchInput = document.getElementById('company-match-search');
    const targetSection = document.querySelector('.dataset-matching-card') || document.getElementById('company-matches-container');

    if (currentActiveSkillFilter && currentActiveSkillFilter.toLowerCase() === cleanSkill.toLowerCase()) {
        clearSkillFilter();
        return;
    }

    currentActiveSkillFilter = cleanSkill;
    if (searchInput) searchInput.value = cleanSkill;

    // Highlight all matching pills across the page
    updateSkillPillHighlights(cleanSkill);

    // Apply the filter across the 45 companies
    filterCompanyMatches();

    // Smooth scroll to the 45-company recruiter fit section
    if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    showToast(`Filtering 45-company recruiters for "${cleanSkill}"`, 'success');
}

function clearSkillFilter() {
    currentActiveSkillFilter = null;
    const searchInput = document.getElementById('company-match-search');
    if (searchInput) searchInput.value = '';
    
    updateSkillPillHighlights(null);
    displayCurrentCompanyBatch();
    showToast('Cleared skill filter. Showing all recruiter matches.', 'info');
}

function updateSkillPillHighlights(skillName) {
    const clean = skillName ? skillName.toLowerCase() : null;
    document.querySelectorAll('.skill-pill').forEach(p => {
        const text = p.getAttribute('data-skill') || p.innerText.trim();
        p.classList.toggle('active-skill-filter', clean !== null && text.toLowerCase() === clean);
    });
    document.querySelectorAll('.skill-mini-pill').forEach(p => {
        const text = p.innerText.trim();
        p.classList.toggle('active-skill-filter', clean !== null && text.toLowerCase() === clean);
    });
}

function filterCompanyMatches() {
    const search = document.getElementById('company-match-search')?.value.toLowerCase().trim() || '';
    const tier = document.getElementById('company-tier-filter')?.value || 'all';

    // Update active highlight if user typed in search input
    if (search !== currentActiveSkillFilter?.toLowerCase()) {
        currentActiveSkillFilter = search || null;
        updateSkillPillHighlights(search || null);
    }

    // When searching/filtering, search across all 45 companies
    const allMatches = window.AppState.allCompanyMatches || [];
    const filtered = allMatches.filter(comp => {
        const matchesSearch = !search || 
                              comp.company.toLowerCase().includes(search) || 
                              comp.role.toLowerCase().includes(search) || 
                              comp.required_skills.some(s => s.toLowerCase().includes(search) || search.includes(s.toLowerCase())) ||
                              comp.matched_skills.some(s => s.toLowerCase().includes(search) || search.includes(s.toLowerCase()));

        const matchesTier = tier === 'all' || comp.fit_tier === tier;

        return matchesSearch && matchesTier;
    });

    const countEl = document.getElementById('company-matches-count');
    if (countEl) {
        if (search) {
            countEl.innerHTML = `Filtered by: <strong class="text-primary">"${search}"</strong> (${filtered.length} found) &bull; <button class="btn btn-outline btn-sm" onclick="clearSkillFilter()" style="padding:0.15rem 0.6rem; font-size:0.75rem; border-radius:12px; margin-left:0.35rem;"><i class="fa-solid fa-xmark"></i> Clear Filter</button>`;
        } else {
            countEl.innerHTML = `Showing <strong>${Math.min(15, filtered.length)}</strong> of <strong>${filtered.length}</strong> matching companies`;
        }
    }

    renderCompanyMatches(filtered.slice(0, 15));
}

function animateGauge(targetScore, color) {
    const progressEl = document.getElementById('ats-gauge');
    const valueEl = document.getElementById('ats-gauge-num');

    let current = 0;
    const speed = 15;
    const timer = setInterval(() => {
        current += 1;
        valueEl.innerText = `${current}%`;
        progressEl.style.background = `conic-gradient(${color || '#6366F1'} ${current * 3.6}deg, var(--border-color) 0deg)`;

        if (current >= targetScore) {
            clearInterval(timer);
            valueEl.innerText = `${targetScore}%`;
        }
    }, speed);
}

function toggleQuestionBody(idx) {
    const body = document.getElementById(`q-body-${idx}`);
    const icon = document.getElementById(`q-icon-${idx}`);
    if (body) {
        body.classList.toggle('open');
        if (icon) {
            icon.classList.toggle('fa-chevron-up');
            icon.classList.toggle('fa-chevron-down');
        }
    }
}

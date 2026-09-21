/**
 * AI Career Companion - Resume-Job Matcher & Skill Gap Analyzer (Module 2)
 */

let cachedJobProfiles = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchJobProfiles();
});

async function fetchJobProfiles() {
    try {
        const res = await fetch('/api/jobs');
        const data = await res.json();
        if (data.success) {
            cachedJobProfiles = data.jobs;
        }
    } catch (err) {
        console.warn('Error fetching jobs:', err);
    }
}

function syncResumeFromAnalyzer() {
    const analyzedText = window.AppState.analyzedResumeText;
    const matcherTextarea = document.getElementById('matcher-resume-text');

    if (analyzedText && matcherTextarea) {
        matcherTextarea.value = analyzedText;
        showToast('Successfully synchronized resume from Analyzer!', 'success');
    } else {
        // Check if raw text area in module 1 has content
        const rawText = document.getElementById('resume-raw-text').value;
        if (rawText && matcherTextarea) {
            matcherTextarea.value = rawText;
            showToast('Synchronized text from Module 1!', 'success');
        } else {
            showToast('No analyzed resume found. Please paste your resume or analyze it in Module 1 first.', 'info');
        }
    }
}

function loadPresetJobDescription() {
    const selectEl = document.getElementById('preset-job-dropdown');
    const selectedId = selectEl.value;
    const jdTextarea = document.getElementById('matcher-jd-text');

    if (!selectedId) return;

    const job = cachedJobProfiles.find(j => j.id == selectedId);
    if (job && jdTextarea) {
        jdTextarea.value = `Company: ${job.company}
Role: ${job.role_title}
Experience: ${job.experience_level} | Location: ${job.location} | CTC: ${job.ctc_range}

Required Skills:
${job.required_skills}

Job Description & Responsibilities:
${job.description}`;
        showToast(`Loaded JD for ${job.company} - ${job.role_title}`, 'info');
    }
}

async function submitJobMatching() {
    const resumeText = document.getElementById('matcher-resume-text').value.trim();
    const jdText = document.getElementById('matcher-jd-text').value.trim();

    if (!resumeText) {
        showToast('Please paste or sync your resume first.', 'error');
        return;
    }

    if (!jdText) {
        showToast('Please select a target company JD or paste a custom job description.', 'error');
        return;
    }

    const matchBtn = document.getElementById('btn-match-jd');
    matchBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Calculating Match & Gaps...';
    matchBtn.disabled = true;

    try {
        const response = await fetch('/api/resume/match-job', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: resumeText, jd_text: jdText })
        });

        const data = await response.json();
        matchBtn.innerHTML = '<i class="fa-solid fa-crosshairs"></i> Run Resume–Job Matching Engine';
        matchBtn.disabled = false;

        if (!response.ok || !data.success) {
            showToast(data.error || 'Failed to match job description.', 'error');
            return;
        }

        renderMatchingResults(data.match_result);
        showToast('Job matching & gap analysis complete!', 'success');

    } catch (err) {
        matchBtn.innerHTML = '<i class="fa-solid fa-crosshairs"></i> Run Resume–Job Matching Engine';
        matchBtn.disabled = false;
        showToast('Network error during matching: ' + err.message, 'error');
    }
}

function renderMatchingResults(result) {
    const container = document.getElementById('matcher-results');
    container.style.display = 'block';

    // 1. Overall Score & Progress Bar
    document.getElementById('match-score-num').innerText = `${result.match_score}%`;
    const progressBar = document.getElementById('match-progress-bar');
    progressBar.style.width = `${result.match_score}%`;

    const badge = document.getElementById('match-readiness-badge');
    badge.innerText = result.readiness_badge;
    badge.style.color = result.readiness_color;
    badge.style.borderColor = result.readiness_color;

    // 2. Matched Skills Pills
    document.getElementById('matched-skills-count').innerText = result.matched_skills.length;
    const matchedPillsWrap = document.getElementById('matched-skills-pills');
    matchedPillsWrap.innerHTML = '';
    if (result.matched_skills.length === 0) {
        matchedPillsWrap.innerHTML = '<span class="text-muted" style="font-size:0.88rem;">No direct matching keywords detected.</span>';
    } else {
        result.matched_skills.forEach(skill => {
            const pill = document.createElement('span');
            pill.className = 'skill-pill skill-pill-matched';
            pill.innerHTML = `<i class="fa-solid fa-check"></i> ${skill}`;
            matchedPillsWrap.appendChild(pill);
        });
    }

    // 3. Missing Critical Skills Pills
    document.getElementById('missing-skills-count').innerText = result.missing_skills.length;
    const missingPillsWrap = document.getElementById('missing-skills-pills');
    missingPillsWrap.innerHTML = '';
    if (result.missing_skills.length === 0) {
        missingPillsWrap.innerHTML = '<span class="text-success" style="font-size:0.88rem;"><i class="fa-solid fa-circle-check"></i> Outstanding! Your resume covers all core required skills.</span>';
    } else {
        result.missing_skills.forEach(skill => {
            const pill = document.createElement('span');
            pill.className = 'skill-pill skill-pill-missing';
            pill.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${skill}`;
            missingPillsWrap.appendChild(pill);
        });
    }

    // 4. Personalized 4-Week Learning Roadmap
    const timelineContainer = document.getElementById('roadmap-timeline-container');
    timelineContainer.innerHTML = '';

    result.roadmap.forEach(weekItem => {
        const card = document.createElement('div');
        card.className = 'timeline-card';
        card.innerHTML = `
            <div class="timeline-week">${weekItem.week}</div>
            <div class="timeline-title">${weekItem.title}</div>
            <ul class="timeline-tasks">
                ${weekItem.tasks.map(t => `<li>${t}</li>`).join('')}
            </ul>
            <div class="mt-2" style="font-size:0.78rem; color:var(--text-muted);">
                <strong>Resources:</strong> ${weekItem.resources.join(', ')}
            </div>
        `;
        timelineContainer.appendChild(card);
    });

    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

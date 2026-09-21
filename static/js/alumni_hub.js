/**
 * AI Career Companion - Alumni Experience Portal (Module 4)
 */

let alumniSearchTimeout = null;

async function fetchAlumniExperiences() {
    const company = document.getElementById('alumni-company-filter')?.value || 'all';
    const difficulty = document.getElementById('alumni-difficulty-filter')?.value || 'all';
    const search = document.getElementById('alumni-search-input')?.value.trim() || '';

    const feed = document.getElementById('alumni-feed-container');
    if (!feed) return;

    feed.innerHTML = '<div class="text-center p-4"><div class="spinner"></div><p>Loading authentic placement stories...</p></div>';

    try {
        const queryParams = new URLSearchParams({
            company: company,
            difficulty: difficulty,
            search: search
        });

        const res = await fetch(`/api/alumni/experiences?${queryParams.toString()}`);
        const data = await res.json();

        if (!data.success || !data.experiences || data.experiences.length === 0) {
            feed.innerHTML = `
                <div class="card text-center p-5 empty-alumni-card" style="grid-column: 1 / -1; max-width: 600px; margin: 0 auto;">
                    <div style="width:70px; height:70px; border-radius:50%; background:rgba(99,102,241,0.1); color:var(--primary); display:flex; align-items:center; justify-content:center; font-size:2rem; margin:0 auto 1.25rem;">
                        <i class="fa-solid fa-user-graduate"></i>
                    </div>
                    <h3>No Alumni Stories Found</h3>
                    <p class="text-muted" style="max-width:500px; margin:0.5rem auto 1.5rem;">
                        No placement records matched your selected search criteria. Try adjusting company or difficulty filters.
                    </p>
                </div>
            `;
            return;
        }

        populateCompanyFilterOptions(data.experiences);
        renderAlumniExperiences(data.experiences);

    } catch (err) {
        feed.innerHTML = `<div class="card p-4 text-danger">Error loading experiences: ${err.message}</div>`;
    }
}

function populateCompanyFilterOptions(experiences) {
    const compSelect = document.getElementById('alumni-company-filter');
    if (!compSelect || compSelect.dataset.populated) return;

    const currentVal = compSelect.value;
    const companies = new Set();
    experiences.forEach(e => {
        if (e.company) companies.add(e.company);
    });

    compSelect.innerHTML = '<option value="all">All Companies</option>';
    Array.from(companies).sort().forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.innerText = c;
        compSelect.appendChild(opt);
    });
    compSelect.value = currentVal;
    compSelect.dataset.populated = 'true';
}

function debounceAlumniSearch() {
    if (alumniSearchTimeout) clearTimeout(alumniSearchTimeout);
    alumniSearchTimeout = setTimeout(() => {
        fetchAlumniExperiences();
    }, 350);
}

function getInitials(name) {
    if (!name) return 'AL';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
}

function renderAlumniExperiences(experiences) {
    window.AppState.allAlumniExperiences = experiences;
    const feed = document.getElementById('alumni-feed-container');
    if (!feed) return;
    feed.innerHTML = '';

    experiences.forEach(exp => {
        const card = document.createElement('div');
        card.className = 'alumni-card alumni-card-compact';
        card.onclick = () => openAlumniDetail(exp.id);

        const difficultyColor = exp.difficulty === 'Hard' ? 'badge-danger' : exp.difficulty === 'Medium' ? 'badge-warning' : 'badge-success';
        const seniorEmail = exp.email || `${exp.student_name.toLowerCase().replace(/\s+/g, '.')}@gmail.com`;
        const initials = getInitials(exp.student_name);
        const roundsCount = exp.rounds ? exp.rounds.length : 3;

        card.innerHTML = `
            <div class="alumni-compact-top">
                <div class="alumni-compact-avatar">${initials}</div>
                <div class="alumni-compact-student">
                    <h3 class="alumni-compact-name">${exp.student_name}</h3>
                    <span class="alumni-compact-batch">Batch of ${exp.batch_year}</span>
                </div>
                <span class="badge ${difficultyColor} alumni-compact-diff">${exp.difficulty}</span>
            </div>

            <div class="alumni-compact-body">
                <div class="alumni-compact-company-row">
                    <span class="alumni-compact-company"><i class="fa-solid fa-building text-primary"></i> ${exp.company}</span>
                    <span class="alumni-compact-ctc">₹${exp.package_lpa} LPA</span>
                </div>
                <div class="alumni-compact-role">${exp.role}</div>
                
                <div class="alumni-compact-meta">
                    <span class="alumni-compact-rounds"><i class="fa-solid fa-list-check"></i> ${roundsCount} Rounds</span>
                    <span class="alumni-compact-status"><i class="fa-solid fa-circle-check text-success"></i> ${exp.status}</span>
                </div>
            </div>

            <div class="alumni-compact-footer">
                <button class="btn btn-sm btn-outline alumni-compact-view-btn" onclick="event.stopPropagation(); openAlumniDetail(${exp.id})">
                    <i class="fa-solid fa-expand"></i> View Details
                </button>
                <a href="https://www.linkedin.com/search/results/all/?keywords=${encodeURIComponent(exp.student_name + ' ' + exp.company)}" target="_blank" rel="noopener noreferrer" class="btn-linkedin-contact-sm" title="Find on LinkedIn" onclick="event.stopPropagation(); trackLinkedInOutreach('${encodeURIComponent(exp.student_name)}', '${encodeURIComponent(exp.company)}', '${encodeURIComponent(seniorEmail)}')">
                    <i class="fa-brands fa-linkedin"></i> LinkedIn
                </a>
                <button class="btn-gmail-contact-sm" title="Contact Senior via Gmail" onclick="event.stopPropagation(); contactSeniorViaGmail('${encodeURIComponent(seniorEmail)}', '${encodeURIComponent(exp.student_name)}', '${encodeURIComponent(exp.company)}', '${encodeURIComponent(exp.role)}')">
                    <i class="fa-brands fa-google"></i> Gmail
                </button>
            </div>
        `;

        feed.appendChild(card);
    });
}

function openAlumniDetail(expId) {
    const experiences = window.AppState.allAlumniExperiences || [];
    const exp = experiences.find(e => String(e.id) === String(expId));
    if (!exp) return;

    const modal = document.getElementById('alumni-detail-modal');
    const avatarEl = document.getElementById('alumni-detail-avatar');
    const nameEl = document.getElementById('alumni-detail-name');
    const statusEl = document.getElementById('alumni-detail-status');
    const subtitleEl = document.getElementById('alumni-detail-subtitle');
    const bodyEl = document.getElementById('alumni-detail-body');
    const upvoteCountEl = document.getElementById('alumni-detail-upvote-count');
    const upvoteBtnEl = document.getElementById('alumni-detail-upvote-btn');
    const gmailBtnEl = document.getElementById('alumni-detail-gmail-btn');

    if (!modal) return;

    const initials = getInitials(exp.student_name);
    const difficultyColor = exp.difficulty === 'Hard' ? 'badge-danger' : exp.difficulty === 'Medium' ? 'badge-warning' : 'badge-success';
    const seniorEmail = exp.email || `${exp.student_name.toLowerCase().replace(/\s+/g, '.')}@gmail.com`;

    if (avatarEl) avatarEl.innerText = initials;
    if (nameEl) nameEl.innerText = exp.student_name;
    if (statusEl) {
        statusEl.innerText = exp.status || 'Selected';
        statusEl.className = 'badge badge-success';
    }
    if (subtitleEl) {
        subtitleEl.innerText = `Batch of ${exp.batch_year} • ${exp.offer_type || 'On-Campus Placement'}`;
    }

    let roundsHtml = '';
    if (exp.rounds && exp.rounds.length > 0) {
        roundsHtml = `
            <div class="alumni-section-title"><i class="fa-solid fa-list-ol"></i> Round-by-Round Interview Breakdown:</div>
            <ul class="rounds-timeline-list">
                ${exp.rounds.map(r => `
                    <li class="round-timeline-step">
                        <div class="round-name">${r.round_name || 'Interview Round'}</div>
                        <div class="round-desc">${r.details || ''}</div>
                    </li>
                `).join('')}
            </ul>
        `;
    }

    bodyEl.innerHTML = `
        <div class="alumni-badges-row mb-3">
            <span class="badge badge-primary"><i class="fa-solid fa-building"></i> ${exp.company}</span>
            <span class="badge badge-outline"><i class="fa-solid fa-user-tie"></i> ${exp.role}</span>
            <span class="ctc-badge">₹${exp.package_lpa} LPA Package</span>
            <span class="badge ${difficultyColor}">${exp.difficulty} Interview</span>
        </div>

        <div class="alumni-email-tag mb-3" style="display:inline-flex;">
            <i class="fa-solid fa-envelope"></i> ${seniorEmail}
        </div>

        ${roundsHtml}

        <div class="alumni-section-title mt-3"><i class="fa-solid fa-book-bookmark"></i> Preparation Strategy & Resources:</div>
        <p style="font-size:0.92rem; color:var(--text-secondary); line-height:1.6;">${exp.preparation_tips || 'Consistent practice on Core CS and coding challenges.'}</p>

        ${exp.advice_to_juniors ? `
            <div class="alumni-section-title mt-3"><i class="fa-solid fa-comment-dots"></i> Advice to Junior Students:</div>
            <div class="alumni-quote" style="font-size:0.95rem; line-height:1.5;">"${exp.advice_to_juniors}"</div>
        ` : ''}
    `;

    if (upvoteCountEl) upvoteCountEl.innerText = exp.upvotes || 0;
    if (upvoteBtnEl) {
        upvoteBtnEl.onclick = () => upvoteExperience(exp.id, upvoteBtnEl);
        upvoteBtnEl.disabled = false;
        upvoteBtnEl.style.color = 'var(--text-primary)';
    }

    const linkedinBtnEl = document.getElementById('alumni-detail-linkedin-btn');
    if (linkedinBtnEl) {
        linkedinBtnEl.href = `https://www.linkedin.com/search/results/all/?keywords=${encodeURIComponent(exp.student_name + ' ' + exp.company)}`;
        linkedinBtnEl.onclick = () => trackLinkedInOutreach(encodeURIComponent(exp.student_name), encodeURIComponent(exp.company), encodeURIComponent(seniorEmail));
    }

    if (gmailBtnEl) {
        gmailBtnEl.onclick = () => contactSeniorViaGmail(
            encodeURIComponent(seniorEmail),
            encodeURIComponent(exp.student_name),
            encodeURIComponent(exp.company),
            encodeURIComponent(exp.role)
        );
    }

    modal.classList.add('active');
}

function closeAlumniDetailModal(e) {
    if (e && e.target && e.target !== e.currentTarget && !e.target.classList.contains('modal-close')) {
        return;
    }
    const modal = document.getElementById('alumni-detail-modal');
    if (modal) modal.classList.remove('active');
}

// Close on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('alumni-detail-modal');
        if (modal && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    }
});

/**
 * Directly opens Gmail Web Compose in a new tab with prefilled recipient,
 * subject line, and a polite placement mentorship request message.
 */
function contactSeniorViaGmail(email, name, company, role) {
    const decodedEmail = decodeURIComponent(email || 'alumni.contact@gmail.com');
    const decodedName = decodeURIComponent(name || 'Senior');
    const decodedCompany = decodeURIComponent(company || 'Target Company');
    const decodedRole = decodeURIComponent(role || 'Software Engineer');

    const subject = `Placement Guidance Request - ${decodedCompany} (${decodedRole})`;
    const body = `Hi ${decodedName},

I hope this email finds you well!

I came across your placement experience for ${decodedCompany} (${decodedRole}) on the AI Career Companion portal. Your journey and preparation tips were very inspiring.

As a junior student preparing for upcoming campus recruitment drives, I would love to connect with you to ask a few quick questions regarding preparation resources, coding rounds, and interview tips.

Thank you so much for taking out time to guide juniors!

Best regards,
[Your Name]
[Your Branch & College]`;

    // Direct Google Mail web compose URL
    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(decodedEmail)}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    // Track outreach interaction for Alumni Analytics
    fetch('/api/alumni/track-outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            alumni_id: decodedEmail,
            alumni_email: decodedEmail,
            alumni_name: decodedName,
            channel: 'gmail',
            student_name: window.AppState?.currentUser?.name || 'Junior Student',
            student_email: window.AppState?.currentUser?.email || 'student@itm.ac.in',
            target_company: decodedCompany,
            query_topic: `Mentorship request for ${decodedCompany} (${decodedRole})`
        })
    }).catch(e => console.log('Track outreach:', e));

    window.open(gmailUrl, '_blank', 'noopener,noreferrer');
    showToast(`Redirecting to Gmail to contact ${decodedName}...`, 'info');
}

function trackLinkedInOutreach(seniorName, company, seniorEmail) {
    const decodedName = decodeURIComponent(seniorName || 'Senior');
    const decodedCompany = decodeURIComponent(company || 'Company');
    const decodedEmail = decodeURIComponent(seniorEmail || '');

    fetch('/api/alumni/track-outreach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            alumni_id: decodedEmail || decodedName,
            alumni_email: decodedEmail,
            alumni_name: decodedName,
            channel: 'linkedin',
            student_name: window.AppState?.currentUser?.name || 'Junior Student',
            student_email: window.AppState?.currentUser?.email || 'student@itm.ac.in',
            target_company: decodedCompany || 'Company',
            query_topic: `LinkedIn networking & profile connection for ${decodedCompany}`
        })
    }).catch(e => console.log('Track linkedin outreach:', e));
}

async function upvoteExperience(expId, btn) {
    try {
        const res = await fetch(`/api/alumni/upvote/${expId}`, { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            const countEl = (btn && (btn.querySelector('#alumni-detail-upvote-count') || btn.querySelector('.upvote-count') || btn.querySelector('span'))) || document.getElementById('alumni-detail-upvote-count');
            if (countEl) {
                const currentVal = parseInt(countEl.innerText) || 0;
                countEl.innerText = (data.upvotes !== undefined) ? data.upvotes : (currentVal + 1);
            }
            if (btn) {
                btn.style.color = '#ef4444';
                btn.classList.add('upvoted');
                btn.disabled = true;
            }
            showToast('❤️ Thank you! Your upvote has been recorded.', 'success');
        } else {
            showToast(data.error || 'Failed to record upvote.', 'error');
        }
    } catch (err) {
        showToast('Upvote failed: ' + err.message, 'error');
    }
}

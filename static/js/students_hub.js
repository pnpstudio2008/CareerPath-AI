/**
 * AI Career Companion - Ongoing Student Profiles & Placement Tracking (Module 4)
 */

let studentSearchTimeout = null;

async function fetchStudentProfiles() {
    const search = document.getElementById('student-search-input')?.value.trim() || '';
    const branch = document.getElementById('student-branch-filter')?.value || 'all';
    const status = document.getElementById('student-status-filter')?.value || 'all';

    const feed = document.getElementById('students-feed-container');
    if (!feed) return;

    feed.innerHTML = '<div class="text-center p-5"><div class="spinner"></div><p class="mt-2 text-muted">Loading verified student profiles</p></div>';

    try {
        const queryParams = new URLSearchParams({
            search: search,
            branch: branch,
            status: status
        });

        const res = await fetch('/api/students?' + queryParams.toString());
        const data = await res.json();

        if (!data.success || !data.students || data.students.length === 0) {
            feed.innerHTML = `
                <div class="card text-center p-5 empty-student-card" style="grid-column: 1 / -1;">
                    <div style="width:70px; height:70px; border-radius:50%; background:rgba(99,102,241,0.1); color:var(--primary); display:flex; align-items:center; justify-content:center; font-size:2rem; margin:0 auto 1.25rem;">
                        <i class="fa-solid fa-user-graduate"></i>
                    </div>
                    <h3>No Student Records Found</h3>
                    <p class="text-muted" style="max-width:500px; margin:0.5rem auto 1.5rem;">
                        No student profiles match your current search/filter criteria. Placement administrators can create and manage new ongoing students from the Admin Portal.
                    </p>
                    <div>
                        <a href="/admin" target="_blank" class="btn btn-primary">
                            <i class="fa-solid fa-plus-circle"></i> Open Admin Portal
                        </a>
                    </div>
                </div>
            `;
            return;
        }

        window.AppState.allStudentProfiles = data.students;
        renderStudentProfiles(data.students);

    } catch (err) {
        feed.innerHTML = '<div class="card p-4 text-danger" style="grid-column: 1 / -1;">Error loading student profiles: ' + err.message + '</div>';
    }
}

function debounceStudentSearch() {
    if (studentSearchTimeout) clearTimeout(studentSearchTimeout);
    studentSearchTimeout = setTimeout(() => {
        fetchStudentProfiles();
    }, 300);
}

function getStudentInitials(name) {
    if (!name) return 'ST';
    const parts = name.trim().split(' ');
    if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
    return name.slice(0, 2).toUpperCase();
}

function renderStudentProfiles(students) {
    const feed = document.getElementById('students-feed-container');
    if (!feed) return;
    feed.innerHTML = '';

    students.forEach(st => {
        const card = document.createElement('div');
        card.className = 'student-profile-card';
        card.onclick = () => openStudentProfile(st.id);

        const initials = getStudentInitials(st.name);
        const atsScore = Math.round(st.ats_score || 0);

        let statusBadge = '';
        if (st.placement_status === 'Placed') {
            statusBadge = '<span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> Placed (' + (st.placed_company || 'Selected') + ')</span>';
        } else if (st.readiness_status === 'Ready') {
            statusBadge = '<span class="badge badge-primary"><i class="fa-solid fa-star"></i> Placement Ready</span>';
        } else if (st.readiness_status === 'In Progress') {
            statusBadge = '<span class="badge badge-warning"><i class="fa-solid fa-clock-rotate-left"></i> In Progress</span>';
        } else {
            statusBadge = '<span class="badge badge-outline"><i class="fa-solid fa-book-open-reader"></i> ' + (st.placement_status || 'Ongoing') + '</span>';
        }

        const email = st.email || (st.name.toLowerCase().replace(/\s+/g, '.') + '@itm.ac.in');

        card.innerHTML = `
            <div class="student-card-header">
                <div class="student-avatar-circle">${initials}</div>
                <div class="student-header-info">
                    <h3 class="student-name">${st.name}</h3>
                    <span class="student-roll"><i class="fa-solid fa-id-card"></i> ${st.roll_no || 'Roll N/A'}</span>
                </div>
                <div class="student-ats-circle" title="ATS Resume Score">
                    <span class="ats-val">${atsScore}%</span>
                    <span class="ats-lbl">ATS</span>
                </div>
            </div>

            <div class="student-card-details">
                <div class="student-detail-row">
                    <span class="detail-label"><i class="fa-solid fa-graduation-cap"></i> Branch:</span>
                    <span class="detail-val">${st.branch || 'Computer Science'}</span>
                </div>
                <div class="student-detail-row">
                    <span class="detail-label"><i class="fa-solid fa-calendar-days"></i> Batch:</span>
                    <span class="detail-val">Class of ${st.batch_year || '2025'}</span>
                </div>
                <div class="student-detail-row">
                    <span class="detail-label"><i class="fa-solid fa-bullseye"></i> Target:</span>
                    <span class="detail-val text-primary font-weight-bold">${st.target_company || 'General / Tech'}</span>
                </div>
+               ((st.package_lpa > 0) ? `
                <div class="student-detail-row">
                    <span class="detail-label"><i class="fa-solid fa-sack-dollar"></i> Offered CTC:</span>
                    <span class="detail-val text-success font-weight-bold">₹${st.package_lpa} LPA</span>
                </div>` : '') +
`
            </div>

            <div class="student-card-footer">
                <div class="student-status-wrap">
                    ${statusBadge}
                </div>
                <div class="student-actions-wrap">
                    <button class="btn btn-sm btn-outline student-view-btn" onclick="event.stopPropagation(); openStudentProfile(${st.id})">
                        <i class="fa-solid fa-expand"></i> Profile
                    </button>
                    <button class="btn-gmail-contact-sm" title="Contact Student via Gmail" onclick="event.stopPropagation(); contactStudentViaGmail('${encodeURIComponent(email)}', '${encodeURIComponent(st.name)}')">
                        <i class="fa-brands fa-google"></i>
                    </button>
                </div>
            </div>
        `;
        feed.appendChild(card);
    });
}

function openStudentProfile(studentId) {
    const students = window.AppState.allStudentProfiles || [];
    const st = students.find(s => String(s.id) === String(studentId));
    if (!st) return;

    const modal = document.getElementById('student-profile-modal');
    if (!modal) return;

    const initials = getStudentInitials(st.name);
    const atsScore = Math.round(st.ats_score || 0);
    const email = st.email || (st.name.toLowerCase().replace(/\s+/g, '.') + '@itm.ac.in');

    const avatarEl = document.getElementById('student-modal-avatar');
    const nameEl = document.getElementById('student-modal-name');
    const subtitleEl = document.getElementById('student-modal-subtitle');
    const bodyEl = document.getElementById('student-modal-body');
    const gmailBtn = document.getElementById('student-modal-gmail-btn');

    if (avatarEl) avatarEl.innerText = initials;
    if (nameEl) nameEl.innerText = st.name;
    if (subtitleEl) {
        subtitleEl.innerText = 'Roll No: ' + (st.roll_no || 'N/A') + ' • ' + (st.branch || 'Engineering') + ' (Class of ' + (st.batch_year || '2025') + ')';
    }

    let statusHtml = '';
    if (st.placement_status === 'Placed') {
        statusHtml = '<span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> Placed at ' + (st.placed_company || 'Target Company') + ' (' + (st.package_lpa ? '₹' + st.package_lpa + ' LPA' : 'Selected') + ')</span>';
    } else {
        statusHtml = '<span class="badge badge-primary"><i class="fa-solid fa-spinner"></i> Placement Status: ' + (st.placement_status || 'Ongoing / Actively Preparing') + '</span>';
    }

    bodyEl.innerHTML = `
        <div class="alumni-badges-row mb-3">
            <span class="badge badge-outline"><i class="fa-solid fa-building-columns"></i> ${st.branch}</span>
            <span class="badge badge-outline"><i class="fa-solid fa-calendar"></i> Batch ${st.batch_year}</span>
            ${statusHtml}
            <span class="badge badge-warning"><i class="fa-solid fa-bullseye"></i> Target: ${st.target_company || 'Tech Enterprise'}</span>
        </div>

        <div class="student-modal-kpi-grid mb-4">
            <div class="student-kpi-box">
                <div class="student-kpi-num text-primary">${atsScore}%</div>
                <div class="student-kpi-label">ATS Resume Score</div>
            </div>
            <div class="student-kpi-box">
                <div class="student-kpi-num text-emerald">${st.quizzes_completed || 0}</div>
                <div class="student-kpi-label">Quizzes Practiced</div>
            </div>
            <div class="student-kpi-box">
                <div class="student-kpi-num text-purple">${st.readiness_status || 'In Progress'}</div>
                <div class="student-kpi-label">Readiness Tier</div>
            </div>
        </div>

        <div class="alumni-section-title"><i class="fa-solid fa-address-card"></i> Student Contact Information:</div>
        <div class="alumni-email-tag mb-3" style="display:inline-flex;">
            <i class="fa-solid fa-envelope"></i> ${email}
        </div>

        <div class="alumni-section-title mt-3"><i class="fa-solid fa-chart-simple"></i> Preparation Progress Summary:</div>
        <div class="progress-bar-wrap mt-2">
            <div style="display:flex; justify-content;space-between; font-size:0.85rem; font-weight:700; margin-bottom:0.35rem;">
                <span>Resume ATS Compatibility</span>
                <span>${atsScore}%</span>
            </div>
            <div style="width:100%; height:10px; background:var(--bg-base); border-radius:10px; overflow:hidden; box-shadow:var(--nm-inset-sm);">
                <div style="width:${atsScore}%; height:100%; background:linear-gradient(90deg, #6366F1, #06B6D4); border-radius:10px;"></div>
            </div>
        </div>

        <div class="alumni-quote mt-4">
            <i class="fa-solid fa-user-check text-primary"></i> Verified student profile administered through the ITM Placement Management System.
        </div>
    `;

    if (gmailBtn) {
        gmailBtn.onclick = () => contactStudentViaGmail(encodeURIComponent(email), encodeURIComponent(st.name));
    }

    modal.classList.add('active');
}

function closeStudentProfileModal(e) {
    if (e && e.target && e.target !== e.currentTarget && !e.target.classList.contains('modal-close')) {
        return;
    }
    const modal = document.getElementById('student-profile-modal');
    if (modal) modal.classList.remove('active');
}

function contactStudentViaGmail(email, name) {
    const decodedEmail = decodeURIComponent(email || 'student.contact@itm.ac.in');
    const decodedName = decodeURIComponent(name || 'Student');

    const subject = 'Placement Discussion & Career Guidance - ' + decodedName;
    const body = 'Hi ' + decodedName + ',\n\nI hope this email finds you well!\n\nI noticed your student profile on the AI Career Companion portal and wanted to connect regarding your placement preparation and target opportunities.\n\nBest regards,\n[Your Name]';

    const gmailUrl = 'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(decodedEmail) + '&su=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    window.open(gmailUrl, '_blank', 'noopener,noreferrer');
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('student-profile-modal');
        if (modal && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    }
});

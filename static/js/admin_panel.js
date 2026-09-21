/**
 * AI Career Companion - Admin Control Panel & Student Management
 */

/* ==========================================================================
   GOOGLE APPS SCRIPT WEBHOOK CONFIGURATION
   Set your deployed Google Apps Script Web App URL below to automatically
   sync all ongoing and alumni students into your Google Sheet.
   ========================================================================== */
const GOOGLE_SCRIPT_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzsMqVXPFwTvGGyZBzLqxrzjgqEQsBfpJL61seZFEG_4u-9FENyWGdKjfGWgNx3lAtv/exec"

/**
 * Sends student & alumni registration data to Google Sheets via Google Apps Script Web App.
 * Matches the exact 17-column format:
 * 1. Student ID | 2. Student Type | 3. Full Name | 4. Contact Phone | 5. Email (Gmail) |
 * 6. Enrollment / Alumni User ID | 7. Department / Branch | 8. CSE/IT Section | 9. Graduation Batch |
 * 10. Target Company / Career Track | 11. Placed Company | 12. Role / Designation |
 * 13. Offered Package (₹ LPA) | 14. Login Password | 15. 2FA Security Key | 16. Account Status | 17. Created Date
 * 
 * @param {Object} entryData - Structured student or alumni record.
 */
async function syncToGoogleSheet(entryData) {
    if (!GOOGLE_SCRIPT_WEBHOOK_URL || GOOGLE_SCRIPT_WEBHOOK_URL.trim() === "") {
        console.log("[Google Sheets Sync] Webhook URL not configured yet. (Add your Apps Script URL to GOOGLE_SCRIPT_WEBHOOK_URL in admin_panel.js to enable auto-sync).");
        return;
    }

    try {
        const payload = {
            student_id: entryData.student_id || "N/A",
            student_type: entryData.student_type || "Ongoing Student",
            full_name: entryData.full_name || entryData.name || "Anonymous",
            contact_phone: entryData.contact_phone || entryData.phone || "N/A",
            email: entryData.email || "N/A",
            enrollment_alumni_id: entryData.enrollment_alumni_id || entryData.roll_no || entryData.alumni_id || "N/A",
            department_branch: entryData.department_branch || entryData.department || entryData.branch || "Computer Science & Engineering",
            section: entryData.section || entryData.cse_it_section || "N/A",
            graduation_batch: entryData.graduation_batch || entryData.batch_year || "2025",
            target_company: entryData.target_company || "General / Tech",
            placed_company: entryData.placed_company || entryData.company || "Not Placed",
            role_designation: entryData.role_designation || entryData.role || "Student / Aspirant",
            offered_package_lpa: entryData.offered_package_lpa !== undefined ? entryData.offered_package_lpa : (entryData.package_lpa || 0),
            login_password: entryData.login_password || entryData.password || "N/A",
            security_key_2fa: entryData.security_key_2fa || entryData.alumni_id || entryData.roll_no || "N/A",
            account_status: entryData.account_status || "Active",
            portal_url: window.location.origin + (String(entryData.student_type).includes('Alumni') ? '/student/login?role=alumni' : '/student/login'),
            created_date: entryData.created_date || new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
        };

        // Asynchronous post to Google Apps Script Web App
        await fetch(GOOGLE_SCRIPT_WEBHOOK_URL, {
            method: 'POST',
            mode: 'no-cors',
            headers: { 'Content-Type': 'text/plain;charset=utf-8' },
            body: JSON.stringify(payload)
        });
        console.log("[Google Sheets Sync] Record successfully dispatched to Google Sheets:", payload.full_name);
    } catch (err) {
        console.warn("[Google Sheets Sync Warning]:", err.message);
    }
}

let currentAdminTab = 'students';
let editingStudentId = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    // If admin is active or initialized
    if (window.AppState && window.AppState.currentSection === 'admin') {
        initAdminPanel();
    }
});

function initAdminPanel() {
    fetchAdminStats();
    fetchAdminStudents();
}

function switchAdminTab(tabName) {
    currentAdminTab = tabName;

    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    document.querySelectorAll('.admin-tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `admin-tab-${tabName}`);
    });

    if (tabName === 'students') fetchAdminStudents();
    else if (tabName === 'alumni') fetchAdminAlumni();
}

/* ==========================================================================
   ADMIN STATS
   ========================================================================== */
async function fetchAdminStats() {
    try {
        const res = await fetch('/api/admin/stats');
        const data = await res.json();
        if (data.success) {
            const s = data.stats;
            if (document.getElementById('admin-stat-students')) document.getElementById('admin-stat-students').innerText = s.total_students;
            if (document.getElementById('admin-stat-placed')) document.getElementById('admin-stat-placed').innerText = s.placed_students;
            if (document.getElementById('admin-stat-ats')) document.getElementById('admin-stat-ats').innerText = `${s.avg_ats}%`;
            if (document.getElementById('admin-stat-alumni')) document.getElementById('admin-stat-alumni').innerText = s.total_alumni || 0;
        }
    } catch (err) {
        console.error('Failed to load admin stats:', err);
    }
}

/* ==========================================================================
   STUDENT MANAGEMENT (CRUD)
   ========================================================================== */
async function fetchAdminStudents() {
    const search = document.getElementById('admin-student-search')?.value.trim() || '';
    const branch = document.getElementById('admin-branch-filter')?.value || 'all';
    const status = document.getElementById('admin-status-filter')?.value || 'all';
    const readiness = document.getElementById('admin-readiness-filter')?.value || 'all';

    const tbody = document.getElementById('admin-students-tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="8" class="text-center p-4"><div class="spinner"></div> Loading students...</td></tr>';

    try {
        const queryParams = new URLSearchParams({ search, branch, status, readiness });
        const res = await fetch(`/api/admin/students?${queryParams.toString()}`);
        const data = await res.json();

        if (!data.success || data.students.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center p-4 text-muted">No student records found matching your filters.</td></tr>';
            return;
        }

        renderAdminStudentsTable(data.students);
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center p-4 text-danger">Error loading students: ${err.message}</td></tr>`;
    }
}

function renderAdminStudentsTable(students) {
    const tbody = document.getElementById('admin-students-tbody');
    tbody.innerHTML = '';

    students.forEach(s => {
        const tr = document.createElement('tr');

        // Status badges
        const readinessBadge = s.readiness_status === 'Placement Ready' ? 'badge-success' :
                               s.readiness_status === 'In Progress' ? 'badge-warning' : 'badge-danger';

        const placementBadge = s.placement_status === 'Placed' ? 'badge-success' :
                               s.placement_status === 'Interviewing' ? 'badge-primary' : 'badge-outline';

        tr.innerHTML = `
            <td>
                <strong>${s.name}</strong>
                <div style="font-size:0.75rem; color:var(--text-muted);">${s.email}</div>
            </td>
            <td><code>${s.roll_no}</code></td>
            <td>${s.branch} (${s.batch_year})</td>
            <td>
                <span class="score-pill ${s.ats_score >= 80 ? 'score-high' : s.ats_score >= 60 ? 'score-mid' : 'score-low'}">
                    ${s.ats_score}%
                </span>
            </td>
            <td><span class="badge ${readinessBadge}">${s.readiness_status}</span></td>
            <td>${s.quizzes_completed} tests</td>
            <td>
                <span class="badge ${placementBadge}">${s.placement_status}</span>
                ${s.placed_company ? `<div style="font-size:0.75rem; color:var(--primary-soft); font-weight:700;">${s.placed_company} (${s.package_lpa} LPA)</div>` : ''}
            </td>
            <td>
                <div class="table-actions">
                    <button class="btn btn-outline-success btn-sm" onclick="openPromoteModal(${s.id})" title="Promote to Alumni Hub">
                        <i class="fa-solid fa-graduation-cap"></i> Promote
                    </button>
                    <button class="btn btn-outline btn-sm" onclick="openEditStudentModal(${s.id})" title="Edit Student Progress">
                        <i class="fa-solid fa-pen-to-square"></i>
                    </button>
                    <button class="btn btn-danger-outline btn-sm" onclick="confirmDeleteStudent(${s.id}, '${s.name}')" title="Delete Student">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        `;

        tbody.appendChild(tr);
    });
}

let promotingStudentId = null;

// Open Promote to Alumni Modal
async function openPromoteModal(studentId) {
    try {
        const res = await fetch(`/api/admin/students/${studentId}`);
        const data = await res.json();
        if (!data.success || !data.student) {
            showToast('Failed to load student details.', 'error');
            return;
        }

        const s = data.student;
        promotingStudentId = s.id;

        document.getElementById('promote-student-id').value = s.id;
        document.getElementById('form-promote-name').value = s.name;
        document.getElementById('form-promote-batch').value = s.batch_year || '2024';
        document.getElementById('form-promote-email').value = s.email;
        document.getElementById('form-promote-company').value = s.placed_company || s.target_company || 'Amazon';
        document.getElementById('form-promote-role').value = 'Software Development Engineer (SDE-1)';
        document.getElementById('form-promote-package').value = s.package_lpa > 0 ? s.package_lpa : 12.0;
        document.getElementById('form-promote-difficulty').value = 'Medium';
        document.getElementById('form-promote-mode').value = 'On-Campus';
        document.getElementById('form-promote-rounds').value = `Round 1: Online Technical Assessment (DSA & Problem Solving)\nRound 2: Technical Interview (OOP Principles, SQL Queries, Project Walkthrough)\nRound 3: HR & Cultural Alignment Round`;
        document.getElementById('form-promote-prep').value = `Prepared with AI Career Companion Practice MCQs, LeetCode top interview 150, and Core CS revision.`;
        document.getElementById('form-promote-advice').value = `Be confident, clarify requirements before coding, and master your resume projects thoroughly.`;

        document.getElementById('promote-modal-backdrop').classList.add('active');
    } catch (err) {
        showToast('Error loading student: ' + err.message, 'error');
    }
}

function closePromoteModal(event) {
    if (event && event.target !== document.getElementById('promote-modal-backdrop') && !event.target.classList.contains('modal-close-btn') && !event.target.classList.contains('btn-cancel')) {
        return;
    }
    const modal = document.getElementById('promote-modal-backdrop');
    if (modal) modal.classList.remove('active');
}

async function submitPromoteStudentForm(event) {
    event.preventDefault();
    if (!promotingStudentId) return;

    const payload = {
        student_name: document.getElementById('form-promote-name').value.trim(),
        batch_year: document.getElementById('form-promote-batch').value.trim(),
        email: document.getElementById('form-promote-email').value.trim(),
        company: document.getElementById('form-promote-company').value.trim(),
        role: document.getElementById('form-promote-role').value.trim(),
        package_lpa: parseFloat(document.getElementById('form-promote-package').value || 10),
        difficulty: document.getElementById('form-promote-difficulty').value,
        offer_type: document.getElementById('form-promote-mode').value,
        rounds: document.getElementById('form-promote-rounds').value.trim(),
        preparation_tips: document.getElementById('form-promote-prep').value.trim(),
        advice_to_juniors: document.getElementById('form-promote-advice').value.trim()
    };

    try {
        const res = await fetch(`/api/admin/students/promote-to-alumni/${promotingStudentId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to promote student.', 'error');
            return;
        }

        document.getElementById('promote-modal-backdrop').classList.remove('active');
        showToast(data.message, 'success');

        // Show generated alumni login credentials to admin so they can share with the student
        const loginId = data.alumni_login_id || payload.email.split('@')[0].toUpperCase();
        const loginPwd = data.alumni_password || 'alumni123';
        const loginEmail = data.alumni_email || payload.email;
        setTimeout(() => {
            alert(
                `Alumni Account Created Successfully!\n\n` +
                `Student Name : ${payload.student_name}\n` +
                `Alumni Login ID : ${loginId}\n` +
                `Password  : ${loginPwd}\n` +
                `Email  : ${loginEmail}\n\n` +
                `Share these credentials with the student so they can log in to the Alumni Portal.\n` +
                `(They can change their password after first login.)`
            );
        }, 400);

        // Automatically sync promoted alumni student to Google Sheets
        syncToGoogleSheet({
            student_id: promotingStudentId,
            student_type: "Alumni Student (Promoted)",
            full_name: payload.student_name,
            contact_phone: "N/A",
            email: loginEmail,
            enrollment_alumni_id: loginId,
            department_branch: "Computer Science & Engineering",
            section: "N/A (Promoted)",
            graduation_batch: payload.batch_year,
            target_company: payload.company,
            placed_company: payload.company,
            role_designation: payload.role,
            offered_package_lpa: payload.package_lpa,
            login_password: loginPwd,
            security_key_2fa: loginId,
            account_status: "Placed & Promoted to Alumni",
            created_date: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
        });

        // Refresh admin views
        fetchAdminStudents();
        fetchAdminStats();
        fetchAdminAlumni();
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}


function debounceAdminStudentSearch() {
    clearTimeout(window.adminSearchTimer);
    window.adminSearchTimer = setTimeout(() => {
        fetchAdminStudents();
    }, 300);
}

// Add Student Modal
function openAddStudentModal() {
    const modal = document.getElementById('student-modal-backdrop');
    if (!modal) return;

    document.getElementById('student-modal-title').innerHTML = '<i class="fa-solid fa-user-plus text-primary"></i> Add New Student to Cohort';
    document.getElementById('student-form').reset();
    editingStudentId = null;
    modal.classList.add('active');
}

// Edit Student Modal
async function openEditStudentModal(studentId) {
    try {
        const res = await fetch(`/api/admin/students/${studentId}`);
        const data = await res.json();
        if (!data.success || !data.student) {
            showToast('Failed to load student details.', 'error');
            return;
        }

        const s = data.student;
        editingStudentId = s.id;

        document.getElementById('student-modal-title').innerHTML = `<i class="fa-solid fa-user-pen text-primary"></i> Edit Student: <strong>${s.name}</strong>`;
        document.getElementById('form-student-name').value = s.name;
        document.getElementById('form-student-roll').value = s.roll_no;
        document.getElementById('form-student-email').value = s.email;
        document.getElementById('form-student-branch').value = s.branch;
        document.getElementById('form-student-batch').value = s.batch_year;
        document.getElementById('form-student-ats').value = s.ats_score;
        document.getElementById('form-student-readiness').value = s.readiness_status;
        document.getElementById('form-student-target').value = s.target_company;
        document.getElementById('form-student-quizzes').value = s.quizzes_completed;
        document.getElementById('form-student-placement').value = s.placement_status;
        document.getElementById('form-student-company').value = s.placed_company || '';
        document.getElementById('form-student-package').value = s.package_lpa || 0;

        document.getElementById('student-modal-backdrop').classList.add('active');
    } catch (err) {
        showToast('Error: ' + err.message, 'error');
    }
}

function closeStudentModal(event) {
    if (event && event.target !== document.getElementById('student-modal-backdrop') && !event.target.classList.contains('modal-close-btn') && !event.target.classList.contains('btn-cancel')) {
        return;
    }
    const modal = document.getElementById('student-modal-backdrop');
    if (modal) modal.classList.remove('active');
}

async function submitStudentForm(event) {
    event.preventDefault();

    const payload = {
        name: document.getElementById('form-student-name').value.trim(),
        roll_no: document.getElementById('form-student-roll').value.trim(),
        email: document.getElementById('form-student-email').value.trim(),
        branch: document.getElementById('form-student-branch').value,
        batch_year: document.getElementById('form-student-batch').value.trim(),
        ats_score: parseFloat(document.getElementById('form-student-ats').value || 0),
        readiness_status: document.getElementById('form-student-readiness').value,
        target_company: document.getElementById('form-student-target').value.trim(),
        quizzes_completed: parseInt(document.getElementById('form-student-quizzes').value || 0),
        placement_status: document.getElementById('form-student-placement').value,
        placed_company: document.getElementById('form-student-company').value.trim(),
        package_lpa: parseFloat(document.getElementById('form-student-package').value || 0)
    };

    const isEdit = (editingStudentId !== null);
    const url = isEdit ? `/api/admin/students/update/${editingStudentId}` : '/api/admin/students/add';
    const method = isEdit ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to save student.', 'error');
            return;
        }

        document.getElementById('student-modal-backdrop').classList.remove('active');
        showToast(data.message, 'success');

        // Automatically sync to Google Sheets
        syncToGoogleSheet({
            student_id: data.id || payload.roll_no,
            student_type: payload.placement_status === 'Placed' ? 'Alumni Student' : 'Ongoing Student',
            full_name: payload.name,
            contact_phone: "N/A",
            email: payload.email,
            enrollment_alumni_id: payload.roll_no,
            department_branch: payload.branch,
            section: "Section A",
            graduation_batch: payload.batch_year,
            target_company: payload.target_company,
            placed_company: payload.placed_company || (payload.placement_status === 'Placed' ? payload.target_company : 'Not Placed'),
            role_designation: payload.placement_status === 'Placed' ? 'Software Engineer' : 'Student Candidate',
            offered_package_lpa: payload.package_lpa || 0,
            login_password: "N/A",
            security_key_2fa: payload.roll_no,
            account_status: payload.readiness_status || 'In Progress',
            created_date: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
        });

        fetchAdminStudents();
        fetchAdminStats();
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}

async function confirmDeleteStudent(studentId, name) {
    if (!confirm(`Are you sure you want to remove student "${name}" from the database?`)) {
        return;
    }

    try {
        const res = await fetch(`/api/admin/students/delete/${studentId}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            showToast(`Student ${name} deleted successfully.`, 'success');
            fetchAdminStudents();
            fetchAdminStats();
        } else {
            showToast(data.error || 'Failed to delete student.', 'error');
        }
    } catch (err) {
        showToast('Error deleting student: ' + err.message, 'error');
    }
}

/* ==========================================================================
   ALUMNI MANAGEMENT (ADMIN POWER)
   ========================================================================== */
async function fetchAdminAlumni() {
    const tbody = document.getElementById('admin-alumni-tbody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="7" class="text-center p-4"><div class="spinner"></div> Loading alumni stories...</td></tr>';

    try {
        const res = await fetch('/api/alumni/experiences?company=all&difficulty=all');
        const data = await res.json();

        if (!data.success || data.experiences.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center p-4 text-muted">No alumni experiences found.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        data.experiences.forEach(exp => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${exp.student_name}</strong></td>
                <td>${exp.email}</td>
                <td><span class="badge badge-primary">${exp.company}</span></td>
                <td>${exp.role}</td>
                <td><strong>₹${exp.package_lpa} LPA</strong></td>
                <td><i class="fa-solid fa-heart text-danger"></i> ${exp.upvotes}</td>
                <td>
                    <button class="btn btn-danger-outline btn-sm" onclick="confirmDeleteAlumni(${exp.id}, '${exp.student_name}')" title="Delete Experience">
                        <i class="fa-solid fa-trash"></i> Delete
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center p-4 text-danger">Error: ${err.message}</td></tr>`;
    }
}

async function confirmDeleteAlumni(expId, name) {
    if (!confirm(`Are you sure you want to remove the placement experience of "${name}"?`)) {
        return;
    }

    try {
        const res = await fetch(`/api/admin/alumni/delete/${expId}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            showToast('Alumni story removed.', 'success');
            fetchAdminAlumni();
            fetchAdminStats();
            if (typeof fetchAlumniExperiences === 'function') fetchAlumniExperiences();
        } else {
            showToast(data.error || 'Failed to delete.', 'error');
        }
    } catch (err) {
        showToast('Error: ' + err.message, 'error');
    }
}

// ==========================================
// CREATE STUDENT LOGIN PORTAL HANDLERS
// ==========================================
function openCreateStudentLoginModal() {
    const modal = document.getElementById('create-student-login-backdrop');
    if (!modal) return;
    document.getElementById('create-student-login-form').reset();
    document.getElementById('new-st-password').value = 'student@123';
    document.getElementById('new-st-batch').value = '2025';
    modal.classList.add('active');
}

function closeCreateStudentLoginModal(event) {
    if (event && event.target !== document.getElementById('create-student-login-backdrop') && !event.target.classList.contains('modal-close-btn') && !event.target.classList.contains('btn-cancel')) {
        return;
    }
    const modal = document.getElementById('create-student-login-backdrop');
    if (modal) modal.classList.remove('active');
}

async function submitCreateStudentLoginForm(event) {
    event.preventDefault();

    const payload = {
        name: document.getElementById('new-st-name').value.trim(),
        phone: document.getElementById('new-st-phone').value.trim(),
        email: document.getElementById('new-st-email').value.trim(),
        department: document.getElementById('new-st-department').value,
        branch: document.getElementById('new-st-department').value,
        section: document.getElementById('new-st-section').value,
        roll_no: document.getElementById('new-st-enrollment').value.trim(),
        enrollment_no: document.getElementById('new-st-enrollment').value.trim(),
        password: document.getElementById('new-st-password').value.trim(),
        batch_year: document.getElementById('new-st-batch').value.trim() || '2025',
        target_company: document.getElementById('new-st-target').value.trim() || 'General / Tech',
        ats_score: 75.0,
        readiness_status: 'In Progress',
        placement_status: 'Not Placed'
    };

    try {
        const res = await fetch('/api/admin/students/create-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to create student account.', 'error');
            return;
        }

        document.getElementById('create-student-login-backdrop').classList.remove('active');
        document.getElementById('create-student-login-form').reset();
        showToast(`🎉 Student Account Created! Enrollment: ${payload.roll_no} | Password: ${payload.password}`, 'success');

        // Automatically sync newly created ongoing student to Google Sheets
        syncToGoogleSheet({
            student_id: data.id || payload.roll_no,
            student_type: "Ongoing Student",
            full_name: payload.name,
            contact_phone: payload.phone,
            email: payload.email,
            enrollment_alumni_id: payload.roll_no,
            department_branch: payload.branch,
            section: payload.section,
            graduation_batch: payload.batch_year,
            target_company: payload.target_company,
            placed_company: payload.placed_company || "Not Placed",
            role_designation: "Student / Aspirant",
            offered_package_lpa: payload.package_lpa || 0,
            login_password: payload.password,
            security_key_2fa: payload.roll_no,
            account_status: "Active (Ongoing Student)",
            created_date: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
        });

        fetchAdminStudents();
        fetchAdminStats();
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}

/* ==========================================================================
   ADMIN DIRECT PUBLISH ALUMNI STORY
   ========================================================================== */
function openAdminAddExperienceModal() {
    const modal = document.getElementById('admin-experience-modal-backdrop');
    if (!modal) return;
    document.getElementById('admin-experience-form').reset();
    modal.classList.add('active');
}

function closeAdminAddExperienceModal(event) {
    if (event && event.target !== document.getElementById('admin-experience-modal-backdrop') && !event.target.classList.contains('modal-close-btn') && !event.target.classList.contains('btn-cancel')) {
        return;
    }
    const modal = document.getElementById('admin-experience-modal-backdrop');
    if (modal) modal.classList.remove('active');
}

async function submitAdminExperienceForm(event) {
    event.preventDefault();

    const name = document.getElementById('admin-exp-name').value.trim();
    const batch = document.getElementById('admin-exp-batch').value.trim();
    const email = document.getElementById('admin-exp-email').value.trim();
    const company = document.getElementById('admin-exp-company').value.trim();
    const role = document.getElementById('admin-exp-role').value.trim();
    const pkg = parseFloat(document.getElementById('admin-exp-package').value || 8.0);
    const difficulty = document.getElementById('admin-exp-difficulty').value;
    const mode = document.getElementById('admin-exp-mode').value;
    const rawRounds = document.getElementById('admin-exp-rounds').value.trim();
    const prep = document.getElementById('admin-exp-prep').value.trim();
    const advice = document.getElementById('admin-exp-advice').value.trim();

    const rounds = rawRounds.split('\n').filter(l => l.trim().length > 0).map((line, idx) => ({
        round_name: line.includes(':') ? line.split(':')[0].trim() : `Round ${idx + 1}`,
        details: line.includes(':') ? line.split(':').slice(1).join(':').trim() : line.trim()
    }));

    const payload = {
        student_name: name,
        batch_year: batch,
        email: email,
        company: company,
        role: role,
        package_lpa: pkg,
        offer_type: mode,
        difficulty: difficulty,
        status: 'Selected',
        rounds: rounds,
        preparation_tips: prep,
        advice_to_juniors: advice
    };

    try {
        const res = await fetch('/api/alumni/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to publish story.', 'error');
            return;
        }

        document.getElementById('admin-experience-modal-backdrop').classList.remove('active');
        document.getElementById('admin-experience-form').reset();
        showToast('🎉 Placement Story Published to Alumni Hub!', 'success');

        fetchAdminAlumni();
        fetchAdminStats();
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}

/* ==========================================================================
   ADMIN REGISTER ALUMNI STUDENT LOGIN ACCOUNT
   ========================================================================== */
function openCreateAlumniLoginModal() {
    const modal = document.getElementById('create-alumni-login-backdrop');
    if (!modal) return;
    document.getElementById('create-alumni-login-form').reset();
    document.getElementById('new-al-batch').value = new Date().getFullYear().toString();
    modal.classList.add('active');
}

function closeCreateAlumniLoginModal(event) {
    if (event && event.target !== document.getElementById('create-alumni-login-backdrop') && !event.target.classList.contains('modal-close-btn') && !event.target.classList.contains('btn-cancel')) {
        return;
    }
    const modal = document.getElementById('create-alumni-login-backdrop');
    if (modal) modal.classList.remove('active');
}

async function submitCreateAlumniLoginForm(event) {
    event.preventDefault();

    const name = document.getElementById('new-al-name').value.trim();
    const alumni_id = document.getElementById('new-al-id').value.trim().toUpperCase();
    const email = document.getElementById('new-al-email').value.trim();
    const company = document.getElementById('new-al-company').value.trim();
    const role = document.getElementById('new-al-role').value.trim();
    const pkg = parseFloat(document.getElementById('new-al-package').value || 0);
    const branch = document.getElementById('new-al-branch').value;
    const batch = document.getElementById('new-al-batch').value.trim();
    const phone = document.getElementById('new-al-phone').value.trim();
    const password = document.getElementById('new-al-password').value.trim();
    const sec_key = document.getElementById('new-al-2fa').value.trim().toUpperCase() || alumni_id;
    const rawRounds = document.getElementById('new-al-rounds').value.trim();
    const prep = document.getElementById('new-al-prep').value.trim();

    const payload = {
        name: name,
        alumni_id: alumni_id,
        email: email,
        phone: phone,
        branch: branch,
        department: branch,
        batch_year: batch,
        company: company,
        role: role,
        package_lpa: pkg,
        password: password,
        security_key_2fa: sec_key,
        rounds: rawRounds,
        preparation_tips: prep,
        advice_to_juniors: prep
    };

    try {
        const res = await fetch('/api/admin/alumni/create-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
            showToast(data.error || 'Failed to create alumni account.', 'error');
            return;
        }

        document.getElementById('create-alumni-login-backdrop').classList.remove('active');
        document.getElementById('create-alumni-login-form').reset();
        showToast(`🎉 Alumni Account Created! User ID: ${alumni_id} | Password: ${password}`, 'success');

        // Automatically sync newly created alumni student to Google Sheets
        syncToGoogleSheet({
            student_id: data.id || alumni_id,
            student_type: "Alumni Student",
            full_name: name,
            contact_phone: phone,
            email: email,
            enrollment_alumni_id: alumni_id,
            department_branch: branch,
            section: "N/A (Alumni)",
            graduation_batch: batch,
            target_company: company,
            placed_company: company,
            role_designation: role,
            offered_package_lpa: pkg,
            login_password: password,
            security_key_2fa: sec_key,
            account_status: "Verified Alumni Mentor",
            created_date: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
        });

        fetchAdminAlumni();
        fetchAdminStats();
    } catch (err) {
        showToast('Network error: ' + err.message, 'error');
    }
}


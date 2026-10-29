import os

def process_admin_alumni_html():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin_alumni.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update top nav
    content = content.replace('href="#" class="admin-nav-link active"><i data-lucide="layout-dashboard"></i> Cohort Management', 'href="/admin" class="admin-nav-link"><i data-lucide="layout-dashboard"></i> Cohort Management')
    content = content.replace('href="#" class="admin-nav-link" onclick="document.getElementById(\'tab-alumni\').click()"><i data-lucide="users"></i> Alumni Records', 'href="/admin/alumni" class="admin-nav-link active"><i data-lucide="users"></i> Alumni Records')
    content = content.replace('href="#" class="admin-nav-link"><i data-lucide="settings"></i> Settings', 'href="/admin/settings" class="admin-nav-link"><i data-lucide="settings"></i> Settings')

    # Update Hero
    content = content.replace('Cohort & <span>Placement Management</span>', 'Alumni <span>Records & Placements</span>')
    content = content.replace('Manage student cohorts, track real-time placement progress, and supervise alumni records & verified mentors.', 'Manage verified alumni accounts, placement stories, and mentorship network.')

    # Remove tabs
    tabs_html = """<div class="admin-tabs">
                        <button class="admin-tab active" id="tab-students" onclick="switchAdminTab('students')">
                            <i data-lucide="graduation-cap"></i> Student Cohort & Progress
                        </button>
                        <button class="admin-tab" id="tab-alumni" onclick="switchAdminTab('alumni')">
                            <i data-lucide="users"></i> Manage Alumni Records
                        </button>
                    </div>"""
    
    new_tabs_html = """<div class="admin-tabs">
                        <h3 style="margin:0; font-size: 1.1rem; color: var(--admin-text-main); font-weight: 700;">
                            <i data-lucide="users" style="vertical-align:middle; margin-right:8px; color:var(--admin-purple);"></i> Alumni Records
                        </h3>
                    </div>"""
    content = content.replace(tabs_html, new_tabs_html)

    # Change button
    content = content.replace('<button class="admin-btn-primary" onclick="openCreateStudentLoginModal()" id="btn-add-student">\n                        <i data-lucide="plus"></i> Add Ongoing Student\n                    </button>', '<button class="admin-btn-primary" onclick="openAdminAddExperienceModal()" style="background: linear-gradient(135deg, var(--admin-purple), var(--admin-primary));">\n                        <i data-lucide="plus"></i> Add Placement Record\n                    </button>')

    # Remove student view and filter bar
    student_view_start = content.find('<div class="admin-filter-bar">')
    student_view_end = content.find('<!-- Alumni Table (Hidden by default) -->')
    if student_view_start != -1 and student_view_end != -1:
        content = content[:student_view_start] + content[student_view_end:]

    # Make alumni view visible
    content = content.replace('<div class="admin-table-wrapper" id="alumni-view" style="display:none;">', '<div class="admin-table-wrapper" id="alumni-view">')

    # Also change the JS init function for this page to fetch alumni instead
    # Wait, the easiest way is to add a script block at the end that switches to alumni tab or just fetches alumni
    script_inject = """<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Override the default fetch
        setTimeout(() => {
            fetchAdminAlumni();
            fetchAdminStats();
        }, 100);
    });
</script></body>"""
    content = content.replace('</body>', script_inject)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_admin_alumni_html()
print("Processed admin_alumni.html")

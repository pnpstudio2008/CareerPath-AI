import os

def process_admin_html():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update top nav
    content = content.replace('href="#" class="admin-nav-link active"><i data-lucide="layout-dashboard"></i> Cohort Management', 'href="/admin" class="admin-nav-link active"><i data-lucide="layout-dashboard"></i> Cohort Management')
    content = content.replace('href="#" class="admin-nav-link" onclick="document.getElementById(\'tab-alumni\').click()"><i data-lucide="users"></i> Alumni Records', 'href="/admin/alumni" class="admin-nav-link"><i data-lucide="users"></i> Alumni Records')
    content = content.replace('href="#" class="admin-nav-link"><i data-lucide="settings"></i> Settings', 'href="/admin/settings" class="admin-nav-link"><i data-lucide="settings"></i> Settings')

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
                            <i data-lucide="graduation-cap" style="vertical-align:middle; margin-right:8px; color:var(--admin-primary);"></i> Student Cohort
                        </h3>
                    </div>"""
    content = content.replace(tabs_html, new_tabs_html)

    # Remove alumni view
    alumni_view_start = content.find('<!-- Alumni Table (Hidden by default) -->')
    alumni_view_end = content.find('<!-- Pagination -->')
    if alumni_view_start != -1 and alumni_view_end != -1:
        content = content[:alumni_view_start] + content[alumni_view_end:]

    # Make students-view always display without inline style (wait it doesn't have display:none but let's check)
    
    # Let's remove alumni modals (optional, but cleaner)
    alumni_modal1 = content.find('<div class="modal-backdrop" id="create-alumni-login-backdrop"')
    alumni_modal1_end = content.find('<div class="modal-backdrop" id="admin-experience-modal-backdrop"')
    alumni_modal2 = content.find('<div class="modal-backdrop" id="admin-experience-modal-backdrop"')
    alumni_modal2_end = content.find('<div class="modal-backdrop" id="promote-modal-backdrop"')
    # We will just leave modals to avoid breaking JS unless necessary

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_admin_html()
print("Processed admin.html")

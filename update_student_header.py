import re

def update_student_header():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\student_profile.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_header = """
    <header class="navbar saas-navbar">
        <div class="nav-container saas-nav-container">
            <div class="nav-brand">
                <img src="/static/images/logo.png" alt="Logo" class="brand-logo-img" style="width: 42px; height: 42px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div class="brand-text">
                    <span class="brand-title" style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">AI Career Companion</span>
                    <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748B; font-weight: 500;">Student Portal</span>
                </div>
            </div>

            <!-- Nav Actions -->
            <div class="nav-actions saas-nav-actions">
                <a href="/" class="btn btn-outline btn-sm" title="Main Platform">
                    <i class="fa-solid fa-globe"></i> <span>Platform</span>
                </a>
                <button class="btn btn-primary btn-sm" onclick="openEditProfileModal()">
                    <i class="fa-solid fa-user-pen"></i> <span>Edit Profile</span>
                </button>
                <button class="btn btn-outline btn-sm" onclick="studentLogout()">
                    <i class="fa-solid fa-right-from-bracket"></i> <span>Logout</span>
                </button>
            </div>
        </div>
    </header>
"""
    pattern = re.compile(r'<header class="student-portal-header">.*?</header>', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_header.strip(), content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated student_profile header!')

update_student_header()

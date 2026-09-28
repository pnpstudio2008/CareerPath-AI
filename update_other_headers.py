import re

def update_alumni_header():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\alumni_profile.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_header = """
    <header class="navbar saas-navbar">
        <div class="nav-container saas-nav-container">
            <div class="nav-brand">
                <img src="/static/images/logo.png" alt="Logo" class="brand-logo-img" style="width: 42px; height: 42px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div class="brand-text">
                    <span class="brand-title" style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">AI Career Companion</span>
                    <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748B; font-weight: 500;">Alumni Portal</span>
                </div>
            </div>

            <!-- Nav Actions -->
            <div class="nav-actions saas-nav-actions">
                <a href="/?view=platform" class="btn btn-outline btn-sm" title="Main Platform">
                    <i class="fa-solid fa-globe"></i> <span>Platform</span>
                </a>
                <button class="btn btn-outline btn-sm" onclick="alumniLogout()">
                    <i class="fa-solid fa-right-from-bracket"></i> <span>Logout</span>
                </button>
            </div>
        </div>
    </header>
"""
    pattern = re.compile(r'<header class="alumni-portal-header">.*?</header>', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_header.strip(), content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated alumni_profile header!')

def update_admin_header():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_header = """
    <header class="navbar saas-navbar">
        <div class="nav-container saas-nav-container">
            <div class="nav-brand">
                <img src="/static/images/logo.png" alt="Logo" class="brand-logo-img" style="width: 42px; height: 42px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div class="brand-text">
                    <span class="brand-title" style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">AI Career Companion</span>
                    <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748B; font-weight: 500;">Admin Console</span>
                </div>
            </div>

            <!-- Nav Actions -->
            <div class="nav-actions saas-nav-actions">
                <a href="/" class="btn btn-outline btn-sm" title="Main Platform">
                    <i class="fa-solid fa-globe"></i> <span>Platform</span>
                </a>
                <a href="/api/admin/logout" class="btn btn-outline btn-sm">
                    <i class="fa-solid fa-right-from-bracket"></i> <span>Logout</span>
                </a>
            </div>
        </div>
    </header>
"""
    pattern = re.compile(r'<header class="admin-header">.*?</header>', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_header.strip(), content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Updated admin header!')

update_alumni_header()
update_admin_header()

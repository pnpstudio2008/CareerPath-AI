import re

def update_header():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_header = """
    <!-- Top Navigation Header -->
    <header class="navbar saas-navbar">
        <div class="nav-container saas-nav-container">
            <div class="nav-brand" onclick="navigateTo('home')" style="gap: 12px;">
                <img src="/static/images/logo.png" alt="Logo" class="brand-logo-img" style="width: 42px; height: 42px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div class="brand-text">
                    <span class="brand-title" style="font-size: 1.15rem; font-weight: 800; color: #0F172A;">AI Career Companion</span>
                    <span class="brand-subtitle" style="font-size: 0.75rem; color: #64748B; font-weight: 500;">By Riya Modi & Diksha Durgapal</span>
                </div>
            </div>

            <!-- Desktop Nav Links -->
            <nav class="nav-menu saas-nav-menu" id="nav-menu">
                <a href="#home" class="nav-link active saas-nav-link" onclick="navigateTo('home')">
                    <i class="fa-solid fa-house"></i> <span>Home</span>
                </a>
                <a href="#analyzer" class="nav-link saas-nav-link" onclick="navigateTo('analyzer')">
                    <i class="fa-solid fa-file-invoice"></i> <span>Resume Analyzer</span>
                </a>
                <a href="#mocktest" class="nav-link saas-nav-link" onclick="navigateTo('mocktest')">
                    <i class="fa-solid fa-circle-check"></i> <span>Mock Test</span>
                </a>
                <a href="#prep" class="nav-link saas-nav-link" onclick="navigateTo('prep')">
                    <i class="fa-solid fa-laptop-code"></i> <span>Practice</span>
                </a>
                <a href="#alumni" class="nav-link saas-nav-link" onclick="navigateTo('alumni')">
                    <i class="fa-solid fa-users-viewfinder"></i> <span>Alumni Hub</span>
                </a>
            </nav>

            <!-- Nav Actions -->
            <div class="nav-actions saas-nav-actions">
                <button class="saas-icon-btn"><i class="fa-solid fa-magnifying-glass"></i></button>
                <button class="saas-icon-btn has-notification"><i class="fa-solid fa-bell"></i></button>
                
                <div class="saas-profile-dropdown" onclick="window.location.href='{{ user.dashboard_url if user else '/login' }}'">
                    {% if user %}
                        <div class="saas-avatar-small">{{ user.name[0] }}</div>
                        <span class="saas-profile-name">{{ user.name }}</span>
                    {% else %}
                        <div class="saas-avatar-small"><i class="fa-solid fa-user"></i></div>
                        <span class="saas-profile-name">Login</span>
                    {% endif %}
                    <i class="fa-solid fa-chevron-down" style="font-size: 0.7rem; color: #64748B;"></i>
                </div>
                
                <button class="mobile-menu-toggle" id="mobile-toggle">
                    <i class="fa-solid fa-bars"></i>
                </button>
            </div>
        </div>
    </header>
"""

    pattern = re.compile(r'<header class="navbar">.*?</header>', re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_header.strip(), content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated header in index.html")
    else:
        print("Could not find header in index.html")

update_header()

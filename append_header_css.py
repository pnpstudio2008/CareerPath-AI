import os

def append_saas_styles():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'
    
    saas_css = """
/* ==========================================================================
   SAAS HEADER STYLES
   ========================================================================== */
.saas-navbar {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0.75rem 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.saas-nav-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.saas-nav-menu {
    display: flex;
    gap: 0.5rem;
    background: transparent;
}

.saas-nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    transition: all 0.2s ease;
}

.saas-nav-link:hover {
    background: #F1F5F9;
    color: var(--text-primary);
}

.saas-nav-link.active {
    background: var(--primary);
    color: #FFFFFF;
}

.saas-nav-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.saas-icon-btn {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 1px solid var(--border-subtle);
    background: #FFFFFF;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    transition: all 0.2s ease;
}

.saas-icon-btn:hover {
    background: #F1F5F9;
    color: var(--text-primary);
}

.saas-icon-btn.has-notification::after {
    content: '';
    position: absolute;
    top: 10px;
    right: 10px;
    width: 6px;
    height: 6px;
    background: var(--accent-rose);
    border-radius: 50%;
}

.saas-profile-dropdown {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.6rem 0.4rem 0.4rem;
    background: #F8FAFC;
    border: 1px solid var(--border-subtle);
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.saas-profile-dropdown:hover {
    background: #F1F5F9;
    border-color: #CBD5E1;
}

.saas-avatar-small {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--primary);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
}

.saas-profile-name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
}

@media (max-width: 992px) {
    .saas-nav-menu { display: none; }
}
"""
    
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(saas_css)

append_saas_styles()
print('Appended SaaS Header styles.')

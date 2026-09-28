import os

def append_saas_styles():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'
    
    saas_css = """
/* ==========================================================================
   SAAS DASHBOARD OVERRIDES (Landing / Home)
   ========================================================================== */

.saas-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 3rem;
    padding: 2rem 0 4rem 0;
}

.saas-hero-content {
    flex: 1;
    max-width: 600px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(37, 99, 235, 0.1);
    color: var(--primary);
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

.saas-hero-content h1 {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.saas-hero-content p {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 2rem;
    line-height: 1.6;
}

.hero-cta-group {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.hero-trust {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.avatar-group {
    display: flex;
}

.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #CBD5E1;
    border: 2px solid #FFF;
    margin-left: -10px;
}
.avatar:first-child { margin-left: 0; background: #94A3B8; }
.avatar:nth-child(2) { background: #64748B; }
.avatar:nth-child(3) { background: #475569; }

/* Visual Cluster */
.saas-hero-visual {
    flex: 1;
    position: relative;
    height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.visual-card-main {
    background: #FFFFFF;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    width: 320px;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.08);
    border: 1px solid var(--border-subtle);
    z-index: 2;
    transform: rotate(-2deg);
}

.v-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 1rem;
}

.v-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--bg-base);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
}

.v-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    margin: 0.2rem;
}
.v-badge.blue { background: rgba(37, 99, 235, 0.1); color: var(--primary); }
.v-badge.outline { border: 1px solid var(--primary); color: var(--primary); }

.v-exp-item {
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
    margin-bottom: 0.5rem;
}

.visual-card-floating {
    position: absolute;
    background: #FFFFFF;
    border-radius: var(--radius-md);
    padding: 1rem;
    box-shadow: 0 15px 30px -5px rgba(0,0,0,0.1);
    border: 1px solid var(--border-subtle);
    z-index: 3;
}

.visual-card-floating.top-right {
    top: 20px;
    right: 20px;
    transform: rotate(3deg);
    width: 140px;
}

.visual-card-floating.bottom-right {
    bottom: 20px;
    right: 0px;
    width: 220px;
}

.v-score-circle {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    border: 5px solid var(--accent-emerald);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
}

.v-match-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.v-bar-bg {
    flex: 1;
    height: 6px;
    background: var(--bg-base);
    border-radius: 999px;
    overflow: hidden;
}

.v-bar-fill {
    height: 100%;
    border-radius: 999px;
}
.v-bar-fill.emerald { background: var(--accent-emerald); }
.v-bar-fill.purple { background: var(--accent-purple); }
.v-bar-fill.amber { background: var(--accent-amber); }

/* Features Grid */
.saas-features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.saas-feature-card {
    background: #FFFFFF;
    border-radius: var(--radius-md);
    padding: 1.5rem;
    border: 1px solid var(--border-subtle);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}

.saas-feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
}

.sf-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.sf-icon.blue { background: rgba(37, 99, 235, 0.1); color: var(--primary); }
.sf-icon.orange { background: rgba(245, 158, 11, 0.1); color: var(--accent-amber); }
.sf-icon.green { background: rgba(16, 185, 129, 0.1); color: var(--accent-emerald); }
.sf-icon.purple { background: rgba(139, 92, 246, 0.1); color: var(--accent-purple); }
.sf-icon.amber { background: rgba(245, 158, 11, 0.1); color: var(--accent-amber); }

.sf-content h3 {
    font-size: 1rem;
    margin-bottom: 0.4rem;
    color: var(--text-primary);
}

.sf-content p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.4;
    margin: 0;
}

.sf-arrow {
    margin-top: auto;
    color: var(--text-muted);
    font-size: 0.9rem;
}

/* Dashboard Summary */
.saas-dashboard-summary {
    display: flex;
    gap: 1.5rem;
    background: #FFFFFF;
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    flex-wrap: wrap;
    align-items: center;
}

.summary-welcome {
    flex: 1;
    min-width: 250px;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.summary-stats-grid {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.summary-stat-card {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem 1.2rem;
    background: var(--bg-base);
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-subtle);
}

.ss-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ss-icon.blue { background: rgba(37, 99, 235, 0.1); color: var(--primary); }
.ss-icon.green { background: rgba(16, 185, 129, 0.1); color: var(--accent-emerald); }
.ss-icon.purple { background: rgba(139, 92, 246, 0.1); color: var(--accent-purple); }
.ss-icon.orange { background: rgba(245, 158, 11, 0.1); color: var(--accent-amber); }

.ss-info {
    display: flex;
    flex-direction: column;
}

.ss-num {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
}

.ss-label {
    font-size: 0.7rem;
    color: var(--text-muted);
}

.summary-action-card {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: #F0Fdf4;
    border: 1px solid #BBF7D0;
    border-radius: var(--radius-md);
    min-width: 250px;
}

.sac-icon {
    width: 36px;
    height: 36px;
    background: #DCFCE7;
    color: #16A34A;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

/* Responsiveness */
@media (max-width: 992px) {
    .saas-hero {
        flex-direction: column;
        text-align: center;
    }
    .hero-badge { margin: 0 auto 1.5rem auto; }
    .hero-cta-group { justify-content: center; }
    .hero-trust { justify-content: center; }
}

@media (max-width: 768px) {
    .saas-hero-content h1 { font-size: 2.2rem; }
    .hero-cta-group { flex-direction: column; }
    .saas-dashboard-summary { flex-direction: column; align-items: stretch; }
    .summary-stats-grid { grid-template-columns: 1fr 1fr; display: grid; }
}
"""
    
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(saas_css)

append_saas_styles()
print('Appended SaaS styles.')

import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'

new_css = """
/* ==========================================================================
   ALUMNI HALL OF FAME REDESIGN
   ========================================================================== */

/* Hero Section */
.hof-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 3rem;
    padding: 3rem 0 4rem;
}

.hof-hero-left {
    flex: 1;
    max-width: 600px;
}

.h-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    color: #D97706; /* Gold/Amber */
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border: 1px solid var(--border-subtle);
}

.h-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1.25rem;
    letter-spacing: -0.02em;
}

.h-desc {
    font-size: 1.1rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Achievement Composition (Right Side) */
.hof-hero-right {
    position: relative;
    width: 420px;
    height: 320px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.h-achievement-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
}

.h-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(251,191,36,0.2) 0%, rgba(251,191,36,0) 70%);
    border-radius: 50%;
    z-index: 1;
}

.h-main-award {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2rem;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1);
    border: 1px solid rgba(251, 191, 36, 0.3);
    z-index: 2;
    min-width: 220px;
}

.h-award-icon {
    width: 72px;
    height: 72px;
    margin: 0 auto 1rem;
    background: linear-gradient(135deg, #FDE68A, #F59E0B);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
    box-shadow: 0 8px 16px rgba(245, 158, 11, 0.3);
}

.h-main-award h3 {
    font-size: 0.85rem;
    font-weight: 800;
    color: var(--text-secondary);
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

.h-award-score {
    font-size: 2.5rem;
    font-weight: 800;
    color: #D97706;
    line-height: 1;
}

.h-float-badge {
    position: absolute;
    background: white;
    padding: 0.6rem 1.25rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 10px 20px -5px rgba(0,0,0,0.08);
    border: 1px solid var(--border-glass);
    z-index: 3;
    color: var(--text-primary);
}
.h-float-badge.b-top { top: 20px; right: 20px; color: #4F46E5; }
.h-float-badge.b-bottom { bottom: 20px; left: 20px; color: #059669; }

/* Main Container */
.hof-main-container {
    background: white;
    border-radius: 24px;
    border: 1px solid var(--border-subtle);
    padding: 2.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 2rem;
}

.hof-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.hof-header-left { display: flex; align-items: center; gap: 1.25rem; }
.hof-icon { width: 48px; height: 48px; background: #FFFBEB; color: #D97706; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.hof-title { font-size: 1.35rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary); }
.hof-sub { font-size: 0.95rem; color: var(--text-secondary); margin: 0; }

.hof-filters {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.h-search-wrap {
    flex: 1;
    min-width: 280px;
    position: relative;
    display: flex;
    align-items: center;
}
.h-search-wrap i { position: absolute; left: 1rem; color: var(--text-muted); }
.h-search-wrap input { width: 100%; padding: 0.75rem 1rem 0.75rem 2.5rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); font-size: 0.9rem; background: #F8FAFC; }
.h-search-wrap input:focus { outline: none; border-color: var(--primary); background: white; }

.h-select { padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--border-color); font-size: 0.9rem; background: #F8FAFC; color: var(--text-primary); cursor: pointer; }
.h-select:focus { outline: none; border-color: var(--primary); }

/* Alumni Grid */
.hof-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}

.hof-card {
    background: white;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    padding: 1.5rem;
    transition: all 0.25s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
}
.hof-card:hover {
    transform: translateY(-3px);
    border-color: #BFDBFE;
    box-shadow: 0 12px 24px -8px rgba(37,99,235,0.15);
}

.hc-header {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    position: relative;
}

.hc-rank-ribbon {
    position: absolute;
    top: -0.5rem;
    left: -0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 28px;
    padding: 0.4rem 0;
    border-radius: 4px;
    color: white;
    font-size: 0.7rem;
    font-weight: 800;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    z-index: 2;
}
.hc-rank-ribbon.rank-gold { background: linear-gradient(135deg, #FCD34D, #F59E0B); }
.hc-rank-ribbon.rank-silver { background: linear-gradient(135deg, #E2E8F0, #94A3B8); }
.hc-rank-ribbon.rank-bronze { background: linear-gradient(135deg, #FDBA74, #D97706); }
.hc-rank-ribbon.rank-neutral { background: #CBD5E1; }
.hc-rank-ribbon i { font-size: 0.8rem; margin-bottom: 2px; }

.hc-avatar-wrap { position: relative; margin-left: 1rem; }
.hc-avatar { width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, #E0E7FF, #C7D2FE); color: #4F46E5; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; font-weight: 700; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }

.hc-user-info { flex: 1; }
.hc-name { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.2rem; }
.hc-role { font-size: 0.75rem; color: var(--text-secondary); line-height: 1.3; }
.hc-role strong { color: var(--text-primary); }
.hc-package { font-size: 0.75rem; color: #059669; font-weight: 600; margin-top: 0.25rem; }

.hc-score-ring { width: 48px; height: 48px; flex-shrink: 0; }
.circular-chart { display: block; margin: 0 auto; max-width: 100%; max-height: 250px; }
.circle-bg { fill: none; stroke: #F1F5F9; stroke-width: 3.8; }
.circle { fill: none; stroke-width: 2.8; stroke-linecap: round; }
.circular-chart.green .circle { stroke: #10B981; }
.percentage { fill: #10B981; font-family: sans-serif; font-size: 0.5em; text-anchor: middle; font-weight: 800; }

.hc-divider { height: 1px; background: var(--border-color); margin: 1.25rem 0; }

.hc-challenge-info { flex: 1; margin-bottom: 1.25rem; }
.hc-chal-title { display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.85rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.75rem; line-height: 1.3; }
.hc-chal-title i { color: #D97706; margin-top: 0.1rem; }

.hc-skills { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.h-skill-chip { background: #F1F5F9; color: var(--text-secondary); font-size: 0.7rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 999px; }

.hc-btn-solve {
    width: 100%;
    background: #EFF6FF;
    color: #2563EB;
    border: none;
    padding: 0.85rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
.hc-btn-solve i.fa-arrow-right { margin-left: auto; transition: transform 0.2s ease; }
.hc-btn-solve:hover { background: linear-gradient(135deg, #2563EB, #8B5CF6); color: white; }
.hc-btn-solve:hover i.fa-arrow-right { transform: translateX(3px); }

/* Responsive */
@media (max-width: 1024px) {
    .hof-hero { flex-direction: column; text-align: center; }
    .hof-hero-right { margin-top: 2rem; }
    .hof-grid { grid-template-columns: repeat(2, 1fr); }
    .hof-header { flex-direction: column; align-items: flex-start; }
}
@media (max-width: 768px) {
    .hof-grid { grid-template-columns: 1fr; }
    .hof-filters { flex-direction: column; }
    .h-search-wrap, .h-select { width: 100%; }
}
"""

with open(filepath, 'a', encoding='utf-8') as f:
    f.write(new_css)
print("CSS appended to style.css")

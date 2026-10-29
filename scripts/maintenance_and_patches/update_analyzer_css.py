import os

css_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'

new_css = """
/* ==========================================================================
   AI RESUME PDF ANALYZER REDESIGN
   ========================================================================== */

/* Hero Section */
.analyzer-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 3rem;
    padding: 3.5rem 2.5rem;
    background: linear-gradient(135deg, rgba(239, 246, 255, 0.6) 0%, rgba(245, 243, 255, 0.4) 100%);
    border-radius: var(--radius-lg);
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.8);
    box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.6);
}

.analyzer-hero-left {
    flex: 1;
    max-width: 600px;
}

.a-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: white;
    color: var(--primary);
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.4rem 0.8rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    border: 1px solid var(--border-subtle);
}

.a-title {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1.25rem;
    letter-spacing: -0.02em;
}

.a-desc {
    font-size: 1.05rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

.analyzer-hero-right {
    position: relative;
    width: 450px;
    height: 280px;
    perspective: 1000px;
}

.a-float-card {
    position: absolute;
    background: white;
    border-radius: var(--radius-md);
    padding: 1.5rem;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
    border: 1px solid var(--border-glass);
    transition: transform 0.3s ease;
}

.a-float-card.ats-card {
    top: 20px;
    left: 0;
    width: 180px;
    z-index: 2;
    transform: translateZ(20px);
}

.a-float-card.company-card {
    top: -10px;
    right: 0;
    width: 280px;
    z-index: 1;
    transform: translateZ(0);
}

.c-match-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.8rem;
}
.c-match-row:last-child {
    margin-bottom: 0;
}

.c-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
}

.c-info {
    display: flex;
    flex-direction: column;
}

.c-name {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-primary);
}

.c-score {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Main Grid */
.analyzer-main-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
}

/* Upload Panel */
.upload-panel {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-subtle);
    padding: 2.5rem;
    box-shadow: var(--shadow-sm);
}

.upload-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 2rem;
}

.u-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    border: 1px solid transparent;
}
.u-chip.red { background: rgba(239, 68, 68, 0.1); color: #EF4444; border-color: rgba(239, 68, 68, 0.2); }
.u-chip.green { background: rgba(16, 185, 129, 0.1); color: #10B981; border-color: rgba(16, 185, 129, 0.2); }
.u-chip.blue { background: rgba(59, 130, 246, 0.1); color: #3B82F6; border-color: rgba(59, 130, 246, 0.2); }
.u-chip.purple { background: rgba(139, 92, 246, 0.1); color: #8B5CF6; border-color: rgba(139, 92, 246, 0.2); }

.upload-dropzone {
    border: 2px dashed #93C5FD;
    border-radius: var(--radius-md);
    background: #F8FAFC;
    padding: 4rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-bottom: 2rem;
}
.upload-dropzone:hover {
    background: #EFF6FF;
    border-color: var(--primary);
}

.dz-icon {
    width: 64px;
    height: 64px;
    background: white;
    color: var(--primary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin: 0 auto 1.25rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dz-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.dz-sub {
    font-size: 0.95rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}

.dz-link {
    color: var(--primary);
    font-weight: 600;
    text-decoration: underline;
}

.dz-meta {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.upload-actions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.btn-gradient {
    background: linear-gradient(135deg, #2563EB, #8B5CF6);
    border: none;
    padding: 0.8rem 1.5rem;
    color: white;
    font-weight: 600;
}
.btn-gradient:hover {
    opacity: 0.95;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* Info Panel */
.info-panel {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-subtle);
    padding: 2rem;
    box-shadow: var(--shadow-sm);
}

.info-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.info-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.info-row:last-child { margin-bottom: 0; }

.info-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.info-icon.blue { background: #EFF6FF; color: #3B82F6; }
.info-icon.green { background: #ECFDF5; color: #10B981; }
.info-icon.purple { background: #F5F3FF; color: #8B5CF6; }
.info-icon.orange { background: #FFF7ED; color: #F59E0B; }

.info-text h4 {
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    color: var(--text-primary);
}
.info-text p {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.4;
    margin: 0;
}

/* Stats Row */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-subtle);
    padding: 1.5rem;
    display: flex;
    gap: 1rem;
    box-shadow: var(--shadow-sm);
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
}
.stat-icon.blue { background: #EFF6FF; color: #3B82F6; }
.stat-icon.green { background: #ECFDF5; color: #10B981; }
.stat-icon.purple { background: #F5F3FF; color: #8B5CF6; }
.stat-icon.orange { background: #FFF7ED; color: #F59E0B; }

.stat-content h3 {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
    line-height: 1;
}

.stat-content p {
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.3;
    margin: 0;
}
.stat-content p strong {
    color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
    .analyzer-main-grid { grid-template-columns: 1fr; }
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .analyzer-hero { flex-direction: column; text-align: center; }
    .analyzer-hero-left { max-width: 100%; }
    .analyzer-hero-right { margin-top: 2rem; width: 100%; max-width: 450px; }
}

@media (max-width: 768px) {
    .stats-row { grid-template-columns: 1fr; }
    .upload-actions { flex-direction: column; align-items: stretch; }
    .a-title { font-size: 2.2rem; }
}
"""

with open(css_filepath, 'a', encoding='utf-8') as f:
    f.write(new_css)
print("CSS applied.")

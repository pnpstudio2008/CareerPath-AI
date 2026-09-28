import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'

new_css = """
/* ==========================================================================
   MOCK TEST PLATFORM REDESIGN
   ========================================================================== */

/* Hero */
.mocktest-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 3rem;
    padding: 3rem 0 4rem;
}

.mocktest-hero-left {
    flex: 1;
    max-width: 600px;
}

.m-badge {
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

.m-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 1.25rem;
    letter-spacing: -0.02em;
}

.m-desc {
    font-size: 1.1rem;
    color: var(--text-secondary);
    line-height: 1.6;
}

.mocktest-hero-right {
    position: relative;
    width: 480px;
    height: 320px;
}

/* Abstract CSS Composition */
.m-abstract-card {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 280px;
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: 0 24px 48px -12px rgba(0,0,0,0.12);
    border: 1px solid var(--border-glass);
    overflow: hidden;
    z-index: 2;
}

.m-abs-header {
    background: linear-gradient(135deg, #1E1B4B, #312E81);
    color: white;
    padding: 1rem 1.25rem;
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.m-abs-body {
    padding: 1.5rem;
    background: #F8FAFC;
}

.m-abs-line { height: 8px; background: #E2E8F0; border-radius: 4px; margin-bottom: 1rem; }
.m-abs-line.short { width: 60%; }
.m-abs-line.shorter { width: 40%; margin-bottom: 0; }

.m-abs-footer {
    padding: 1rem 1.5rem;
    display: flex;
    gap: 0.5rem;
    background: white;
    border-top: 1px solid var(--border-subtle);
}

.m-abs-tag {
    background: #EFF6FF;
    color: #2563EB;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
}
.m-abs-tag.outline {
    background: white;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
}

.m-float-card {
    position: absolute;
    background: white;
    border-radius: 999px;
    padding: 0.6rem 1.25rem;
    font-weight: 600;
    font-size: 0.85rem;
    box-shadow: 0 12px 24px -6px rgba(0,0,0,0.08);
    border: 1px solid var(--border-glass);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    z-index: 3;
}
.m-float-card.fc-1 { top: 20px; left: 20px; }
.m-float-card.fc-2 { top: 60px; right: 0; }
.m-float-card.fc-3 { bottom: 40px; right: 40px; }

/* Main Configuration Card */
.mocktest-main-card {
    background: white;
    border-radius: 24px;
    border: 1px solid var(--border-subtle);
    padding: 2.5rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 2rem;
}

.m-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 2.5rem;
}

.m-header-left {
    display: flex;
    gap: 1.25rem;
}

.m-header-icon {
    width: 48px;
    height: 48px;
    background: #EEF2FF;
    color: #4F46E5;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}

.m-header-title { font-size: 1.35rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary); }
.m-header-sub { font-size: 0.95rem; color: var(--text-secondary); margin: 0; max-width: 500px; }

.m-header-right {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    background: #F5F3FF;
    border: 1px solid #E0E7FF;
    padding: 0.85rem 1.25rem;
    border-radius: 12px;
    max-width: 320px;
}
.m-header-right i { color: #8B5CF6; margin-top: 0.2rem; }
.m-header-right strong { display: block; color: #4C1D95; font-size: 0.85rem; font-weight: 700; }
.m-header-right span { color: #6D28D9; font-size: 0.75rem; line-height: 1.3; display: block; }

.m-config-grid {
    display: grid;
    grid-template-columns: 60% 35%;
    gap: 5%;
}

.m-step-group {
    margin-bottom: 2rem;
}

.m-step-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.m-step-number {
    width: 28px;
    height: 28px;
    background: var(--primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
}

.m-step-header h4 { font-size: 1.05rem; font-weight: 700; margin-bottom: 0.2rem; color: var(--text-primary); }
.m-step-header p { font-size: 0.85rem; color: var(--text-secondary); margin: 0; }

.m-step-content {
    padding-left: calc(28px + 1rem);
}

/* Skill Chips */
#mocktest-tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}

.m-skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.m-skill-chip.selected {
    background: #EFF6FF;
    color: #2563EB;
    border-color: #BFDBFE;
}
.m-skill-chip.unselected {
    background: white;
    color: var(--text-secondary);
    border-color: var(--border-color);
}
.m-skill-chip.unselected:hover { border-color: var(--primary); color: var(--primary); }

.m-skill-chip.custom {
    background: white;
    color: var(--primary);
    border-color: #BFDBFE;
    border-style: dashed;
}
.m-skill-chip.custom:hover { background: #EFF6FF; }

/* Mini Upload */
.m-mini-upload {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    background: #F8FAFC;
    border: 1px dashed #CBD5E1;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s ease;
}
.m-mini-upload:hover { border-color: var(--primary); background: white; }
.m-mini-upload-left { display: flex; align-items: center; gap: 1rem; }
.m-mini-icon { width: 40px; height: 40px; background: white; color: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-sm); }
.m-mini-upload-left strong { display: block; font-size: 0.9rem; color: var(--text-primary); }
.m-mini-upload-left span { display: block; font-size: 0.8rem; color: var(--text-secondary); }

/* Settings */
.m-settings-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.m-setting-item label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.m-select {
    width: 100%;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border-color);
    background: #F8FAFC;
    color: var(--text-primary);
    font-size: 0.9rem;
    cursor: pointer;
    transition: border-color 0.2s ease;
}
.m-select:focus { border-color: var(--primary); outline: none; background: white; }

.m-btn-start {
    width: 100%;
    margin-top: 3rem;
    background: linear-gradient(135deg, #2563EB, #8B5CF6);
    color: white;
    border: none;
    border-radius: var(--radius-md);
    padding: 1.25rem;
    font-size: 1.1rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    cursor: pointer;
    box-shadow: 0 10px 25px -5px rgba(37,99,235,0.3);
    transition: all 0.3s ease;
}
.m-btn-start:hover { transform: translateY(-2px); box-shadow: 0 15px 30px -5px rgba(37,99,235,0.4); }

/* Bottom Features */
.m-features-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-top: 2rem;
}

.m-feature-card {
    background: white;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-glass);
    padding: 1.5rem;
    display: flex;
    gap: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
}

.m-feat-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.m-feat-icon.green { background: #ECFDF5; color: #10B981; }
.m-feat-icon.blue { background: #EFF6FF; color: #3B82F6; }
.m-feat-icon.orange { background: #FFF7ED; color: #F59E0B; }
.m-feat-icon.purple { background: #F5F3FF; color: #8B5CF6; }

.m-feat-text h4 { font-size: 0.9rem; font-weight: 700; margin-bottom: 0.25rem; color: var(--text-primary); }
.m-feat-text p { font-size: 0.8rem; color: var(--text-secondary); margin: 0; line-height: 1.4; }

/* Responsive */
@media (max-width: 1024px) {
    .mocktest-hero { flex-direction: column; text-align: center; }
    .mocktest-hero-right { margin: 2rem auto 0; }
    .m-config-grid { grid-template-columns: 1fr; gap: 3rem; }
    .m-features-row { grid-template-columns: repeat(2, 1fr); }
    .m-card-header { flex-direction: column; gap: 1.5rem; }
}

@media (max-width: 768px) {
    .m-features-row { grid-template-columns: 1fr; }
    .m-mini-upload { flex-direction: column; align-items: stretch; gap: 1rem; text-align: center; }
    .m-mini-upload-left { flex-direction: column; }
    .m-title { font-size: 2.2rem; }
}
"""

with open(filepath, 'a', encoding='utf-8') as f:
    f.write(new_css)
print("Added Mock Test CSS.")

import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'

new_css = """
/* ==========================================================================
   ALUMNI PORTAL DASHBOARD REDESIGN
   ========================================================================== */

/* Premium Hero */
.alumni-premium-hero {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px -10px rgba(37,99,235,0.15);
    border: 1px solid rgba(255, 255, 255, 0.8);
    background: #ffffff;
}

.ap-hero-bg {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(120deg, #F0F9FF 0%, #E0E7FF 50%, #F5F3FF 100%);
    opacity: 0.8;
    z-index: 1;
}

.ap-hero-bg::after {
    content: '';
    position: absolute;
    top: -50%; left: 50%;
    width: 1000px; height: 1000px;
    background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
    transform: translate(-50%, -20%);
}

.ap-hero-content {
    position: relative;
    z-index: 2;
    padding: 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 2rem;
    flex-wrap: wrap;
}

.ap-profile-main {
    display: flex;
    align-items: center;
    gap: 2rem;
    flex: 1;
    min-width: 300px;
}

.ap-avatar {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #8B5CF6);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 800;
    border: 4px solid white;
    box-shadow: 0 12px 24px -8px rgba(59,130,246,0.4);
    flex-shrink: 0;
}

.ap-name-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
}

.ap-name {
    font-size: 2rem;
    font-weight: 800;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.02em;
}

.ap-verified-badge {
    background: #ECFDF5;
    color: #059669;
    border: 1px solid #A7F3D0;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.ap-chips-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-bottom: 1.25rem;
}

.ap-chip {
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(203, 213, 225, 0.5);
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #475569;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    backdrop-filter: blur(4px);
}

.ap-actions-row { display: flex; gap: 1rem; flex-wrap: wrap; }

.ap-btn-primary {
    background: linear-gradient(135deg, #0A66C2, #004182);
    color: white;
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(10,102,194,0.2);
    transition: all 0.2s ease;
}
.ap-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(10,102,194,0.3); color: white; }

.ap-btn-secondary {
    background: white;
    color: #3B82F6;
    border: 1px solid #BFDBFE;
    padding: 0.6rem 1.25rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    transition: all 0.2s ease;
}
.ap-btn-secondary:hover { background: #F8FAFC; border-color: #93C5FD; color: #2563EB; }

.ap-quote-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    max-width: 280px;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
    border: 1px solid var(--border-subtle);
    position: relative;
}
.ap-quote-icon { position: absolute; top: -10px; left: -10px; background: #3B82F6; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; box-shadow: 0 4px 6px rgba(59,130,246,0.3); }
.ap-quote-text { font-size: 0.95rem; font-weight: 600; color: #1E293B; line-height: 1.4; margin: 0 0 1rem 0; font-style: italic; }
.ap-quote-label { font-size: 0.75rem; font-weight: 700; color: #8B5CF6; display: flex; align-items: center; gap: 0.4rem; }

/* Metrics Row */
.ap-metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
    margin-bottom: 2rem;
}

.ap-metric-card {
    background: white;
    border-radius: 16px;
    border: 1px solid var(--border-subtle);
    padding: 1.25rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 140px;
    transition: transform 0.2s ease;
}
.ap-metric-card:hover { transform: translateY(-3px); box-shadow: 0 12px 24px -8px rgba(0,0,0,0.08); }

.ap-metric-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }
.ap-m-icon { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; }
.ap-m-label { font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); flex: 1; }
.ap-m-arrow { color: #CBD5E1; font-size: 0.75rem; }

.ap-metric-body { position: relative; }
.ap-m-value { font-size: 2.2rem; font-weight: 800; color: var(--text-primary); margin: 0 0 0.25rem 0; line-height: 1; }
.ap-m-trend { font-size: 0.75rem; font-weight: 700; display: inline-flex; align-items: center; gap: 0.2rem; }
.ap-m-trend.neutral { color: #94A3B8; }

.ap-sparkline {
    position: absolute;
    bottom: -10px;
    right: -10px;
    width: 60px;
    height: 30px;
    background-size: 100% 100%;
    opacity: 0.6;
}
.ap-sparkline.red { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40'%3E%3Cpath d='M0 30 Q20 10, 40 30 T80 10 L100 20 L100 40 L0 40 Z' fill='rgba(239,68,68,0.1)'/%3E%3Cpath d='M0 30 Q20 10, 40 30 T80 10 L100 20' fill='none' stroke='%23EF4444' stroke-width='2'/%3E%3C/svg%3E"); }
.ap-sparkline.blue { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40'%3E%3Cpath d='M0 20 Q30 30, 50 10 T100 20 L100 40 L0 40 Z' fill='rgba(59,130,246,0.1)'/%3E%3Cpath d='M0 20 Q30 30, 50 10 T100 20' fill='none' stroke='%233B82F6' stroke-width='2'/%3E%3C/svg%3E"); }
.ap-sparkline.green { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40'%3E%3Cpath d='M0 35 Q20 5, 50 25 T100 15 L100 40 L0 40 Z' fill='rgba(16,185,129,0.1)'/%3E%3Cpath d='M0 35 Q20 5, 50 25 T100 15' fill='none' stroke='%2310B981' stroke-width='2'/%3E%3C/svg%3E"); }
.ap-sparkline.purple { background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 40'%3E%3Cpath d='M0 10 Q25 40, 60 20 T100 10 L100 40 L0 40 Z' fill='rgba(139,92,246,0.1)'/%3E%3Cpath d='M0 10 Q25 40, 60 20 T100 10' fill='none' stroke='%238B5CF6' stroke-width='2'/%3E%3C/svg%3E"); }

/* Dashboard Grid */
.ap-dashboard-grid {
    display: grid;
    grid-template-columns: 2fr 1.2fr 1fr;
    gap: 1.5rem;
}

.ap-panel {
    background: white;
    border-radius: 20px;
    border: 1px solid var(--border-subtle);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}

.ap-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.ap-panel-title { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); display: flex; align-items: center; gap: 0.5rem; }

.ap-panel-actions { display: flex; align-items: center; gap: 1rem; }
.ap-verified-badge.small { padding: 0.2rem 0.6rem; font-size: 0.7rem; }

.ap-btn-edit { background: white; border: 1px solid #E2E8F0; color: #475569; padding: 0.35rem 0.75rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s ease; }
.ap-btn-edit:hover { background: #F8FAFC; border-color: #CBD5E1; color: #0F172A; }

/* Profile Table */
.ap-profile-table {
    display: flex;
    flex-direction: column;
}
.ap-row {
    display: flex;
    justify-content: space-between;
    padding: 0.85rem 0;
    border-bottom: 1px solid #F1F5F9;
}
.ap-row:last-child { border-bottom: none; }
.ap-label { color: var(--text-secondary); font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }
.ap-val { color: var(--text-primary); font-size: 0.85rem; font-weight: 500; text-align: right; }

/* Donut Chart */
.ap-donut-container { position: relative; width: 100%; max-width: 200px; margin: 0 auto 1.5rem; }
.ap-donut-svg { width: 100%; height: auto; transform: rotate(-90deg); }
.ap-donut-bg { fill: none; stroke: #F1F5F9; stroke-width: 4; }
.ap-donut-segment { fill: none; stroke-width: 4; stroke-linecap: round; transition: stroke-dasharray 1s ease; }
.ap-donut-segment.red { stroke: #EF4444; }
.ap-donut-segment.blue { stroke: #3B82F6; }

.ap-donut-center {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    text-align: center;
}
.ap-donut-center strong { display: block; font-size: 2rem; font-weight: 800; color: var(--text-primary); line-height: 1; }
.ap-donut-center span { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; display: block; margin-top: 0.2rem; }

.ap-chart-legend { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 1rem; }
.ap-legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); }
.ap-legend-item span { margin-left: auto; color: var(--text-secondary); font-weight: 500; }
.ap-dot { width: 8px; height: 8px; border-radius: 50%; }
.ap-dot.red { background: #EF4444; }
.ap-dot.blue { background: #3B82F6; }
.ap-chart-sub { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; margin: 0; }

/* Activity Panel */
.ap-icon-btn { color: #CBD5E1; cursor: pointer; }
.ap-icon-btn:hover { color: #64748B; }

.ap-activity-feed { display: flex; flex-direction: column; gap: 1rem; }
.ap-activity-empty { display: flex; flex-direction: column; align-items: center; text-align: center; color: var(--text-muted); padding: 2rem 0; }
.ap-activity-empty i { font-size: 2rem; margin-bottom: 1rem; color: #E2E8F0; }
.ap-activity-empty span { font-size: 0.9rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.2rem; }
.ap-activity-empty small { font-size: 0.75rem; }

.ap-activity-item { display: flex; align-items: flex-start; gap: 0.85rem; padding: 0.75rem; background: #F8FAFC; border-radius: 12px; border: 1px solid transparent; transition: border-color 0.2s ease; cursor: default; }
.ap-activity-item:hover { border-color: #E2E8F0; }
.ap-act-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0; }
.ap-act-icon.red { background: #FEE2E2; color: #EF4444; }
.ap-act-icon.blue { background: #DBEAFE; color: #3B82F6; }
.ap-act-info strong { display: block; font-size: 0.85rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.1rem; }
.ap-act-info span { font-size: 0.75rem; color: var(--text-secondary); }

/* Responsive Adjustments */
@media (max-width: 1200px) {
    .ap-dashboard-grid { grid-template-columns: 1fr 1fr; }
    .ap-activity-panel { grid-column: span 2; }
    .ap-activity-feed { flex-direction: row; flex-wrap: wrap; }
    .ap-activity-item { flex: 1; min-width: 200px; }
}

@media (max-width: 1024px) {
    .ap-metrics-grid { grid-template-columns: repeat(2, 1fr); }
    .ap-profile-main { flex-direction: column; text-align: center; }
    .ap-name-row, .ap-chips-row, .ap-actions-row { justify-content: center; }
    .ap-hero-content { flex-direction: column; }
}

@media (max-width: 768px) {
    .ap-dashboard-grid { grid-template-columns: 1fr; }
    .ap-activity-panel { grid-column: auto; }
    .ap-activity-feed { flex-direction: column; }
    .ap-row { flex-direction: column; text-align: left; gap: 0.25rem; padding: 0.6rem 0; }
    .ap-val { text-align: left; }
    .ap-hero-content { padding: 1.5rem; }
    .ap-quote-card { max-width: 100%; width: 100%; }
}
"""

with open(filepath, 'a', encoding='utf-8') as f:
    f.write(new_css)
print("CSS appended to style.css")

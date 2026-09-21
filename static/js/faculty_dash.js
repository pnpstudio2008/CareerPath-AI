/**
 * AI Career Companion - Faculty Analytics Dashboard (Module 5)
 */

let subjectChartInstance = null;
let tierChartInstance = null;

async function initFacultyDashboard() {
    try {
        const res = await fetch('/api/faculty/insights');
        const data = await res.json();

        if (!data.success) return;

        const stats = data.stats;

        // 1. KPI Cards
        const totalStudents = document.getElementById('faculty-total-students');
        if (totalStudents) totalStudents.innerText = stats.total_students_enrolled;

        const resumesEval = document.getElementById('faculty-resumes-evaluated');
        if (resumesEval) resumesEval.innerText = stats.resumes_evaluated;

        const readyPct = document.getElementById('faculty-ready-pct');
        if (readyPct) readyPct.innerText = `${stats.placement_ready_pct}%`;

        const avgAts = document.getElementById('faculty-avg-ats');
        if (avgAts) avgAts.innerText = stats.average_ats_score;

        // 2. Skill Gap Heatmap Table
        const tbody = document.getElementById('faculty-heatmap-tbody');
        if (tbody) {
            tbody.innerHTML = '';
            stats.skill_gap_heatmap.forEach(item => {
                const tr = document.createElement('tr');
                const severityClass = item.severity === 'High' ? 'badge-danger' : item.severity === 'Medium' ? 'badge-warning' : 'badge-info';
                tr.innerHTML = `
                    <td><strong>${item.skill}</strong></td>
                    <td>
                        <div class="card-header-flex" style="margin:0; gap:0.5rem;">
                            <span>${item.gap_percentage}%</span>
                            <div class="progress-bar-bg" style="width: 100px; margin:0;">
                                <div class="progress-bar-fill" style="width: ${item.gap_percentage}%; background:${item.severity === 'High' ? 'var(--accent-rose)' : 'var(--accent-amber)'};"></div>
                            </div>
                        </div>
                    </td>
                    <td><span class="badge ${severityClass}">${item.severity}</span></td>
                    <td style="font-size:0.86rem; color:var(--text-secondary);">${item.recommendation}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        // 3. Render Chart.js Visualizations
        renderFacultyCharts(stats);

    } catch (err) {
        console.warn('Error loading faculty insights:', err);
    }
}

function renderFacultyCharts(stats) {
    const isDark = (document.documentElement.getAttribute('data-theme') === 'dark');
    const textColor = isDark ? '#94A3B8' : '#475569';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';

    // Subject Performance Bar Chart
    const subjectCanvas = document.getElementById('facultySubjectChart');
    if (subjectCanvas) {
        if (subjectChartInstance) subjectChartInstance.destroy();

        const labels = stats.subject_performance.map(s => s.subject);
        const scores = stats.subject_performance.map(s => s.avg_score);

        subjectChartInstance = new Chart(subjectCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Class Average Score (%)',
                    data: scores,
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.75)',
                        'rgba(6, 182, 212, 0.75)',
                        'rgba(16, 185, 129, 0.75)',
                        'rgba(139, 92, 246, 0.75)'
                    ],
                    borderColor: [
                        '#6366F1',
                        '#06B6D4',
                        '#10B981',
                        '#8B5CF6'
                    ],
                    borderWidth: 1.5,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } },
                        grid: { color: gridColor }
                    },
                    y: {
                        min: 0,
                        max: 100,
                        ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    }

    // Tier Readiness Doughnut Chart
    const tierCanvas = document.getElementById('facultyTierChart');
    if (tierCanvas) {
        if (tierChartInstance) tierChartInstance.destroy();

        const tierLabels = Object.keys(stats.company_tier_distribution);
        const tierValues = Object.values(stats.company_tier_distribution);

        tierChartInstance = new Chart(tierCanvas, {
            type: 'doughnut',
            data: {
                labels: tierLabels,
                datasets: [{
                    data: tierValues,
                    backgroundColor: [
                        '#8B5CF6', // Product
                        '#6366F1', // Dream
                        '#06B6D4'  // Mass
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } }
                    }
                }
            }
        });
    }
}

import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\js\resume_analyzer.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the end of `document.getElementById('ats-feedback-text').innerText = ats.feedback_summary;`
# and insert my logic there.

logic = """document.getElementById('ats-feedback-text').innerText = ats.feedback_summary;

    // --- UPDATE HERO CARDS DYNAMICALLY ---
    const heroScore = document.getElementById('hero-ats-score');
    const heroCircle = document.getElementById('hero-ats-circle');
    const heroLabel = document.getElementById('hero-ats-label');
    
    if (heroScore && heroCircle && heroLabel) {
        heroScore.innerText = ats.ats_score;
        heroCircle.style.borderColor = ats.rating_color;
        
        let trendIcon = '<i class="fa-solid fa-arrow-trend-up"></i>';
        if (ats.ats_score < 50) trendIcon = '<i class="fa-solid fa-arrow-trend-down"></i>';
        else if (ats.ats_score < 75) trendIcon = '<i class="fa-solid fa-minus"></i>';
        
        heroLabel.innerHTML = `${trendIcon} ${ats.rating}`;
        heroLabel.style.color = ats.rating_color;
    }

    // Update Company hero card if benchmark data is available
    if (data.cohort_benchmark && data.cohort_benchmark.length > 0) {
        const heroCompany = document.getElementById('hero-company-matches');
        if (heroCompany) {
            heroCompany.innerHTML = ''; // clear placeholders
            // Take top 4 matches
            data.cohort_benchmark.slice(0, 4).forEach(comp => {
                let badgeColor = '#EF4444'; // Red default
                let bgBadgeColor = 'rgba(239,68,68,0.1)';
                if (comp.match_score >= 80) { badgeColor = '#10B981'; bgBadgeColor = 'rgba(16,185,129,0.1)'; }
                else if (comp.match_score >= 60) { badgeColor = '#3B82F6'; bgBadgeColor = 'rgba(59,130,246,0.1)'; }
                else if (comp.match_score >= 40) { badgeColor = '#F59E0B'; bgBadgeColor = 'rgba(245,158,11,0.1)'; }
                
                const html = `
                    <div class="c-match-row">
                        <div class="c-icon" style="color: ${badgeColor}; background: ${bgBadgeColor};">${comp.company.charAt(0).toUpperCase()}</div>
                        <div class="c-info">
                            <span class="c-name" style="color:var(--text-primary);">${comp.company}</span>
                            <span class="c-score" style="color:var(--text-secondary);">${comp.match_score}% Match</span>
                        </div>
                    </div>
                `;
                heroCompany.insertAdjacentHTML('beforeend', html);
            });
        }
    }
    // ------------------------------------"""

content = content.replace("document.getElementById('ats-feedback-text').innerText = ats.feedback_summary;", logic)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated resume_analyzer.js")

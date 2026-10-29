import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\js\alumni_hub.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """function renderAlumniExperiences(experiences) {
    window.AppState.allAlumniExperiences = experiences;
    const feed = document.getElementById('alumni-feed-container');
    if (!feed) return;
    feed.innerHTML = '';

    experiences.forEach((exp, index) => {
        const card = document.createElement('div');
        card.className = 'hof-card';
        
        // Generate mock rank (1, 2, 3...)
        const rank = index + 1;
        let rankClass = 'rank-neutral';
        let rankIcon = '<i class="fa-solid fa-medal"></i>';
        if (rank === 1) { rankClass = 'rank-gold'; rankIcon = '<i class="fa-solid fa-crown"></i>'; }
        else if (rank === 2) { rankClass = 'rank-silver'; }
        else if (rank === 3) { rankClass = 'rank-bronze'; }

        const initials = getInitials(exp.student_name);
        
        // Use realistic dummy skills for the challenge test if none exist
        const challengeSkills = exp.difficulty === 'Hard' ? ['DSA', 'System Design', 'OS'] : ['DSA', 'OOP', 'Database'];
        const skillsHtml = challengeSkills.map(s => `<span class="h-skill-chip">${s}</span>`).join('');
        
        // Format package if exists
        const packageInfo = exp.package_lpa ? `<div class="hc-package">₹${exp.package_lpa} LPA</div>` : '';

        card.innerHTML = `
            <div class="hc-header">
                <div class="hc-rank-ribbon ${rankClass}">
                    ${rankIcon}
                    <span>${rank}</span>
                </div>
                
                <div class="hc-avatar-wrap">
                    <div class="hc-avatar">${initials}</div>
                </div>
                
                <div class="hc-user-info">
                    <h4 class="hc-name">${exp.student_name}</h4>
                    <div class="hc-role">${exp.role} at <strong>${exp.company}</strong></div>
                    ${packageInfo}
                </div>
                
                <div class="hc-score-ring">
                    <svg viewBox="0 0 36 36" class="circular-chart green">
                        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <path class="circle" stroke-dasharray="100, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                        <text x="18" y="20.35" class="percentage">100%</text>
                    </svg>
                </div>
            </div>
            
            <div class="hc-divider"></div>
            
            <div class="hc-challenge-info">
                <div class="hc-chal-title">
                    <i class="fa-solid fa-trophy"></i>
                    <span>${exp.company} ${exp.role} Placement Challenge</span>
                </div>
                <div class="hc-skills">
                    ${skillsHtml}
                </div>
            </div>
            
            <button class="hc-btn-solve" onclick="startAlumniChallenge('${exp.company}', '${exp.role}')">
                <i class="fa-solid fa-play"></i> Solve ${exp.student_name.split(' ')[0]}'s Test <i class="fa-solid fa-arrow-right"></i>
            </button>
        `;
        feed.appendChild(card);
    });
}

// Add the wrapper function for starting the challenge
window.startAlumniChallenge = function(company, role) {
    if (typeof navigateTo === 'function') navigateTo('mocktest');
    
    // Set the dropdowns if they exist
    const roleSelect = document.getElementById('mocktest-role-select');
    if (roleSelect) {
        // Try to find a matching option, else just pick first
        let matched = false;
        for (let i = 0; i < roleSelect.options.length; i++) {
            if (roleSelect.options[i].text.toLowerCase().includes(role.toLowerCase())) {
                roleSelect.selectedIndex = i;
                matched = true;
                break;
            }
        }
    }
    
    // Overwrite skills
    if (typeof mockActiveSkills !== 'undefined') {
        mockActiveSkills = ['DSA', 'System Design', 'OOP', 'Database'];
        if (typeof updateMockSkillsPreview === 'function') updateMockSkillsPreview();
    }
    
    // Optional: Start automatically after 500ms
    setTimeout(() => {
        if (typeof generateAndStartMockTest === 'function') {
            generateAndStartMockTest();
        }
    }, 500);
};
"""

content = re.sub(r'function renderAlumniExperiences\s*\([^)]*\)\s*\{.*?\n\}\n', new_func, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated alumni_hub.js")

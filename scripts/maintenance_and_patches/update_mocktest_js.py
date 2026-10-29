import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\js\mock_test.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """function updateMockSkillsPreview() {
    const container = document.getElementById('mocktest-tags-container');
    const indicator = document.getElementById('mocktest-skills-count-text');
    if (!container) return;

    let skillsList = [];
    if (window.AppState && window.AppState.analyzedSkills) {
        for (const [cat, list] of Object.entries(window.AppState.analyzedSkills)) {
            skillsList.push(...list);
        }
    }

    let certsList = (window.AppState && window.AppState.analyzedCertifications) ? window.AppState.analyzedCertifications : [];

    // Initialize if first time
    if (!window._skillsInitialized) {
        mockActiveSkills = skillsList;
        mockActiveCertifications = certsList;
        window._skillsInitialized = true;
    }

    container.innerHTML = '';

    const allSkills = [...skillsList, ...certsList];
    const defaultTags = ['Python', 'DSA & Problem Solving', 'Java / OOP', 'SQL & Databases', 'React / Web', 'Cloud & Docker', 'Core CS Fundamentals'];
    const tagsToRender = allSkills.length > 0 ? allSkills.slice(0, 15) : defaultTags;
    
    // Default mockActiveSkills to the initial list if empty
    if (mockActiveSkills.length === 0) mockActiveSkills = [...tagsToRender];
    
    tagsToRender.forEach((tag, idx) => {
        const isSelected = mockActiveSkills.includes(tag);
        const pill = document.createElement('div');
        pill.className = isSelected ? 'm-skill-chip selected' : 'm-skill-chip unselected';
        pill.innerHTML = isSelected ? `<i class="fa-solid fa-check"></i> <span>${tag}</span>` : `<i class="fa-regular fa-square"></i> <span>${tag}</span>`;
        
        pill.onclick = function() {
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
                this.classList.add('unselected');
                this.innerHTML = `<i class="fa-regular fa-square"></i> <span>${tag}</span>`;
                mockActiveSkills = mockActiveSkills.filter(s => s !== tag);
            } else {
                this.classList.remove('unselected');
                this.classList.add('selected');
                this.innerHTML = `<i class="fa-solid fa-check"></i> <span>${tag}</span>`;
                if (!mockActiveSkills.includes(tag)) mockActiveSkills.push(tag);
            }
        };
        container.appendChild(pill);
    });

    const addCustom = document.createElement('div');
    addCustom.className = 'm-skill-chip custom';
    addCustom.innerHTML = `<i class="fa-solid fa-plus"></i> <span>Add Custom Skill</span>`;
    addCustom.onclick = function() {
        const newSkill = prompt('Enter a custom skill (e.g. Go, AWS, Docker):');
        if (newSkill && newSkill.trim()) {
            const skillName = newSkill.trim();
            if (!mockActiveSkills.includes(skillName)) {
                mockActiveSkills.push(skillName);
                skillsList.push(skillName); // Fake add it so it persists in the list
                if (window.AppState) {
                    if (!window.AppState.analyzedSkills) window.AppState.analyzedSkills = {};
                    if (!window.AppState.analyzedSkills['Custom']) window.AppState.analyzedSkills['Custom'] = [];
                    window.AppState.analyzedSkills['Custom'].push(skillName);
                }
            }
            updateMockSkillsPreview(); // Re-render
        }
    };
    container.appendChild(addCustom);

    if (indicator) {
        indicator.innerHTML = allSkills.length === 0 ? 'Using Core Tech Stack (Upload resume for custom test)' : 'Ready for Skill Test';
    }
}
"""

content = re.sub(r'function updateMockSkillsPreview\(\)\s*\{.*?(?=\n\s*function|\n\s*async function|\n\s*\/\*)', new_func, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated mock_test.js")

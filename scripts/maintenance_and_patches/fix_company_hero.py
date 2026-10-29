import os
import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\js\resume_analyzer.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """    // Update Company hero card if benchmark data is available
    if (data.cohort_benchmark && data.cohort_benchmark.length > 0) {
        const heroCompany = document.getElementById('hero-company-matches');
        if (heroCompany) {
            heroCompany.innerHTML = ''; // clear placeholders
            // Take top 4 matches
            data.cohort_benchmark.slice(0, 4).forEach(comp => {"""

new_logic = """    // Update Company hero card if benchmark data is available
    if (data.dataset_matching && data.dataset_matching.top_matches && data.dataset_matching.top_matches.length > 0) {
        const heroCompany = document.getElementById('hero-company-matches');
        if (heroCompany) {
            heroCompany.innerHTML = ''; // clear placeholders
            // Take top 4 matches
            data.dataset_matching.top_matches.slice(0, 4).forEach(comp => {"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed resume_analyzer.js company cards bug")
else:
    print("Could not find the target code in resume_analyzer.js")

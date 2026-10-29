import re

html_filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'

with open(html_filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<!-- Floating Dashboard Cards \(CSS Only\) -->\s*<div class="a-float-card ats-card">.*?<div class="a-float-card company-card">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
# The end of the floating cards block is `</div>\s*</div>` inside `analyzer-hero-right`.
# Let's just find `analyzer-hero-right` and replace its contents.

pattern = re.compile(r'(<div class="analyzer-hero-right">)(.*?)(</div>\s*</div>\s*</section>)', re.DOTALL)

replacement = r"""\1
                    <!-- Floating Dashboard Cards (Dynamic JS updated) -->
                    <div class="a-float-card ats-card">
                        <div style="font-size: 0.8rem; font-weight: 600; text-align: center; margin-bottom: 0.8rem; color: var(--text-primary);">ATS Score</div>
                        <div id="hero-ats-circle" class="v-score-circle large" style="margin: 0 auto; width: 80px; height: 80px; border: 4px solid #E2E8F0; transition: border-color 0.5s ease;">
                            <span id="hero-ats-score" style="font-size: 1.8rem; font-weight: 800; color: var(--text-primary);">--</span>
                        </div>
                        <div id="hero-ats-label" style="color: #64748B; font-size: 0.85rem; font-weight: 700; text-align: center; margin-top: 0.8rem; transition: color 0.5s ease;">
                            <i class="fa-solid fa-clock"></i> Awaiting Resume
                        </div>
                    </div>
                    
                    <div class="a-float-card company-card" id="hero-company-matches">
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #94A3B8; background: #F1F5F9;">?</div>
                            <div class="c-info"><span class="c-name" style="color:#94A3B8;">Pending</span><span class="c-score" style="color:#CBD5E1;">-- Match</span></div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #94A3B8; background: #F1F5F9;">?</div>
                            <div class="c-info"><span class="c-name" style="color:#94A3B8;">Pending</span><span class="c-score" style="color:#CBD5E1;">-- Match</span></div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #94A3B8; background: #F1F5F9;">?</div>
                            <div class="c-info"><span class="c-name" style="color:#94A3B8;">Pending</span><span class="c-score" style="color:#CBD5E1;">-- Match</span></div>
                        </div>
                        <div class="c-match-row">
                            <div class="c-icon" style="color: #94A3B8; background: #F1F5F9;">?</div>
                            <div class="c-info"><span class="c-name" style="color:#94A3B8;">Pending</span><span class="c-score" style="color:#CBD5E1;">-- Match</span></div>
                        </div>
                    </div>
                \3"""

content = pattern.sub(replacement, content)

with open(html_filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html")

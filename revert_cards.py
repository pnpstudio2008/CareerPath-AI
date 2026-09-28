import re

def revert_to_cards():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cards_html = """
                <div class="saas-hero-visual">
                    <!-- Dashboard Visual Cluster (CSS Only) -->
                    <div class="visual-card-main">
                        <div class="v-header">
                            <div>
                                <h4 style="margin:0; font-size: 1.1rem; color: var(--text-primary);">{{ user.name if user else 'Student Portal' }}</h4>
                                <span style="font-size: 0.8rem; color: var(--text-muted);">Computer Science Student</span>
                            </div>
                            <div class="v-avatar"><i class="fa-solid fa-user"></i></div>
                        </div>
                        <div class="v-skills mt-3">
                            <span class="v-badge blue">Java</span>
                            <span class="v-badge blue">Python</span>
                            <span class="v-badge blue">Web Development</span>
                            <span class="v-badge outline">AI/ML</span>
                        </div>
                        <div class="v-exp mt-3">
                            <h5 style="font-size: 0.85rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-plus" style="color: var(--primary);"></i> Experience / Projects</h5>
                            <div class="v-exp-item">
                                <i class="fa-solid fa-circle-check text-emerald"></i>
                                <div>
                                    <div style="font-size: 0.85rem; font-weight: 600;">Smart Vehicle Service App</div>
                                    <div style="font-size: 0.75rem; color: var(--text-muted);">Android Studio &bull; Java</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="visual-card-floating top-right">
                        <div style="font-size: 0.8rem; font-weight: 600; text-align: center; margin-bottom: 0.5rem;">Resume Score</div>
                        <div class="v-score-circle">
                            <span style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">82</span>
                        </div>
                        <div style="color: var(--accent-emerald); font-size: 0.8rem; font-weight: 600; text-align: center; margin-top: 0.5rem;">
                            <i class="fa-solid fa-sparkles"></i> Excellent
                        </div>
                    </div>
                    
                    <div class="visual-card-floating bottom-right">
                        <div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.8rem;">Career Match</div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">Software Developer</span>
                            <div class="v-bar-bg"><div class="v-bar-fill emerald" style="width: 92%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">92%</span>
                        </div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">AI/ML Intern</span>
                            <div class="v-bar-bg"><div class="v-bar-fill purple" style="width: 85%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">85%</span>
                        </div>
                        <div class="v-match-row">
                            <span style="font-size: 0.75rem;">Web Developer</span>
                            <div class="v-bar-bg"><div class="v-bar-fill amber" style="width: 78%;"></div></div>
                            <span style="font-size: 0.75rem; font-weight: 600;">78%</span>
                        </div>
                    </div>
                </div>
"""
    
    # We want to replace `<div class="saas-hero-visual"...>...</div>` exactly before `<!-- FEATURE CARDS -->`
    pattern = re.compile(r'<div class="saas-hero-visual"[^>]*>.*?</div>\s*</div>\s*<!-- FEATURE CARDS -->', re.DOTALL)
    
    # Wait, the closing tags are:
    # </div> (closes saas-hero-visual)
    # </div> (closes saas-hero)
    # <!-- FEATURE CARDS -->
    
    replacement = cards_html.strip() + "\n            </div>\n\n            <!-- FEATURE CARDS -->"
    
    if pattern.search(content):
        content = pattern.sub(replacement, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully replaced image with CSS floating cards.")
    else:
        print("Regex didn't match. Printing what's there:")
        import sys
        match = re.search(r'<div class="saas-hero-visual".*?FEATURE CARDS', content, re.DOTALL)
        if match:
            print(match.group(0))

revert_to_cards()

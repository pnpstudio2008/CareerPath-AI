import re

def update_hero_image():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_visual = """
                <div class="saas-hero-visual" style="display: flex; justify-content: center; align-items: center;">
                    <img src="/static/images/hero_building.png" alt="Campus Building" style="max-width: 100%; height: auto; max-height: 420px; border-radius: 24px; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.15); object-fit: cover;">
                </div>
"""

    # We need to replace the entire <div class="saas-hero-visual"> ... </div> block
    # It ends right before <!-- FEATURE CARDS -->
    pattern = re.compile(r'<div class="saas-hero-visual">.*?</div>\s*</div>\s*<!-- FEATURE CARDS -->', re.DOTALL)
    
    if pattern.search(content):
        # We also match the closing </div> of <div class="saas-hero">, so we must put it back
        replacement = new_visual.strip() + "\n            </div>\n\n            <!-- FEATURE CARDS -->"
        content = pattern.sub(replacement, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated hero image in index.html")
    else:
        print("Could not find saas-hero-visual in index.html")

update_hero_image()

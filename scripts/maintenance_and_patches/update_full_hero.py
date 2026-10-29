import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the block starting with .saas-hero { and ending with the end of the file or before .saas-features-grid
# But actually, using regex to replace specific blocks is safer.

# Let's remove the old .saas-hero block
content = re.sub(r'\.saas-hero\s*\{[^}]*\}', '', content)
# Remove old pseudo elements
content = re.sub(r'\.saas-hero::before\s*\{[^}]*\}', '', content)
content = re.sub(r'\.saas-hero::after\s*\{[^}]*\}', '', content)
content = re.sub(r'\.saas-hero-content,\s*\.saas-hero-visual\s*\{[^}]*\}', '', content)
content = re.sub(r'\.saas-hero-content\s*\{[^}]*\}', '', content)

new_hero_css = """
.saas-hero {
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    margin-top: -2rem; 
    margin-bottom: 3rem;
    border-radius: 0;
    padding: 6rem 0;
    overflow: hidden;
}

.saas-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: url('/static/images/hero_campus_bg.jpg');
    background-size: cover;
    background-position: center;
    z-index: 0;
}

.saas-hero::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(to right, rgba(248, 250, 252, 0.95) 0%, rgba(248, 250, 252, 0.85) 45%, rgba(248, 250, 252, 0.1) 75%, rgba(248, 250, 252, 0) 100%);
    z-index: 1;
}

.saas-hero-content {
    max-width: 1240px;
    margin: 0 auto;
    padding: 0 1.25rem;
    position: relative;
    z-index: 2;
}
"""

# Append the new css at the end of the file
content += new_hero_css

# Fix mobile layout for the hero so it doesn't break
content = re.sub(r'@media\s*\(\s*max-width:\s*992px\s*\)\s*\{[^\}]*\.saas-hero\s*\{[^\}]*\}[^\}]*\}', '', content)
# It's hard to regex out nested brackets perfectly, so I'll just append an override

mobile_override = """
@media (max-width: 992px) {
    .saas-hero {
        padding: 4rem 0;
        text-align: center;
    }
    .saas-hero-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .saas-hero::after {
        background: linear-gradient(to bottom, rgba(248, 250, 252, 0.95) 0%, rgba(248, 250, 252, 0.8) 40%, rgba(248, 250, 252, 0.2) 100%) !important;
    }
}
"""
content += mobile_override

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated CSS for full-width hero.")

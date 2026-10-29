import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\index.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to find and remove <div class="saas-hero-visual">...</div>
# We know it ends with <!-- FEATURE CARDS -->
pattern = re.compile(r'<div class="saas-hero-visual">.*?</div>\s*</div>\s*<!-- FEATURE CARDS -->', re.DOTALL)
if pattern.search(content):
    content = pattern.sub('</div>\n\n            <!-- FEATURE CARDS -->', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Removed saas-hero-visual cards.")
else:
    print("Not found.")

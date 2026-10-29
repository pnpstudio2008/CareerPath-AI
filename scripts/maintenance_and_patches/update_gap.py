import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'(\.saas-features-grid\s*\{[^}]*gap:\s*)1rem;', r'\1 1.5rem;', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

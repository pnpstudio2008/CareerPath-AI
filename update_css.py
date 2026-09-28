import re
import os

def update_css():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\style.css'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Font
    content = re.sub(r'family=Plus\+Jakarta\+Sans:wght@[^&]+', 'family=Inter:wght@300;400;500;600;700;800', content)
    content = content.replace("'Plus Jakarta Sans'", "'Inter'")
    
    # Base background and text colors
    content = content.replace('--bg-base: #E8ECF2;', '--bg-base: #F8FAFC;')
    content = content.replace('--bg-surface: #E8ECF2;', '--bg-surface: #FFFFFF;')
    content = content.replace('--bg-card: #E8ECF2;', '--bg-card: #FFFFFF;')
    content = content.replace('--bg-card-hover: #EEF2F8;', '--bg-card-hover: #F8FAFC;')
    content = content.replace('--text-primary: #1E293B;', '--text-primary: #0F172A;')
    content = content.replace('--text-muted: #64748B;', '--text-muted: #94A3B8;')
    
    # Accent colors
    content = content.replace('--primary: #6366F1;', '--primary: #2563EB;')
    content = content.replace('--primary-soft: #4F46E5;', '--primary-soft: #3B82F6;')
    content = content.replace('linear-gradient(145deg, #6366F1, #4F46E5)', 'linear-gradient(135deg, #2563EB, #3B82F6)')
    
    # Soft Shadows instead of Neumorphism
    content = content.replace('--nm-flat: 8px 8px 18px var(--nm-shadow-dark), -8px -8px 18px var(--nm-shadow-light);', '--nm-flat: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.03);')
    content = content.replace('--nm-flat-sm: 4px 4px 10px var(--nm-shadow-dark), -4px -4px 10px var(--nm-shadow-light);', '--nm-flat-sm: 0 1px 3px 0 rgba(0,0,0,0.05), 0 1px 2px -1px rgba(0,0,0,0.03);')
    content = content.replace('--nm-raised: 12px 12px 24px var(--nm-shadow-dark), -12px -12px 24px var(--nm-shadow-light);', '--nm-raised: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);')
    content = content.replace('--nm-inset: inset 4px 4px 8px var(--nm-shadow-dark), inset -4px -4px 8px var(--nm-shadow-light);', '--nm-inset: inset 0 0 0 1px var(--border-subtle);')
    content = content.replace('--nm-inset-sm: inset 2px 2px 5px var(--nm-shadow-dark), inset -2px -2px 5px var(--nm-shadow-light);', '--nm-inset-sm: inset 0 0 0 1px var(--border-subtle);')
    content = content.replace('--nm-inset-deep: inset 6px 6px 12px var(--nm-shadow-dark), inset -6px -6px 12px var(--nm-shadow-light);', '--nm-inset-deep: inset 0 2px 4px 0 rgba(0,0,0,0.03);')
    
    # Borders
    content = content.replace('--border-subtle: rgba(0, 0, 0, 0.04);', '--border-subtle: #E2E8F0;')
    
    # Border Radius
    content = content.replace('--radius-sm: 10px;', '--radius-sm: 8px;')
    content = content.replace('--radius-md: 18px;', '--radius-md: 16px;')
    content = content.replace('--radius-lg: 26px;', '--radius-lg: 24px;')
    
    # Add borders to components that previously relied on neumorphic shadows
    # For .card, .btn, etc.
    content = re.sub(r'(\.card\s*\{[^}]*)', r'\1\n    border: 1px solid var(--border-subtle);', content)
    content = re.sub(r'(\.btn\s*\{[^}]*)', r'\1\n    border: 1px solid transparent;', content)
    content = re.sub(r'(\.feature-card\s*\{[^}]*)', r'\1\n    border: 1px solid var(--border-subtle);\n    background: var(--bg-surface);', content)
    
    # Remove border 2px solid --nm-shadow-light
    content = content.replace('border: 2px solid var(--nm-shadow-light);', '')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    comp_path = r'c:\Users\desai\Downloads\Projects\riyamam\static\css\components.css'
    with open(comp_path, 'r', encoding='utf-8') as f:
        comp_content = f.read()
        
    comp_content = comp_content.replace('border: 2px solid var(--nm-shadow-light);', '')
    comp_content = comp_content.replace('box-shadow: var(--nm-inset-sm);', 'border: 1px solid var(--border-subtle);')
    
    with open(comp_path, 'w', encoding='utf-8') as f:
        f.write(comp_content)

update_css()
print('CSS Updated!')

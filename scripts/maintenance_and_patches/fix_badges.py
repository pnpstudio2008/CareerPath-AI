import os
import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's fix the mess I made
# I will find .score-low { ... } and the start of .admin-table-wrapper to replace all badge CSS
start_idx = content.find('.score-low { background: #FEF2F2; color: #EF4444; }')
end_idx = content.find('/* Actions */')

if start_idx != -1 and end_idx != -1:
    new_css = """.score-low { background: #FEF2F2; color: #EF4444; }

        /* Shared Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.6rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            border: 1px solid transparent;
        }
        .badge::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
        }
        
        /* Badge Variants */
        .badge-success { background: #F0FDF4; color: #10B981; }
        .badge-success::before { background: #10B981; }

        .badge-warning { background: #FFF7ED; color: #F97316; }
        .badge-warning::before { background: #F97316; }

        .badge-danger { background: #FEF2F2; color: #EF4444; }
        .badge-danger::before { background: #EF4444; }

        .badge-primary { background: #EFF6FF; color: var(--admin-primary); }
        .badge-primary::before { background: var(--admin-primary); }

        .badge-secondary { background: #F8FAFC; border-color: var(--admin-border); color: var(--admin-text-muted); }
        .badge-secondary::before { display: none; }

        """
    
    content = content[:start_idx] + new_css + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed CSS badges!")
else:
    print("Could not find indices!")

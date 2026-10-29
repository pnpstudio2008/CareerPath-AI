import os
import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the sidebar element completely
sidebar_pattern = r'<aside class="admin-sidebar">.*?</aside>'
content = re.sub(sidebar_pattern, '', content, flags=re.DOTALL)

# Update CSS
# Change --admin-sidebar-width to 0px
content = content.replace('--admin-sidebar-width: 260px;', '--admin-sidebar-width: 0px;')

# Change admin-nav-left width to auto
content = content.replace('width: var(--admin-sidebar-width);', 'width: auto;', 1) # Only first occurrence, which is in admin-nav-left

# Update main content margin and max-width just to be safe
content = content.replace('margin-left: var(--admin-sidebar-width);', 'margin-left: 0;')
content = content.replace('max-width: calc(100vw - var(--admin-sidebar-width));', 'max-width: 100vw; margin: 0 auto; width: 100%;')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

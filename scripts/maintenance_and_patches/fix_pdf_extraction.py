import os
import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\nlp_engine.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Strategy 3 and 4 removal logic
# They start from "    # Strategy 3:" and go until "    return full_text if full_text else """
start_idx = content.find('    # Strategy 3:')
end_idx = content.find('    return full_text if full_text else ""')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + content[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Removed dangerous regex PDF fallbacks.")
else:
    print("Could not find Strategy 3/4")

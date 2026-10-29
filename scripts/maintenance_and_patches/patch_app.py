import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_analyze_resume = False
in_docstring = False
indent = "    "
func_start_idx = -1
func_end_idx = -1

for i, line in enumerate(lines):
    if line.startswith("def analyze_resume():"):
        in_analyze_resume = True
        func_start_idx = i
        continue

if func_start_idx != -1:
    # Find the end of the docstring
    for i in range(func_start_idx + 1, len(lines)):
        if '"""' in lines[i]:
            if not in_docstring:
                in_docstring = True
            else:
                in_docstring = False
                docstring_end_idx = i
                break
                
    # Find the end of the function (which is the return jsonify block)
    for i in range(docstring_end_idx + 1, len(lines)):
        if lines[i].strip() == "})":
            if i + 1 < len(lines) and lines[i+1].strip() == "":
                func_end_idx = i
                break

    print(f"Function from {func_start_idx} to {func_end_idx}")

    rate_limit_lines = [
        "    # --- RATE LIMITING ---\n",
        "    last_upload = session.get('resume_last_upload_time', 0)\n",
        "    if time.time() - last_upload > 24 * 3600:\n",
        "        session['resume_upload_count'] = 0\n",
        "\n",
        "    if session.get('resume_upload_count', 0) >= 10:\n",
        "        return jsonify({\n",
        "            'success': False, \n",
        "            'error': 'You have reached your daily limit of 10 resume analyses. Please try again after 24 hours to help us reduce network consumption.'\n",
        "        }), 429\n",
        "    # ---------------------\n",
        "\n",
        "    try:\n",
        "        session['resume_upload_count'] = session.get('resume_upload_count', 0) + 1\n",
        "        session['resume_last_upload_time'] = time.time()\n"
    ]

    # Reconstruct the file
    new_content = []
    # Up to docstring end
    new_content.extend(lines[:docstring_end_idx+1])
    
    # Add rate limit and try block
    new_content.extend(rate_limit_lines)
    
    # Indent the body
    for line in lines[docstring_end_idx+1:func_end_idx+1]:
        if line.strip() == "":
            new_content.append(line)
        else:
            new_content.append("    " + line)
            
    # Add except block
    except_lines = [
        "    except Exception as e:\n",
        "        return jsonify({\n",
        "            'success': False,\n",
        "            'error': f'Failed to parse or analyze resume. {str(e)}',\n",
        "            'is_resume': False\n",
        "        }), 500\n"
    ]
    new_content.extend(except_lines)
    
    # Rest of the file
    new_content.extend(lines[func_end_idx+1:])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    print("Patched app.py successfully.")
else:
    print("Could not find analyze_resume.")

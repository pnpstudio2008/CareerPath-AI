import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """    student = authenticate_student(identifier, password)
    if student:
        session['pending_2fa_type'] = 'student'"""

new_code = """    student = authenticate_student(identifier, password)
    if student:
        if student.get("account_status", "Active") == "Frozen":
            return jsonify({
                "success": False,
                "error": "Your account has been frozen by the Administrator. Please contact support."
            })
        session['pending_2fa_type'] = 'student'"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app.py")
else:
    print("Could not find the target code in app.py")

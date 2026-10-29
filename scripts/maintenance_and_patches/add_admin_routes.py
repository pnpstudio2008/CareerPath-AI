import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_routes = """@app.route('/admin', methods=['GET'])
def admin_portal():
    \"\"\"Renders the standalone Admin Dashboard or Login Page.\"\"\"
    if session.get('admin_logged_in'):
        return render_template('admin.html', admin_user=session.get('admin_user', 'Administrator'))
    return render_template('admin_login.html')

@app.route('/admin/alumni', methods=['GET'])
def admin_alumni_portal():
    \"\"\"Renders the Admin Alumni Records page.\"\"\"
    if session.get('admin_logged_in'):
        return render_template('admin_alumni.html', admin_user=session.get('admin_user', 'Administrator'))
    return redirect(url_for('admin_portal'))

@app.route('/admin/settings', methods=['GET'])
def admin_settings_portal():
    \"\"\"Renders the Admin Settings page (for freezing accounts, etc.).\"\"\"
    if session.get('admin_logged_in'):
        return render_template('admin_settings.html', admin_user=session.get('admin_user', 'Administrator'))
    return redirect(url_for('admin_portal'))

@app.route('/api/admin/students/toggle-freeze/<int:student_id>', methods=['POST'])
@admin_required
def toggle_freeze_student(student_id):
    \"\"\"Admin toggles the freeze status of a student account.\"\"\"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_status FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({"success": False, "error": "Student not found."})
            
        current_status = dict(row).get('account_status', 'Active')
        new_status = 'Frozen' if current_status != 'Frozen' else 'Active'
        
        cursor.execute("UPDATE students SET account_status = ? WHERE id = ?", (new_status, student_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": f"Student account is now {new_status}.",
            "new_status": new_status
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})"""

old_routes = """@app.route('/admin', methods=['GET'])
def admin_portal():
    \"\"\"Renders the standalone Admin Dashboard or Login Page.\"\"\"
    if session.get('admin_logged_in'):
        return render_template('admin.html', admin_user=session.get('admin_user', 'Administrator'))
    return render_template('admin_login.html')"""

if old_routes in content:
    content = content.replace(old_routes, new_routes)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added admin alumni and settings routes")
else:
    print("Could not find the admin_portal route in app.py")

import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\app.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_route = """@app.route('/api/admin/students/toggle-freeze-by-roll', methods=['POST'])
@admin_required
def toggle_freeze_student_by_roll():
    \"\"\"Admin toggles the freeze status of a student account by roll_no.\"\"\"
    try:
        data = request.json or request.form.to_dict()
        roll_no = data.get('roll_no', '').strip().lower()
        if not roll_no:
            return jsonify({"success": False, "error": "Roll number is required."})
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, account_status FROM students WHERE LOWER(roll_no) = ?", (roll_no,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({"success": False, "error": f"Student with roll number '{roll_no}' not found."})
            
        current_status = dict(row).get('account_status', 'Active')
        new_status = 'Frozen' if current_status != 'Frozen' else 'Active'
        
        cursor.execute("UPDATE students SET account_status = ? WHERE id = ?", (new_status, row['id']))
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": f"Account for {row['name']} ({roll_no.upper()}) is now {new_status}.",
            "new_status": new_status
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})"""

old_target = """@app.route('/api/admin/students/toggle-freeze/<int:student_id>', methods=['POST'])
@admin_required
def toggle_freeze_student(student_id):"""

if old_target in content:
    content = content.replace(old_target, new_route + "\n\n" + old_target)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added toggle freeze by roll route")
else:
    print("Could not find the target to insert new route")

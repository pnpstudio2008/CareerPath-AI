import os
filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace IDs and function names
content = content.replace('id="admin-search" placeholder="Search student name, roll no, or email..." oninput="filterAdminTable()"', 'id="admin-student-search" placeholder="Search student name, roll no, or email..." oninput="fetchAdminStudents()"')
content = content.replace('id="admin-filter-branch" onchange="filterAdminTable()"', 'id="admin-branch-filter" onchange="fetchAdminStudents()"')
content = content.replace('id="admin-filter-status" onchange="filterAdminTable()"', 'id="admin-status-filter" onchange="fetchAdminStudents()"')
content = content.replace('id="admin-filter-readiness" onchange="filterAdminTable()"', 'id="admin-readiness-filter" onchange="fetchAdminStudents()"')
content = content.replace('onclick="resetAdminFilters()"', 'onclick="resetFilters()"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

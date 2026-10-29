import os

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\static\js\admin_panel.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_func = """function switchAdminTab(tabName) {
    currentAdminTab = tabName;

    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    document.querySelectorAll('.admin-tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `admin-tab-${tabName}`);
    });

    if (tabName === 'students') fetchAdminStudents();
    else if (tabName === 'alumni') fetchAdminAlumni();
}"""

new_func = """function switchAdminTab(tabName) {
    currentAdminTab = tabName;

    // Handle new design
    const tabStudents = document.getElementById('tab-students');
    const tabAlumni = document.getElementById('tab-alumni');
    const viewStudents = document.getElementById('students-view');
    const viewAlumni = document.getElementById('alumni-view');

    if (tabStudents && tabAlumni && viewStudents && viewAlumni) {
        if (tabName === 'students') {
            tabStudents.classList.add('active');
            tabAlumni.classList.remove('active');
            viewStudents.style.display = 'block';
            viewAlumni.style.display = 'none';
        } else {
            tabAlumni.classList.add('active');
            tabStudents.classList.remove('active');
            viewAlumni.style.display = 'block';
            viewStudents.style.display = 'none';
        }
    } else {
        // Fallback to old design if elements not found
        document.querySelectorAll('.admin-tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });

        document.querySelectorAll('.admin-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `admin-tab-${tabName}`);
        });
    }

    if (tabName === 'students') fetchAdminStudents();
    else if (tabName === 'alumni') fetchAdminAlumni();
}"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated switchAdminTab.")
else:
    print("Could not find old switchAdminTab function exactly. Will use regex or manual replace.")


import os
import re

def process_admin_settings_html():
    filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin_settings.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update top nav
    content = content.replace('href="#" class="admin-nav-link active"><i data-lucide="layout-dashboard"></i> Cohort Management', 'href="/admin" class="admin-nav-link"><i data-lucide="layout-dashboard"></i> Cohort Management')
    content = content.replace('href="#" class="admin-nav-link" onclick="document.getElementById(\'tab-alumni\').click()"><i data-lucide="users"></i> Alumni Records', 'href="/admin/alumni" class="admin-nav-link"><i data-lucide="users"></i> Alumni Records')
    content = content.replace('href="#" class="admin-nav-link"><i data-lucide="settings"></i> Settings', 'href="/admin/settings" class="admin-nav-link active"><i data-lucide="settings"></i> Settings')

    # Update Hero
    content = content.replace('Cohort & <span>Placement Management</span>', 'Platform <span>Settings & Security</span>')
    content = content.replace('Manage student cohorts, track real-time placement progress, and supervise alumni records & verified mentors.', 'Configure system settings, manage access control, and enforce security policies.')

    # Remove metrics grid entirely
    metrics_start = content.find('<!-- METRICS -->')
    metrics_end = content.find('<!-- MANAGEMENT PANEL -->')
    if metrics_start != -1 and metrics_end != -1:
        content = content[:metrics_start] + content[metrics_end:]

    # Remove the entire management panel contents (filters, tables, etc)
    panel_start = content.find('<div class="admin-panel-container">')
    panel_end = content.find('</main>')
    
    settings_panel_html = """<div class="admin-panel-container" style="max-width: 800px; margin: 0 auto;">
                <div class="admin-panel-header">
                    <div class="admin-tabs">
                        <h3 style="margin:0; font-size: 1.1rem; color: var(--admin-text-main); font-weight: 700;">
                            <i data-lucide="shield" style="vertical-align:middle; margin-right:8px; color:var(--admin-primary);"></i> Access Control
                        </h3>
                    </div>
                </div>

                <div style="padding: 2rem;">
                    <h4 style="margin-top:0; margin-bottom:1rem; font-size:1rem;">Student Account Freeze</h4>
                    <p style="color: var(--admin-text-muted); font-size:0.875rem; margin-bottom:1.5rem; line-height:1.5;">
                        Freeze an ongoing student's account to instantly revoke their login access to the platform. 
                        They will not be able to log in until an administrator unfreezes the account.
                    </p>

                    <div style="display: flex; gap: 1rem; align-items: flex-end;">
                        <div style="flex:1;">
                            <label style="display:block; font-size:0.75rem; font-weight:600; color:var(--admin-text-muted); margin-bottom:0.5rem; text-transform:uppercase;">Student ID / Roll No</label>
                            <input type="text" id="freeze-student-id" class="admin-search-input" placeholder="e.g. 24C11018" style="padding-left: 1rem;">
                        </div>
                        <button class="admin-btn-primary" onclick="toggleFreeze()" id="btn-freeze-student" style="background: #EF4444; box-shadow: 0 4px 6px -1px rgba(239,68,68,0.2);">
                            <i data-lucide="lock"></i> Toggle Freeze Status
                        </button>
                    </div>
                    
                    <div id="freeze-result" style="margin-top: 1.5rem; padding: 1rem; border-radius: 12px; display: none; font-size: 0.875rem; font-weight: 500;"></div>
                </div>
            </div>
            """
    
    if panel_start != -1 and panel_end != -1:
        content = content[:panel_start] + settings_panel_html + content[panel_end:]

    # Add script for toggle freeze
    script_inject = """<script>
    async function toggleFreeze() {
        const identifier = document.getElementById('freeze-student-id').value.trim();
        const resultDiv = document.getElementById('freeze-result');
        
        if (!identifier) {
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = '#FEF2F2';
            resultDiv.style.color = '#EF4444';
            resultDiv.innerText = 'Please enter a Student ID or Roll No.';
            return;
        }

        try {
            // First we need to find the student ID from roll_no...
            // Or we can modify our API endpoint to accept roll_no too!
            // Wait, since we are doing it via a new API endpoint, let's create a specific one for this.
            
            const res = await fetch('/api/admin/students/toggle-freeze-by-roll', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ roll_no: identifier })
            });
            const data = await res.json();
            
            resultDiv.style.display = 'block';
            if (data.success) {
                resultDiv.style.backgroundColor = '#F0FDF4';
                resultDiv.style.color = '#10B981';
                resultDiv.innerHTML = `<i data-lucide="check-circle" style="vertical-align:middle; width:16px; height:16px;"></i> ${data.message}`;
                if (typeof lucide !== 'undefined') lucide.createIcons();
            } else {
                resultDiv.style.backgroundColor = '#FEF2F2';
                resultDiv.style.color = '#EF4444';
                resultDiv.innerHTML = `<i data-lucide="alert-circle" style="vertical-align:middle; width:16px; height:16px;"></i> ${data.error}`;
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }
        } catch (err) {
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = '#FEF2F2';
            resultDiv.style.color = '#EF4444';
            resultDiv.innerText = 'Network error occurred.';
        }
    }
</script></body>"""
    content = content.replace('</body>', script_inject)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_admin_settings_html()
print("Processed admin_settings.html")

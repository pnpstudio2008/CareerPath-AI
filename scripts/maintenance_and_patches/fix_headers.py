import os
filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\admin.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove checkbox th
content = content.replace('<th style="width: 40px;"><input type="checkbox" class="admin-checkbox"></th>', '')

# Replace alumni headers
old_alumni_headers = """                            <tr>
                                <th>ALUMNI MENTOR</th>
                                <th>ROLL / BATCH</th>
                                <th>COMPANY & ROLE</th>
                                <th>PACKAGE</th>
                                <th>OFFER TYPE</th>
                                <th>ACTIONS</th>
                            </tr>"""

new_alumni_headers = """                            <tr>
                                <th>ALUMNI MENTOR</th>
                                <th>EMAIL</th>
                                <th>COMPANY</th>
                                <th>ROLE</th>
                                <th>PACKAGE</th>
                                <th>UPVOTES</th>
                                <th>ACTIONS</th>
                            </tr>"""

content = content.replace(old_alumni_headers, new_alumni_headers)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

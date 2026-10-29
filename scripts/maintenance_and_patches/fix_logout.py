import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\templates\alumni_profile.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

logout_func = """        async function alumniLogout() {
            try {
                await fetch('/api/alumni/logout', { method: 'POST' });
                window.location.href = '/student/login?role=alumni';
            } catch (err) {
                console.error(err);
                window.location.href = '/student/login?role=alumni';
            }
        }
    </script>"""

content = content.replace("    </script>", logout_func)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added alumniLogout to alumni_profile.html")

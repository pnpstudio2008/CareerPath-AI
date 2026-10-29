import os
import glob
import re

html_files = glob.glob(r'c:\Users\desai\Downloads\Projects\riyamam\templates\*.html')

robust_fetch = """
<script>
// --- Safe JSON Fetch Wrapper ---
async function safeJsonFetch(response) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return await response.json();
    } else {
        const text = await response.text();
        console.error("Non-JSON response received:", text.substring(0, 200));
        throw new Error("Server returned an invalid or HTML response. (Possible Network/Server Error)");
    }
}
</script>
"""

def inject_safe_fetch(content):
    if "safeJsonFetch" not in content and "await res.json()" in content:
        # Find the first <script> tag and put our helper right before it
        script_idx = content.find('<script>')
        if script_idx != -1:
            content = content[:script_idx] + robust_fetch + content[script_idx:]
        else:
            # Or just before </body>
            content = content.replace('</body>', robust_fetch + '</body>')

    content = re.sub(r'await\s+([a-zA-Z0-9_]+)\.json\(\)', r'await safeJsonFetch(\1)', content)
    # Ensure safeJsonFetch itself uses .json() !
    content = content.replace("return await safeJsonFetch(response);", "return await response.json();")
    
    return content

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "await res.json()" in content or "await response.json()" in content:
        new_content = inject_safe_fetch(content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {os.path.basename(file)}")

print("Done patching HTML files.")

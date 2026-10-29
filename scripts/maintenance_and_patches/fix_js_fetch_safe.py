import os
import glob
import re

js_files = glob.glob(r'c:\Users\desai\Downloads\Projects\riyamam\static\js\*.js')

robust_fetch = """
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
"""

def inject_safe_fetch(content):
    # First, replace all `await X.json()` with `await safeJsonFetch(X)`
    # but NOT if it's already safeJsonFetch
    
    # We'll do it carefully
    content = re.sub(r'await\s+([a-zA-Z0-9_]+)\.json\(\)', r'await safeJsonFetch(\1)', content)
    
    if "safeJsonFetch" in content and "// --- Safe JSON Fetch Wrapper ---" not in content:
        content = robust_fetch + "\n" + content
        
    # We must ensure safeJsonFetch itself uses .json() !
    content = content.replace("return await safeJsonFetch(response);", "return await response.json();")
    
    return content

for file in js_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = inject_safe_fetch(content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Injected safeJsonFetch safely.")

import re

filepath = r'c:\Users\desai\Downloads\Projects\riyamam\app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

error_handlers = """
# ==========================================
# GLOBAL ERROR HANDLERS
# ==========================================
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        # Return JSON for all API routes
        if request.path.startswith('/api/'):
            return jsonify({
                "success": False,
                "error": e.description if hasattr(e, 'description') else str(e)
            }), e.code
        return e

    # Handle non-HTTP exceptions
    if request.path.startswith('/api/'):
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred: " + str(e)
        }), 500
    
    return "Internal Server Error", 500

"""

# Let's insert this before `# ==========================================\n# RESUME ANALYZER & ATS EVALUATION API`
target = "# ==========================================\n# RESUME ANALYZER & ATS EVALUATION API"
content = content.replace(target, error_handlers + "\n" + target)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added global error handlers.")

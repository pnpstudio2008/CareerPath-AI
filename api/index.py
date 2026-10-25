import sys
import os

# Add root project directory to sys.path so app and all local modules can be imported
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Load environment variables if .env exists locally
from dotenv import load_dotenv
env_path = os.path.join(ROOT_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Import the Flask application instance
from app import app

# Vercel WSGI entrypoint callable
# Vercel Python runtime auto-detects 'app'
if __name__ == "__main__":
    app.run(debug=True)

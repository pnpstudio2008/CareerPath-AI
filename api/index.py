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

# WSGI environment path normalizer for Vercel Serverless Function rewrites
class VercelPathNormalizer:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        # Normalize serverless entrypoint rewrites to root path if requested
        if path in ('/api/index', '/api/index.py', '/api/index/', '/api/index.py/'):
            orig = environ.get('HTTP_X_FORWARDED_PATH') or environ.get('HTTP_X_REWRITE_PATH')
            environ['PATH_INFO'] = orig if orig else '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathNormalizer(app.wsgi_app)

# Vercel WSGI entrypoint callable: 'app'
if __name__ == "__main__":
    app.run(debug=True)

import sys
import os
from urllib.parse import parse_qs, urlencode

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
        qs = parse_qs(environ.get('QUERY_STRING', ''), keep_blank_values=True)
        orig_path = None
        if '__vercel_path' in qs:
            orig_path = qs.pop('__vercel_path')[0]
            environ['QUERY_STRING'] = urlencode(qs, doseq=True)

        matched = environ.get('HTTP_X_MATCHED_PATH')
        if matched and not matched.startswith('/api/index.py'):
            environ['PATH_INFO'] = matched
        elif orig_path:
            environ['PATH_INFO'] = orig_path if orig_path.startswith('/') else f'/{orig_path}'
        elif environ.get('PATH_INFO') in ('/api/index', '/api/index.py', '/api/index/', '/api/index.py/'):
            environ['PATH_INFO'] = '/'

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathNormalizer(app.wsgi_app)

# Vercel WSGI entrypoint callable: 'app'
if __name__ == "__main__":
    app.run(debug=True)

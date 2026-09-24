import sys
import os

# Add root project directory to sys.path so app and dependencies can be imported
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import serverless_wsgi
from app import app

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
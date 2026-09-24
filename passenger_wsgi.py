"""
AI Career Companion — Hostinger hPanel Passenger WSGI Entry Point
-----------------------------------------------------------------
Place this project in your Hostinger File Manager under:
  /home/u<id>/domains/ai-career-companion.pnpstudio.in/public_html/

In hPanel → Python App Manager:
  - Application Root : domains/ai-career-companion.pnpstudio.in/public_html
  - Application URL  : ai-career-companion.pnpstudio.in
  - Application startup file : passenger_wsgi.py
  - Application Entry Point  : application
  - Python Version   : 3.11 (or highest available)

After setting up, click "Run pip install" and paste requirements.txt packages.
"""
import sys
import os

# Set application root as the directory containing this file
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Load .env variables (DATABASE_URL, SECRET_KEY, etc.)
from dotenv import load_dotenv
env_path = os.path.join(APP_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Ensure the uploads directory exists (Hostinger clears it on restart)
uploads_dir = os.path.join(APP_DIR, "uploads")
os.makedirs(uploads_dir, exist_ok=True)

# Import Flask app as WSGI callable — Passenger requires the name 'application'
from wsgi import app as application

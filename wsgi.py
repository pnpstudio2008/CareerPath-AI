"""
WSGI Entry Point — AI Career Companion
Works with: Hostinger Passenger, Gunicorn, uWSGI, Render, Railway
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import app

# Ensure uploads directory exists on every startup
os.makedirs(os.path.join(os.path.dirname(__file__), "uploads"), exist_ok=True)

if __name__ == "__main__":
    app.run(debug=False)

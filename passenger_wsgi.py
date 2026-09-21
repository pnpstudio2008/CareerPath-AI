"""
Hostinger hPanel / CloudLinux Passenger WSGI Entry Point
This file enables seamless execution on Hostinger Cloud and Web Hosting plans
using LiteSpeed / Phusion Passenger Python App Manager.
"""
import sys
import os

# Set application root in Python search path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Load environment variables if available
from dotenv import load_dotenv
env_path = os.path.join(APP_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Import the Flask WSGI callable as 'application'
from wsgi import app as application

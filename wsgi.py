"""
WSGI Entrypoint for Production Web Hosting (Render, Railway, Heroku, VPS)
"""
from app import app

if __name__ == "__main__":
    app.run()

import os
import sys

# Try different paths for Railway deployment
possible_paths = [
    os.getcwd(),  # Current working directory
    os.path.dirname(__file__),  # Directory containing wsgi.py
    "/app",  # Railway app directory
]

for path in possible_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# Try to import create_app from different locations
try:
    from app import create_app
except ImportError:
    try:
        # Try importing from the nested app directory
        sys.path.insert(0, "/app")
        from app import create_app
    except ImportError:
        # Try importing directly from the app module
        import app
        create_app = app.create_app

app = create_app()

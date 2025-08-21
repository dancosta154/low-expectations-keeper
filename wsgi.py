import os
import sys

# Debug: Print current directory and files
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir(\".\")}")
if os.path.exists("app"):
    print(f"Files in app directory: {os.listdir(\"app\")}")

# Add current directory to path
sys.path.insert(0, os.getcwd())

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

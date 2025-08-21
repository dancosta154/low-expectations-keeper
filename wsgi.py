import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

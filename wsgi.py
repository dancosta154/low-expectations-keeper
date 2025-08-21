import os
import sys
sys.path.insert(0, os.getcwd())
from app import create_app
app = create_app()

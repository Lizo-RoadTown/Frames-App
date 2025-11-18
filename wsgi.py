"""
WSGI configuration for PythonAnywhere deployment
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/Frames-App'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Add the backend directory to sys.path
backend_path = os.path.join(project_home, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Change to backend directory so relative imports work
os.chdir(backend_path)

# Import the Flask app
from app import app as application

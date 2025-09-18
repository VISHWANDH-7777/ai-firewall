import sys
import os

# Add your project directory to the Python path
project_home = '/home/yourusername/ai-firewall-project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Import your Flask app
from app import app as application
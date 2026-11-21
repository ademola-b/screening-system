# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PythonAnywhere WSGI Configuration for screening-system
# Replace <your-username> with your actual PythonAnywhere username!
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys

# Add your project directory to sys.path
path = '/home/<your-username>/screening-system'
if path not in sys.path:
    sys.path.append(path)

# Point to your Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'screening_exercise.settings'

# Load the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

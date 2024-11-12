"""
WSGI config for sales_projection_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# sales_projection_project/wsgi.py
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend suitable for web servers
import matplotlib.pyplot as plt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales_projection_project.settings')

application = get_wsgi_application()

app = application


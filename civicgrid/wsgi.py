"""WSGI configuration for CivicGrid AI."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civicgrid.settings")

application = get_wsgi_application()

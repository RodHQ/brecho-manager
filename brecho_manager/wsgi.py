"""WSGI config for brecho_manager."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brecho_manager.settings")

application = get_wsgi_application()

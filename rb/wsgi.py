"""
WSGI config for roadBuddy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# settings.production is the production settings in the settings folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rb.settings.development')

application = get_wsgi_application()

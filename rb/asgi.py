"""
ASGI config for roadBuddy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# settings.production is the production settings in the settings folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rb.settings.development')

application = get_asgi_application()

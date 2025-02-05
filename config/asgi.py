# config/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from config.routing import application as channels_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": django.core.asgi.get_asgi_application(),
    "websocket": URLRouter(channels_application.routing),
})

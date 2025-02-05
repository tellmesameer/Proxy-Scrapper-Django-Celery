# config/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from apps.proxy_scraper.consumers import ProxyConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/proxies/$', ProxyConsumer.as_asgi()),
    ]),
})

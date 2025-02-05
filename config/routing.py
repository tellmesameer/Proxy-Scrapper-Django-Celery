# config/routing.py
from django.urls import re_path
from apps.proxy_scraper.consumers import ProxyConsumer

websocket_urlpatterns = [
    re_path(r'^ws/proxies/$', ProxyConsumer.as_asgi()),
]

# apps/proxy_scraper/views.py
import logging
from django.shortcuts import render
from .models import Proxy

logger = logging.getLogger(__name__)

def home(request):
    proxies = Proxy.objects.all()
    logger.debug(f"Rendering home page with {proxies.count()} proxies")
    return render(request, 'proxy_scraper/home.html', {'proxies': proxies})

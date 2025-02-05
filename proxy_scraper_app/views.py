# proxy_scraper_app/views.py
from django.shortcuts import render
from .models import Proxy

def home(request):
    proxies = Proxy.objects.all()
    return render(request, 'home.html', {'proxies': proxies})

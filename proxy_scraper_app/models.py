# proxy_scraper_app/models.py
from django.db import models

class Proxy(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    protocol = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    uptime = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.ip}:{self.port}'

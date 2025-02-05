# proxy_scraper_app/tasks.py
from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Proxy

@shared_task
def scrape_and_save_proxies():
    url = 'https://geonode.com/free-proxy-list/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract IP, port, protocol, country, and uptime
        proxy_table = soup.find('table', class_='proxy__t')  # Adjust based on HTML structure

        for row in proxy_table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            ip = columns[0].text.strip()
            port = int(columns[1].text.strip())
            protocol = columns[4].text.strip()
            country = columns[2].text.strip()
            uptime = columns[8].text.strip()

            # Save data to the database
            Proxy.objects.create(ip=ip, port=port, protocol=protocol, country=country, uptime=uptime)

# apps/proxy_scraper/tasks.py
import logging
from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Proxy

logger = logging.getLogger(__name__)

@shared_task
def scrape_and_save_proxies():
    url = 'https://geonode.com/free-proxy-list/'
    logger.debug(f"Starting proxy scrape from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    proxy_table = soup.find('table', class_='proxy__t')  # Adjust selector as needed

    if not proxy_table:
        logger.error("Could not find the proxy table on the page.")
        return

    new_entries = 0
    for row in proxy_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        try:
            ip = columns[0].text.strip()
            port = int(columns[1].text.strip())
            country = columns[2].text.strip()
            protocol = columns[4].text.strip()
            uptime = columns[8].text.strip()
            Proxy.objects.update_or_create(
                ip=ip, port=port,
                defaults={'protocol': protocol, 'country': country, 'uptime': uptime}
            )
            logger.debug(f"Saved proxy: {ip}:{port} {protocol} from {country} with uptime {uptime}")
            new_entries += 1
        except Exception as e:
            logger.exception(f"Error processing row: {row} - {e}")

    logger.debug(f"Scraping complete. {new_entries} proxies updated/added.")

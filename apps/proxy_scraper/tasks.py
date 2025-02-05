# apps\proxy_scraper\tasks.py
from celery import shared_task
from bs4 import BeautifulSoup
import requests
from .models import Proxy
import logging

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

    # Update this selector based on the current HTML structure of the page
    proxy_table = soup.find('table', class_='free-proxies-table')
    if not proxy_table:
        logger.error("Could not find the proxy table on the page.")
        return

    new_entries = 0
    # Skip the header row and iterate over the table rows
    for row in proxy_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) < 9:
            continue  # Skip rows that don't have enough columns
        try:
            ip = columns[0].text.strip()
            port = int(columns[1].text.strip())
            country = columns[2].text.strip()
            protocol = columns[3].text.strip()  # Adjust the index as needed
            uptime = columns[8].text.strip()      # Adjust the index as needed

            Proxy.objects.update_or_create(
                ip=ip,
                port=port,
                defaults={'protocol': protocol, 'country': country, 'uptime': uptime}
            )
            logger.debug(f"Saved proxy: {ip}:{port} {protocol} from {country} with uptime {uptime}")
            new_entries += 1
        except Exception as e:
            logger.exception(f"Error processing row: {row} - {e}")

    logger.debug(f"Scraping complete. {new_entries} proxies updated/added.")

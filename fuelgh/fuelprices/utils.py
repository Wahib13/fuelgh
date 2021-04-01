import re
import urllib

import requests
from bs4 import BeautifulSoup

NPA_BASE_URL = 'http://www.npa.gov.gh/'
DOWNLOAD_PATH = '/downloads/indicative-prices'
NPA_ALL_DOWNLOADS_URL = urllib.parse.urljoin(NPA_BASE_URL, DOWNLOAD_PATH)


def fetch_link_to_price_sheet():
    """
    scrape from home page. may return None if no link is not found
    """
    response = requests.get(NPA_BASE_URL)
    html_text = response.text
    soup = BeautifulSoup(html_text, 'html.parser')
    for link in soup.find_all('a'):
        if 'Indicative_Prices_' in link.get('href'):
            return link.get('href')


def fetch_link_from_download_page():
    """
    scrape from page with all the downloads. may return None if no link is not found
    """
    final_link = None
    response = requests.get(NPA_ALL_DOWNLOADS_URL)
    html_text = response.text
    soup = BeautifulSoup(html_text, 'html.parser')
    for link in soup.find_all('a'):
        if 'Indicative_Prices_' in link.get('href') and '2021' in link.get('href'):
            # constantly override the variable in order to get the last one
            final_link = link.get('href')
    return final_link


def fetch_latest_link():
    """
    call functions to scrape from both the home and download page and compare which one is more recent and return that
    """
    home_page_link = fetch_link_to_price_sheet()
    download_page_link = fetch_link_from_download_page()
    # TODO use regex to extract date, making sure the latest link is always returned
    # re.search('(\d+)', home_page_link)
    return urllib.parse.urljoin(NPA_BASE_URL, home_page_link)

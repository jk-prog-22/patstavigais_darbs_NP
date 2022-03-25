import requests
import constant
from bs4 import BeautifulSoup

headers = {
    'User-Agent': constant.USERAGENT
}

def getClassifieds(url = constant.BASE, filters = []):
    page = requests.get(url, headers=headers, timeout=constant.TIMEOUT)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        vehicles = soup.find_all('table')
        print(vehicles)
    else:
        print("Error fetching classifieds.")

getClassifieds()
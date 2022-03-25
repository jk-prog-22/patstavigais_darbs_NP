import requests
import constant
import logging
from bs4 import BeautifulSoup

getHeaders = {
    "Referer": "https://www.ss.com/en/transport/cars/filter/",
    "User-Agent": constant.USERAGENT
}

if constant.DEBUG == True:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def getClassifieds(url = constant.FILTER, filters = constant.FILTERS):
    session = requests.Session()
    getContents = session.post(constant.FILTER, headers = getHeaders, timeout = constant.TIMEOUT, allow_redirects = True)
    if getContents.status_code == 200:
        soup = BeautifulSoup(getContents.content, 'html.parser')
        vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
        for vehicle in vehicles:
            elements = vehicle.findAll("td")
            if elements[1].find("a", href=True)["href"]:
                href = elements[1].find("a", href=True)["href"]
                print("Fetching", constant.BASE + href)
                classified = session.get(constant.BASE + href, headers = getHeaders, timeout = constant.TIMEOUT)
                if classified.status_code == 200:
                     print("Fetching data for", href)
                else:
                     print("Unable to fetch data for", href)
    else:
        print("Error fetching classifieds.")

getClassifieds()
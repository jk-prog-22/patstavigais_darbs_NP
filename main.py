import requests
import constant
import logging
from bs4 import BeautifulSoup

headers = {
    'User-Agent': constant.USERAGENT
}

postData = {
    "topt[8][min]": "",
    "topt[8][max]": "",
    "topt[18][min]": "2016",
    "topt[18][max]": "",
    "topt[15][min]": "2.5",
    "topt[15][max]": "",
    "opt[34]": "",
    "opt[35]": "497",
    "opt[32]": "",
    "opt[17]": "",
    "sid": "/en/transport/cars/today/filter/"
}

if constant.DEBUG == True:
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def getClassifieds(url = constant.FILTER, filters = []):
    session = requests.Session()
    page = session.post(url, headers = headers, data = postData, timeout = constant.TIMEOUT, allow_redirects = True)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
        for vehicle in vehicles:
            elements = vehicle.findAll("td")
            href = elements[1].find("a", href=True)["href"]
            classified = session.get(constant.BASE + href, headers = headers, timeout = constant.TIMEOUT)
            if page.status_code == 200:
                print("Fetching data for", href)
            else:
                print("Unable to fetch data for", href)
            break
    else:
        print("Error fetching classifieds.")

getClassifieds()
import requests
import constant
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

def getClassifieds(url = constant.BASE, filters = []):
    page = requests.post(url, headers = headers, data = postData, timeout = constant.TIMEOUT)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
        for vehicle in vehicles:
            print(vehicle.text)
    else:
        print("Error fetching classifieds.")

getClassifieds()
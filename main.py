import requests
import constant
import logging
from bs4 import BeautifulSoup

getHeaders = {
    "Referer": "https://www.ss.com/en/transport/cars/filter/",
    "User-Agent": constant.USERAGENT
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    getContents = session.get(constant.FILTER, headers = getHeaders, timeout = constant.TIMEOUT, allow_redirects = True)
    if getContents.status_code == 200:
        soup = BeautifulSoup(getContents.content, 'html.parser')
        vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
        for vehicle in vehicles:
            elements = vehicle.findAll("td")
            try:
                href = elements[1].find("a", href=True)["href"]
                classified = session.get(constant.BASE + href, headers = getHeaders, timeout = constant.TIMEOUT)
                if classified.status_code == 200:
                    cSoup = BeautifulSoup(classified.content, 'html.parser')
                    try:
                        year = int(cSoup.find("td", {"id": "tdo_18"}).text.split()[0])
                    except AttributeError:
                        print(f"{bcolors.WARNING}Skipping: Unable to retrieve year for", href)
                        continue
                    try:
                        price = int(cSoup.find("span", {"id": "tdo_8"}).text.replace(" ", "").replace("€", ""))
                    except AttributeError:
                        print(f"{bcolors.WARNING}Skipping: Unable to retrieve price for", href)
                        continue

                    # Filtering year
                    # TODO: Probably could use range with one if call
                    if (constant.FILTERS["year"][0] != -1 and year < constant.FILTERS["year"][0]):
                        print(f"{bcolors.HEADER}", href, "year", year, "<",constant.FILTERS["year"][0])
                        continue
                    elif (constant.FILTERS["year"][1] != -1 and year > constant.FILTERS["year"][1]):
                        print(f"{bcolors.HEADER}", href, "year", year, ">", constant.FILTERS["year"][1])
                        continue

                    # Filtering price
                    if (constant.FILTERS["price"][0] != -1 and price < constant.FILTERS["price"][0]):
                        print(f"{bcolors.HEADER}", href, "price", price, "<", constant.FILTERS["price"][0])
                        continue
                    elif (constant.FILTERS["price"][1] != -1 and price > constant.FILTERS["price"][1]):
                        print(f"{bcolors.HEADER}", href, "price", price, ">", constant.FILTERS["price"][1])
                        continue

                    print(f"{bcolors.OKGREEN}Vehicle fits the request:", constant.BASE + href)
                else:
                    print(f"{bcolors.FAIL}Error: Unable to fetch data for", href)
            except IndexError:
                continue
    else:
        print("Error fetching classifieds.")

getClassifieds()
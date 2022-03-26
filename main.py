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

def getClassifieds(url = constant.FILTER):
    session = requests.Session()
    getContents = session.get(url, headers = getHeaders, timeout = constant.TIMEOUT, allow_redirects = True)
    if getContents.status_code == 200:
        soup = BeautifulSoup(getContents.content, 'html.parser')
        nextPage = soup.findAll("a", {"class" : "navi"})[-1]["href"].strip()
        vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
        for vehicle in vehicles:
            elements = vehicle.findAll("td")
            try:
                href = elements[1].find("a", href=True)["href"]
                classified = session.get(constant.BASE + href, headers = getHeaders, timeout = constant.TIMEOUT)
                if classified.status_code == 200:
                    cSoup = BeautifulSoup(classified.content, 'html.parser')

                    # Parsing the vehicles year
                    try:
                        year = int(cSoup.find("td", {"id": "tdo_18"}).text.split()[0])
                    except AttributeError:
                        print(f"{bcolors.WARNING}Skipping: Unable to retrieve year for", href)
                        continue

                    # Parsing the vehicles price
                    try:
                        price = int(cSoup.find("span", {"id": "tdo_8"}).text.replace(" ", "").replace("€", ""))
                    except AttributeError:
                        print(f"{bcolors.WARNING}Skipping: Unable to retrieve price for", href)
                        continue

                    # Parsing the vehicles engine capacity
                    try:
                        capacity = float(cSoup.find("td", {"id": "tdo_15"}).text.split()[0])
                    except AttributeError:
                        print(f"{bcolors.WARNING}Skipping: Unable to retrieve engine capacity for", href)
                        continue

                    # Filtering year
                    # TODO: Probably could use range with one if call
                    yearMin = constant.FILTERS["year"][0]
                    yearMax = constant.FILTERS["year"][1]
                    if (yearMin != -1 and year < yearMin):
                        print(f"{bcolors.HEADER}", href, "year", year, "<", yearMin)
                        continue
                    elif (yearMax != -1 and year > yearMax):
                        print(f"{bcolors.HEADER}", href, "year", year, ">", yearMax)
                        continue

                    # Filtering price
                    priceMin = constant.FILTERS["price"][0]
                    priceMax = constant.FILTERS["price"][1]
                    if (priceMin != -1 and price < priceMin):
                        print(f"{bcolors.HEADER}", href, "price", price, "<", priceMin)
                        continue
                    elif (priceMax != -1 and price > priceMax):
                        print(f"{bcolors.HEADER}", href, "price", price, ">", priceMax)
                        continue

                    # Filtering engine capacity
                    capMin = constant.FILTERS["capacity"][0]
                    capMax = constant.FILTERS["capacity"][1]
                    if (capMin != -1 and capacity < capMin):
                        print(f"{bcolors.HEADER}", href, "engine capacity", capacity, "<", capMin)
                        continue
                    elif (capMax != -1 and price > capMax):
                        print(f"{bcolors.HEADER}", href, "engine capacity", capacity, ">", capMax)
                        continue

                    print(f"{bcolors.OKGREEN}Vehicle fits the request:", constant.BASE + href)
                else:
                    print(f"{bcolors.FAIL}Error: Unable to fetch data for", href)
            except IndexError:
                continue
    else:
        print("Error fetching classifieds.")
    
    if "page" in nextPage:
        print(f"{bcolors.OKBLUE}Switching page:", nextPage)
        getClassifieds(constant.BASE + nextPage)

getClassifieds()
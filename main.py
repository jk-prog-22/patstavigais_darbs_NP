import requests
import constant
import logging
from bs4 import BeautifulSoup

postHeaders = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.ss.com",
    "Referer": "https://www.ss.com/en/transport/cars/filter/",
    "User-Agent": constant.USERAGENT
}

getHeaders = {
    "Referer": "https://www.ss.com/en/transport/cars/filter/",
    "User-Agent": constant.USERAGENT
}

cookies = {"LG": "en"}
postData = "topt%5B8%5D%5Bmin%5D=&topt%5B8%5D%5Bmax%5D=&topt%5B18%5D%5Bmin%5D=2016&topt%5B18%5D%5Bmax%5D=&topt%5B15%5D%5Bmin%5D=2.5&topt%5B15%5D%5Bmax%5D=&opt%5B34%5D=&opt%5B35%5D=497&opt%5B32%5D=488&opt%5B17%5D=&sid=%2Fen%2Ftransport%2Fcars%2Ffilter%2F"

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
    postContents = session.post(url, headers = postHeaders, data = postData, cookies = cookies, timeout = constant.TIMEOUT, allow_redirects = False)
    if postContents.status_code == 302:
        getContents = session.post(constant.BASE + postContents.headers["Location"], headers = getHeaders, timeout = constant.TIMEOUT, allow_redirects = True)
        if getContents.status_code == 200:
            soup = BeautifulSoup(getContents.content, 'html.parser')
            vehicles = soup.findAll("tr", {"id" : lambda L: L and L.startswith('tr_')})
            for vehicle in vehicles:
                elements = vehicle.findAll("td")
                if elements[1].find("a", href=True)["href"]:
                    href = elements[1].find("a", href=True)["href"]
                    print("Fetching", constant.BASE + href)
                    # classified = session.get(constant.BASE + href, headers = headers, timeout = constant.TIMEOUT)
                    # if page.status_code == 200:
                    #     print("Fetching data for", href)
                    # else:
                    #     print("Unable to fetch data for", href)
        else:
            print("Error fetching classifieds.")
    else:
        print("Error: HTTP response code", postContents.status_code, "expecting 302")

getClassifieds()
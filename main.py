import requests
import constant
from bs4 import BeautifulSoup

page = requests.get(constant.BASE)
soup = BeautifulSoup(page.content, 'html.parser')

vehicles = soup.find_all('table')
print(vehicles)
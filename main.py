import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.ss.com/en/transport/cars/today/filter/")
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify())
# LEARNING WEB SCRAPING: PRACTICE
# SOURCE: https://www.analyticsvidhya.com/blog/2021/08/a-simple-introduction-to-web-scraping-with-beautiful-soup/

import pip
from bs4 import BeautifulSoup 
import requests
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_greenhouse_gas_emissions'
req = requests.get(url)
soup = BeautifulSoup(req.text,"html.parser")
print(soup)
rows = soup.find_all('tr')
print(len(rows))
print(rows[0])



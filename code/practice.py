# LEARNING WEB SCRAPING: PRACTICE
# SOURCE: https://www.analyticsvidhya.com/blog/2021/08/a-simple-introduction-to-web-scraping-with-beautiful-soup/

import pip
from bs4 import BeautifulSoup 
import requests
import pandas as pd
file_path = "C:/Users/khilto01/Documents/git/web-scraping-gr/outputs/"
####
# Set URL, make soup
####
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_greenhouse_gas_emissions'
req = requests.get(url)
soup = BeautifulSoup(req.text,"html.parser")

print(soup)
soup.head
soup.body
soup.body.h1

####
# Find all rows
# (tr tag: https://www.w3schools.com/tags/tag_tr.asp)
####

## Note: find finds first instance, find all is all instances
rows = soup.find_all('tr')
print(len(rows))
print(rows[0])

####
# EXAMPLE ROW 2
####
print(test)
v = test.find_all('td')
for i,c in enumerate(v):
    text = c.text.replace('xa0', '').rstrip()
    print(text)

####
# Extracting elements of table
####
## Finding column names (text of first row)
cols = [t.text.rstrip() for t in rows[1].find_all('th')]
cols.insert(0, 'Country')

## Renaming 2022 columns that are all same name
cols[6] = '2022 (per capita)'
cols[7] = '2022 (perc of world)'
cols[8] = '2022 (change from 1990)'

## Creating dictionary of columns with empty values
dict = {c:[] for c in cols}

## Note: just doing 2-209 (to zimbabwe)
## Iterate over the rows of the table to extract info
for r in rows[2:209]:
    ## Getting values
    v = r.find_all('td')
    ## Loop through values + add to dictionary
    for i,c in enumerate(v):
        cell_text = c.text.replace('\xa0', '').replace('\n', '').rstrip()
        dict[cols[i]].append(cell_text)

####
# Save table as CSV (using file path set above)
####
df = pd.DataFrame(dict)
df.head()
df.to_csv(file_path + 'practice_table.csv', sep=',', index=False, encoding='utf-8')

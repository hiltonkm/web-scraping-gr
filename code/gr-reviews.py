## GOOD READS SCRAPING PRACTICE
## Scraping Reviews on Manhunt
## This book was review bombed by a bunch of TERF's :(
## NOTE: This only scrapes the first 30 reviews- I think to get the rest I need to learn more about selenium

## SOURCES:
## - https://github.com/maria-antoniak/goodreads-scraper

# Importing Packages
import pip
import re
from bs4 import BeautifulSoup 
import requests
import pandas as pd

# Setting Links
file_path = "C:/Users/khilto01/Documents/git/web-scraping-gr/outputs/"
book_links = ["https://www.goodreads.com/book/show/53329296/reviews"]
link = book_links[0]

# Grabbing HTML info
response = requests.get(link)
response.status_code == 200
# Soup :)
soup = BeautifulSoup(response.text,"html.parser")


# Reviews List
reviews = soup.find_all(class_= "ReviewCard")
r = reviews[0]
review_list = []
for r in reviews:
    review_author = r.find(class_="ReviewerProfile__name").text
    if type(r.find(attrs={"aria-label": re.compile("Rating")})).__name__ == 'NoneType':
        review_stars = ""
    else:
        review_stars = r.find(attrs={"aria-label": re.compile("Rating")})['aria-label']
    review_date = r.find(class_="Text Text__body3").text
    review_text = r.find(class_ = "ReviewText").text
    review_compiled = {"Review Author": review_author,
                       "Rating": review_stars,
                       "Date of Review": review_date,
                       "Review Text": review_text}
    review_list.append(review_compiled)
review_list

## Saving the final result as a csv
review_list_df = pd.DataFrame(review_list)
review_list_df.to_csv(file_path + "manhunt reviews.csv", index=False)
## GOOD READS SCRAPING PRACTICE
## Scraping information on Gretchen Felker-Martin's book Manhunt (my favorite book that I have read in the past month, it is so good)
## Practice web-scraping/ useing beautiful soup with python

## SOURCES:
## - https://github.com/maria-antoniak/goodreads-scraper
## - https://medium.com/@nikhil-1e9/web-scraping-popular-books-on-goodreads-using-python-4f03b6e1b5a0

# Importing Packages
import pip
import re
from bs4 import BeautifulSoup 
import requests
import pandas as pd

# Setting Links
file_path = "C:/Users/khilto01/Documents/git/web-scraping-gr/outputs/"
manhunt_link = "https://www.goodreads.com/book/show/53329296-manhunt"

# Grabbing HTML info
response = requests.get(manhunt_link)
print(response.status_code)

# Soup :)
soup = BeautifulSoup(response.text,"html.parser")

# TITLE
title = soup.find('h1').text

# PUBLISHED DATE
date = soup.find(string=re.compile(r'First published')).text

# AUTHOR
author = soup.find("span", attrs={"data-testid": "name"}).text

# PAGE #'S/ BOOK TYPE
pages = soup.find(string=re.compile(r'[0-9]+ pages')).text

# GENRES
genres = soup.find_all("a", href=re.compile("genres"))
genre_list = []
for g in genres:
    text = g.text
    print(text)
    if text == "Genres":
        next
    else:
        genre_list.append(text)

# # OF RATINGS
number_of_ratings = soup.find("span", attrs={"data-testid": "ratingsCount"}).text.replace('\xa0ratings', '').rstrip()

# # OF REVIEWS
number_of_reviews = soup.find("span", attrs={"data-testid": "reviewsCount"}).text.replace('\xa0reviews', '').rstrip()

# AVERAGE RATING
average_rating = soup.find("div", class_= "RatingStatistics__rating").text

# RATING DISTRIBUTION
rating_dist = soup.find_all("div", class_= "RatingsHistogram__labelTotal")

for i in range(len(rating_dist)):
    rating_dist[i] = rating_dist[i].text

rating_dist_dict = {"1 star": rating_dist[4],
                    "2 stars": rating_dist[3],
                    "3 stars": rating_dist[2],
                    "4 stars": rating_dist[1],
                    "5 stars": rating_dist[0]}

# Outputting all above measures to a CSV
book_info = {'Title': title,
             'Author': author,
             'Published Date': date,
             'Page Numbers/Book Type': pages,
             'Genres': ", ".join(genre_list),
             'Number of Ratings': number_of_ratings,
             'Number of Reviews': number_of_reviews,
             'Average Rating': average_rating,
             'Rating Distribution': ', '.join(key + ": " + str(val) for key, val in rating_dist_dict.items())}

book_info_df = pd.DataFrame(book_info, index=[0])
book_info_df.to_csv(file_path + "Manhunt.csv", index=False)

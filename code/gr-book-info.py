## GOOD READS SCRAPING PRACTICE
## Scraping information on my favorites shelf of goodreads

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
book_links = ["https://www.goodreads.com/book/show/53329296-manhunt",
              "https://www.goodreads.com/book/show/586852.The_Wall",
              "https://www.goodreads.com/book/show/13456414-a-short-stay-in-hell",
              "https://www.goodreads.com/book/show/51582376-the-secret-lives-of-church-ladies",
              "https://www.goodreads.com/book/show/77265030-against-technoableism",
              "https://www.goodreads.com/book/show/98653925-idlewild",
              "https://www.goodreads.com/book/show/62831518-helen-house",
              "https://www.goodreads.com/book/show/59366193-all-s-well",
              "https://www.goodreads.com/book/show/50887097-why-fish-don-t-exist",
              "https://www.goodreads.com/book/show/61111274-hijab-butch-blues",
              "https://www.goodreads.com/book/show/59095820-miss-major-speaks",
              "https://www.goodreads.com/book/show/7331435-a-visit-from-the-goon-squad",
              "https://www.goodreads.com/book/show/50371656-love-me-tender",
              "https://www.goodreads.com/book/show/35838277-paul-takes-the-form-of-a-mortal-girl",
              "https://www.goodreads.com/book/show/43317482-in-the-dream-house",
              "https://www.goodreads.com/book/show/59093587-patricia-wants-to-cuddle",
              "https://www.goodreads.com/book/show/40864002-a-psalm-for-the-wild-built",
              "https://www.goodreads.com/book/show/57846320-the-school-for-good-mothers",
              "https://www.goodreads.com/book/show/58395049-true-biz"]
## NOTE: These are my top goodreads books, request is currently pending with goodreads to have access to date (they no
## longer support an API)

## Creating function to pull basic information on each book
def get_book_info(url):
    # Grabbing HTML info
    response = requests.get(url)
    response.status_code == 200
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
    return(book_info)

## Running function through links of favorites books
final = []
for l in book_links:
    final.append(get_book_info(l))

## Saving the final result as a csv
book_info_df = pd.DataFrame(final)
book_info_df.to_csv(file_path + "all_books.csv", index=False)

import lxml
import re
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from requests import get

url = "https://www.imdb.com/chart/top/"


class DataIngestion:
    def __init__(self, url):
        super(DataIngestion, self).__init__()
        page = get(url)

        self.soup = BeautifulSoup(page.content, "lxml")

    def body_content(self):
        content = self.soup.find(id="main")
        return content.find_all("tbody", class_="lister-list")

    def movie_body_content(self, movie_url: str):
        movie_page = get(movie_url)
        movie_soup = BeautifulSoup(movie_page.content, "lxml")
        return movie_soup

    def movie_data(self):
        top_page = self.body_content()

        for movie_rows in top_page:
            movie_row = movie_rows.find_all("td", class_="titleColumn")
            for movie_info in movie_row:
                href = movie_info.find(href=True)
                movie_url = f'https://www.imdb.com{href["href"]}'
                movie_page = self.movie_body_content(movie_url)
                movie_content_top = movie_page.find_all("div", class_="main", id="main_top")
                movie_content_bottom = movie_page.find_all("div", class_="main", id="main_bottom")

                top_wrapper = movie_content_top[0].find("div", class_="title_wrapper")
                plot_summary_wrapper = movie_content_top[0].find("div", class_="plot_summary_wrapper")
                plot_wrapper = movie_content_bottom[0].find("div", class_="inline canwrap").span.text
                cast_wrapper = movie_content_bottom[0].find("div", class_="article", id="titleCast").table

                cast_row = cast_wrapper.find_all("td", class_="")
                cast_list = []
                for row in cast_row:
                    try:
                        cast_list.append(row.find("a").text.replace("\n", ""))
                    except:
                        pass
                plot_summary = plot_summary_wrapper.div.find("div", class_="summary_text").text
                director = plot_summary_wrapper.div.find("div", class_="credit_summary_item").a.text

                rating = movie_content_top[0].find("div", class_="ratingValue").text
                title = top_wrapper.h1.text
                release_year = top_wrapper.h1.a.text
                runtime = top_wrapper.div.time.text
                genre = top_wrapper.div.a.text

                print(plot_wrapper)
                # for content in movie_content_top:
                #     print(content)
                #     print("*" * 50)
                break

                # print(movie_url)

        return


ingest = DataIngestion(url)
data = ingest.movie_data()


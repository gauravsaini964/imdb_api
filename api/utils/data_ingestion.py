import lxml

from bs4 import BeautifulSoup
from requests import get
import re

from api.models import Movie, Actor, Director, MovieActor


class DataIngestion:

    # url = "https://www.imdb.com/chart/top/"

    def __init__(self, url):
        self.url = url
        self.page = get(self.url)
        self.soup = BeautifulSoup(self.page.content, "lxml")

    @staticmethod
    def compute_runtime(time_str: str):

        runtime = time_str.split(" ")
        hour = int("".join(filter(str.isdigit, runtime[0]))) * 60
        minute = int("".join(filter(str.isdigit, runtime[1])))
        return hour + minute

    def body_content(self):
        content = self.soup.find(id="main")
        return content.find_all("tbody", class_="lister-list")

    def movie_body_content(self, movie_url: str):
        movie_page = get(movie_url)
        movie_soup = BeautifulSoup(movie_page.content, "lxml")
        return movie_soup

    def write_movie_data(self, data):
        cast_list = data["cast_list"]
        director = data["director"]
        del data["cast_list"]
        del data["director"]
        director_name = director.split(" ")
        director = Director.objects.filter(first_name=director_name[0], last_name=director_name[1]).update_or_create(
            first_name=director_name[0], last_name=director_name[1]
        )
        data["director_id"] = director[0].id
        movie_obj = Movie.objects.filter(title=data["title"]).update_or_create(**data)
        for actor in cast_list:
            actor_name = actor.split(" ")
            actor_create = Actor.objects.filter(first_name=actor_name[0], last_name=actor_name[1]).update_or_create(
                first_name=actor_name[0], last_name=actor_name[1]
            )
            actor_id = actor_create[0].id
            movie_actor = MovieActor.objects.filter(actor_id=actor_id, movie_id=movie_obj[0].id).get_or_create(
                actor_id=actor_id, movie_id=movie_obj[0].id
            )
            print(movie_actor)

        print(movie_obj)

    def fetch_movie_data(self):
        top_page = self.body_content()

        for movie_rows in top_page:
            movie_row = movie_rows.find_all("td", class_="titleColumn")
            for movie_info in movie_row:
                final_movie_data = {}
                href = movie_info.find(href=True)
                movie_url = f'https://www.imdb.com{href["href"]}'
                movie_page = self.movie_body_content(movie_url)
                movie_content_top = movie_page.find_all("div", class_="main", id="main_top")
                movie_content_bottom = movie_page.find_all("div", class_="main", id="main_bottom")
                top_wrapper = movie_content_top[0].find("div", class_="title_wrapper")
                plot_summary_wrapper = movie_content_top[0].find("div", class_="plot_summary_wrapper")
                final_movie_data["plot"] = (
                    movie_content_bottom[0].find("div", class_="inline canwrap").span.text.strip()
                )
                cast_wrapper = movie_content_bottom[0].find("div", class_="article", id="titleCast").table

                cast_row = cast_wrapper.find_all("td", class_="")
                final_movie_data["cast_list"] = []
                for row in cast_row:
                    try:
                        final_movie_data["cast_list"].append(row.find("a").text.replace("\n", "").strip())
                    except:
                        pass
                final_movie_data["plot_summary"] = plot_summary_wrapper.div.find(
                    "div", class_="summary_text"
                ).text.strip()
                final_movie_data["director"] = plot_summary_wrapper.div.find(
                    "div", class_="credit_summary_item"
                ).a.text.strip()

                final_movie_data["ratings"] = (
                    movie_content_top[0].find("div", class_="ratingValue").text.strip().split("/")[0]
                )
                final_movie_data["title"] = top_wrapper.h1.text.strip()
                final_movie_data["release_year"] = top_wrapper.h1.a.text.strip()
                # runtime = top_wrapper.div.time.text.strip()
                final_movie_data["runtime"] = self.compute_runtime(top_wrapper.div.time.text.strip())
                final_movie_data["genre"] = top_wrapper.div.a.text.strip()

                self.write_movie_data(final_movie_data)
        return


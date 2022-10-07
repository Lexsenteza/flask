from bs4 import BeautifulSoup
import requests

URL = "https://www.billboard.com/charts/hot-100/"


class TopSongs:

    def __init__(self, date_back: str):
        self.url = URL
        self.soup = self.make_soup(date_back)

    def make_soup(self, date):
        response = requests.get(f"{self.url}{date}")
        hot_100 = response.text
        return BeautifulSoup(hot_100, "html.parser")

    def title_lists(self) -> list:
        scrapped_title_list = self.soup.find_all(name="h3", id="title-of-a-story", class_="a-truncate-ellipsis")
        title_list = [(item.get_text()).strip("\n\t") for item in scrapped_title_list]
        return title_list

    def artist_list(self):
        scrapped_artist_list = self.soup.find_all(name="span", class_="a-truncate-ellipsis-2line")
        artist_list = [(item.get_text()).strip("\n\t") for item in scrapped_artist_list]
        return artist_list

    def song_list(self):
        song_list = []
        for number in range(0, len(self.title_lists())):
            song_dictionary = {
                "artist": self.artist_list()[number],
                "song": self.title_lists()[number],
            }
            song_list.append(song_dictionary)
        return song_list


import requests

from util import config


class Song:

    def __init__(self, name: str = None, id: int = None):

        self.name = name
        self.id = id

    @property
    def data(self):
        if self.id:
            return requests.get(f"https://api.genius.com/songs/{self.id}?access_token={config.getGeniusKey()}").json()["response"]["song"]
        if self.name:
            return requests.get(f"https://api.genius.com/search?q={self.name.replace(' ', '%20')}&access_token={config.getGeniusKey()}").json()["response"]["hits"]


    @property
    def api_path(self):
        if self.id:
            return f"/songs/{self.id}"
        if self.name:
            return self.data[0]["result"]["api_path"]

    @property
    def song_info(self):
        if self.id:
            return requests.get(f"https://api.genius.com/songs/{self.id}?access_token={config.getGeniusKey()}").json()[
                "response"]["song"]
        if self.name:
            return requests.get(f"https://api.genius.com{self.api_path}?access_token={config.getGeniusKey()}").json()["response"]["song"]

    @property
    def media(self):
        return self.song_info["media"]

    def str(self):
        return {"name": self.name, "id": self.id}

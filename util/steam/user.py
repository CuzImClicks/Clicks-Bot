import urllib.request
import json
from clicks_util.json_util import JsonFile
#from util import config  # module not found error, don't know why
import logging
from clicks_util import logger

lg = logging.getLogger(__name__[10:])


class User:

    def __init__(self, steam_id: int):
        self.steam_id = steam_id

    @property
    def url(self):
        return "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="\
               + "292177DC524546D1D4B31BA0CF3D1FF0"\
               + "&steamids=" + str(self.steam_id) + "&format=json"

    @property
    def Request(self) -> urllib.request.Request:
        return urllib.request.Request(self.url, data=None, headers=self.req_headers, origin_req_host=None)

    @property
    def response(self) -> urllib.request:
        return urllib.request.urlopen(self.Request)

    @property
    def content(self) -> str:
        return self.response.read()

    @property
    def data(self) -> json:
        return json.loads(self.content)

    @property
    def req_headers(self) -> dict:
        return {"User-Agent": "Python script"}

    @property
    def player(self) -> str:
        return self.data["response"]["players"][0]

    @property
    def name(self) -> str:
        return self.player["personaname"]

    @property
    def state(self) -> int:
        return int(self.player["personastate"])

    @property
    def avatar(self) -> str:
        return str(self.player["avatarmedium"])

    def __dict__(self):
        return {self.name: {"name": self.name, "steam_id": self.steam_id, "state": self.state}}

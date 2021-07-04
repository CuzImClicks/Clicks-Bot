import requests
from mojang import MojangAPI


class User:

    def __init__(self, nickname):

        self.nickname = nickname

    def get_uuid(self):

        return MojangAPI.get_uuid(self.nickname)

    def __str__(self):
        return f"{self.nickname} - {self.get_uuid()}"

    @property
    def skin(self):
        return requests.get(f"https://crafatar.com/renders/body/" + self.get_uuid()).json()

    @property
    def avatar(self):
        return requests.get("https://crafatar.com/renders/avatars/" + self.get_uuid()).json()

    @property
    def head(self):
        return requests.get("https://crafatar.com/renders/head/"+ self.get_uuid()).json()

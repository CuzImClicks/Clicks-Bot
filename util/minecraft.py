from mojang import MojangAPI
import requests


class User:

    def __init__(self, nickname):

        self.nickname = nickname

    def get_uuid(self):

        return MojangAPI.get_uuid(self.nickname)

    @property
    def skin(self):
        return requests.get(f"https://crafatar.com/renders/body/" + self.get_uuid()).json()

    @property
    def avatar(self):
        return requests.get("https://crafatar.com/renders/avatars/" + self.get_uuid()).json()

    @property
    def head(self):
        return requests.get("https://crafatar.com/renders/head/"+ self.get_uuid()).json()

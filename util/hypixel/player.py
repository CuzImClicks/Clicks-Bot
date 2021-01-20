import json

import aiohttp
import requests
from util.minecraft import User
from util import config
import logging
import os

lg = logging.getLogger(__name__)
key = config.getKey()
path = os.getcwd()


class Player:

    def __init__(self, name):
        self.name = name
        self.user = User(name)
        self.uuid = self.user.get_uuid()
        self.save()
        self.skyblock = self.SkyBlock(self.data, self.name, self.uuid)

    @property
    def data(self):
        return requests.get(f"https://api.hypixel.net/player?key={key}&player={self.name}&uuid={self.uuid}").json()

    @property
    def profile_id(self):

        return self.data["player"]["_id"]

    def save(self):

        with open(f"{path}/hypixel/{self.name}.json", "w+") as f:
            json.dump(self.data, f, indent=2)

    class SkyBlock:

        def __init__(self, data: dict, name, uuid):
            self.name = name
            self.data = data
            self.profiles_raw = self.data["player"]["stats"]["SkyBlock"]["profiles"]
            self.profiles_data = dict()
            self.profiles = dict()
            for value in self.profiles_raw.values():
                profile = self.Profile(value, uuid)
                self.profiles_data[value["cute_name"]] = profile.content
                self.profiles[profile.name] = profile

            self.save()

        def save(self):
            with open(f"{path}/hypixel/{self.name}-Skyblock.json", "w+") as f:
                f.write(json.dumps(self.profiles_data, indent=2))

        class Profile:

            def __init__(self, profile: dict, uuid: str):
                self.profile = profile
                self.uuid = uuid

            @property
            def content(self):
                return requests.get(
                    f"https://api.hypixel.net/skyblock/profile?key={key}&profile={self.profile['profile_id']}").json()

            @property
            def data_profile(self):
                return self.content["profile"]["members"][self.uuid]

            @property
            def profile_id(self):
                return self.profile["profile_id"]

            @property
            def name(self):
                return self.profile["cute_name"]

            @property
            def fairy_souls_collected(self):
                return self.data_profile["fairy_souls_collected"]

            @property
            def stats(self):
                return self.data_profile["stats"]

            @property
            def death_count(self):
                return self.data_profile["death_count"]

            @property
            def slayer(self):
                return self.data_profile["slayer"]

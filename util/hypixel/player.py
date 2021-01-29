import json
from datetime import datetime
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
                self.user = self.User(self.data_profile)

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

            class User:

                def __init__(self, profile_data):
                    self.profile_data = profile_data
                    self.stats = self.Stats(self.profile_data["stats"])
                    self.slayers = list()
                    #FIXME: TypeError: unhashable type: 'dict'
                    #for slayerboss in list(self.profile_data["slayer_bosses"].values()):
                    #    self.slayers.append(self.SlayerBoss(slayerboss, self.profile_data["slayer_bosses"][slayerboss]))

                @property
                def fairy_souls_collected(self):
                    return self.profile_data["fairy_souls_collected"]

                @property
                def death_count(self):
                    return self.profile_data["death_count"]

                @property
                def last_save(self):
                    #FIXME: OSError: [Errno 22] Invalid argument
                    return datetime.fromtimestamp(int(self.profile_data["last_save"]))

                @property
                def inv_armor(self):
                    return str(self.profile_data["inv_armor"]["data"]).split("/")

                @property
                def coop_invitation(self):
                    return self.profile_data["coop_invitation"]

                @property
                def first_join(self):
                    return self.profile_data["first_join"]

                @property
                def first_join_hub(self):
                    return self.profile_data["first_join_hub"]

                class Stats:

                    def __init__(self, stats):

                        self.stats = dict(stats)

                    @property
                    def deaths(self):
                        return self.stats["deaths"]

                    @property
                    def deaths_void(self):
                        return self.stats["deaths_void"]

                    @property
                    def highest_critical_damage(self):
                        return self.stats["highest_critical_damage"]

                    @property
                    def kills(self):
                        return self.stats["kills"]

                    @property
                    def auctions_bids(self):
                        return self.stats["auctions_bids"]

                    @property
                    def auctions_highest_bid(self):
                        return self.stats["auctions_highest_bid"]

                    @property
                    def auctions_won(self):
                        return self.stats["auctions_won"]

                    @property
                    def auctions_gold_spent(self):
                        return self.stats["auctions_gold_spent"]

                    @property
                    def ender_crystals_destroyed(self):
                        return self.stats["ender_crystals_destroyed"]

                    def important_dict(self):
                        return {"stats": {"deaths": self.deaths,
                         "deaths_void": self.deaths_void,
                          "highest_critical_damage": self.highest_critical_damage,
                          "kills": self.kills,
                          "auctions_bids": self.auctions_bids,
                          "auctions_highest_bid": self.auctions_highest_bid,
                          "auctions_won": self.auctions_won,
                          "auctions_gold_spent": self.auctions_gold_spent,
                          "ender_crystals_destroyed": self.ender_crystals_destroyed}}

                    def __dict__(self):
                        return self.stats

                @property
                def coin_purse(self):
                    #FIXME: returns None
                    self.profile_data["coin_purse"]

                @property
                def last_death(self):
                    return self.profile_data["last_death"]

                @property
                def fairy_exchanges(self):
                    return self.profile_data["fairy_exchanges"]

                class SlayerBoss:

                    def __init__(self, name, slayer_data):

                        self.slayer_data = slayer_data
                        self.name = name

                    @property
                    def claimed_levels(self):
                        return list(self.slayer_data["claimed_levels"].values())

                    @property
                    def xp(self):
                        return self.slayer_data["xp"]

                class Pet:

                    def __init__(self, pet_data):

                        self.pet_data = pet_data

                    @property
                    def uuid(self):
                        return self.pet_data["uuid"]

                    @property
                    def name(self):
                        return str(self.pet_data["type"]).lower()

                    @property
                    def exp(self):
                        return self.pet_data["exp"]

                    @property
                    def active(self):
                        return self.pet_data["active"]

                    @property
                    def tier(self):
                        return str(self.pet_data["tier"]).lower()

                    @property
                    def heldItem(self):
                        return self.pet_data["heldItem"]

                    @property
                    def candyUsed(self):
                        return self.pet_data["candyUsed"]

                    @property
                    def skin(self):
                        return self.pet_data["skin"]



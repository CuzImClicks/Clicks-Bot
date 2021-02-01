import json
from datetime import datetime
import aiohttp
from nbt import nbt
import requests
from util.minecraft import User
from util import config
import logging
import os
from clicks_util import timeconvert, nbt_data

lg = logging.getLogger(__name__)
key = config.getKey()
path = os.getcwd()


class Player:

    def __init__(self, name: str):
        """[summary]

        Args:
            name (str): [name of the player]
        """
        self.name = name
        self.user = User(name)
        self.uuid = self.user.get_uuid()
        self.save()
        self.skyblock = self.SkyBlock(self.data, self.name, self.uuid)

    @property
    def data(self) -> dict:
        """[summary]

        Returns:
            dict: [api informations about the player]
        """
        return requests.get(f"https://api.hypixel.net/player?key={key}&player={self.name}&uuid={self.uuid}").json()

    @property
    def profile_id(self) -> int:
        """[summary]

        Returns:
            int: [the profile id of the player]
        """
        return self.data["player"]["_id"]

    def save(self):
        with open(f"{path}/hypixel/{self.name}.json", "w+") as f:
            json.dump(self.data, f, indent=2)

    class SkyBlock:

        def __init__(self, data: dict, name, uuid):
            """[summary]

            Args:
                data (dict): [data of the player]
                name ([type]): [name of the player]
                uuid ([type]): [uuid of the player]
            """
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
                """[summary]

                Args:
                    profile (dict): [profile from the data]
                    uuid (str): [uuid of the player]
                """
                self.profile = profile
                self.uuid = uuid
                self.user = self.User(self.data_profile)

            @property
            def content(self) -> dict:
                """[summary]

                Returns:
                    dict: [the profile's data]
                """
                return requests.get(
                    f"https://api.hypixel.net/skyblock/profile?key={key}&profile={self.profile['profile_id']}").json()

            @property
            def data_profile(self) -> dict:
                """[summary]

                Returns:
                    dict: [the players data of the profile]
                """
                return self.content["profile"]["members"][self.uuid]

            @property
            def profile_id(self) -> int:
                """[summary]

                Returns:
                    int: [the profile's id]
                """
                return self.profile["profile_id"]

            @property
            def name(self) -> str:
                """[summary]

                Returns:
                    str: [the ingame name of the profile("Kiwi", "Pineapple", "Orange", ...)]
                """
                return self.profile["cute_name"]

            class User:

                def __init__(self, profile_data: dict):
                    """[summary]

                    Args:
                        profile_data (dict): [the players data of the profile]
                    """
                    self.profile_data = profile_data
                    self.stats = self.Stats(self.profile_data["stats"])
                    self.slayers = list()
                    #FIXME: TypeError: unhashable type: 'dict'
                    #for slayerboss in list(self.profile_data["slayer_bosses"].values()):
                    #    self.slayers.append(self.SlayerBoss(slayerboss, self.profile_data["slayer_bosses"][slayerboss]))

                @property
                def fairy_souls_collected(self) -> int:
                    """[summary]

                    Returns:
                        int: [the amount of fairy souls collected]
                    """
                    return self.profile_data["fairy_souls_collected"]

                @property
                def death_count(self) -> int:
                    """[summary]

                    Returns:
                        int: [amount of deaths]
                    """
                    return self.profile_data["death_count"]

                @property
                def last_save(self) -> str:
                    """[summary]

                    Returns:
                        str: [date and time of last save]
                    """
                    return timeconvert.fulldatefromtimestamp(int(self.profile_data["last_save"]))

                @property
                def inv_armor(self):
                    #TODO: nbt encoded in base64
                    return str(self.profile_data["inv_armor"]["data"]).split("/")

                @property
                def coop_invitation(self) -> dict:
                    """[summary]

                    Returns:
                        dict: [timestamp of invite, invited by(uuid), confirmed(bool), confirmed timestamp]
                    """
                    return self.profile_data["coop_invitation"]

                @property
                def first_join(self) -> str:
                    """[summary]

                    Returns:
                        str: [full date and time of first join]
                    """
                    return timeconvert.fulldatefromtimestamp(int(self.profile_data["first_join"]))

                @property
                def first_join_hub(self) -> str:
                    """[summary]

                    Returns:
                        str: [full date and time of first join in the hub]
                    """
                    return timeconvert.fulldatefromtimestamp(int(self.profile_data["first_join_hub"]))

                class Stats:

                    #TODO: Documentation

                    def __init__(self, stats):

                        self.stats = dict(stats)

                    @property
                    def deaths(self) -> int:
                        """[summary]

                        Returns:
                            int: [amount of deaths]
                        """
                        return int(self.stats["deaths"])

                    @property
                    def deaths_void(self):
                        return self.stats["deaths_void"]

                    @property
                    def highest_critical_damage(self) -> int:
                        """[summary]

                        Returns:
                            int: [highest ever dealt crit damage]
                        """
                        return int(self.stats["highest_critical_damage"])

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
                def last_death(self) -> datetime.time:
                    return self.profile_data["last_death"]

                @property
                def fairy_exchanges(self) -> int:
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

                @property
                def dungeons(self) -> dict:
                    return dict(self.profile_data["dungeons"])

                @property
                def griffin(self) -> dict:
                    return dict(self.profile_data["griffin"])

                @property
                def jacob2(self) -> dict:
                    return dict(self.profile_data["jacob2"])

                @property
                def experimentation(self) -> dict:
                    return dict(self.profile_data["experimentation"])                

                @property
                def experience_skill_runecrafting(self) -> dict:
                    return dict(self.profile_data["experience_skill_runecrafting"])

                @property
                def experience_skill_combat(self) -> dict:
                    return dict(self.profile_data["experience_skill_combat"])    

                @property
                def experience_skill_mining(self) -> dict:
                    return dict(self.profile_data["experience_skill_mining"])  

                @property
                def unlocked_coll_tiers(self) -> dict:
                    return dict(self.profile_data["unlocked_coll_tiers"])  

                #TODO: Add more API options

                @property
                def quiver(self):
                    return nbt_data.decode_inventory_data(self.profile_data["quiver"])




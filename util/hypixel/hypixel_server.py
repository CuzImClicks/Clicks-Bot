import logging
import os

from aiohttp.client import ClientSession

from util import config

key = config.getHypixelKey()
lg = logging.getLogger(__name__)
path = os.getcwd()

class Hypixel:
    def __init__(self):
        pass

    @classmethod
    async def guild(self, name: str) -> dict:
        """[summary]

        Args:
            name (str): [Name of the player]

        Returns:
            dict: [guild as a dict]
        """
        async with ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/findGuild?key={key}&byName={name}") as response:
                data = await response.json()
                guildid = data["guild"]

        if guildid is None:
            return "ValueError"

        async with ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/guild?key={key}&id={guildid}") as response:
                return await response.json()

    @classmethod
    async def watchdog(self) -> dict:
        """[summary]

        Returns:
            dict: [the watchdog summary of the last week]
        """
        async with ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/watchdogstats?key={key}") as response:
                return await response.json()

    @classmethod
    async def leaderbords(self) -> dict:
        """[summary]

        Returns:
            dict: [the leaderboards of hypixel]
        """
        async with ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/leaderboards?key={key}") as response:
                return await response.json()

    @classmethod
    async def counts(self) -> dict:
        """[summary]

        Returns:
            dict: [the amount of players playing each gamemode]
        """
        async with ClientSession() as session:
            async with session.get('https://api.hypixel.net/gameCounts?key=' + key) as response:
                return await response.json()

    @classmethod
    async def mcserver(self, ip: str, port: str=25565) -> dict:
        async with ClientSession() as session:
            async with session.get(f'https://api.mcsrvstat.us/2/{ip}:{port}') as response:
                return await response.json()

    @classmethod
    async def playerguild(self, uuid: str) -> str:
        """[summary]

        Args:
            uuid (str): [uuid of a minecraft player]

        Returns:
            str: [name of the guild]
        """
        async with ClientSession() as session:
            async with session.get('https://api.hypixel.net/guild?key=' + key + '&player=' + uuid) as response:
                data = await response.json()
                if data['guild'] is None:
                    return 'None'
                return data['guild']['name']


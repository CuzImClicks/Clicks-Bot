import json
import aiohttp
import os
import logging
import requests
from util import minecraft
from util import config

key = config.getKey()
lg = logging.getLogger(__name__)
path = os.getcwd()

class Hypixel:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def guild(self, name: str) -> dict:
        async with self.session.get(f"https://api.hypixel.net/findGuild?key={key}&byName={name}") as response:
            data = await response.json()
            guildid = data["guild"]

        if guildid is None:
            return "ValueError"

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/guild?key={key}&id={guildid}") as response:
                return await response.json()

    async def watchdog(self) -> dict:
        async with self.session.get(f"https://api.hypixel.net/watchdogstats?key={key}") as response:
            return await response.json()

    async def leaderbords(self) -> dict:
        async with self.session.get(f"https://api.hypixel.net/leaderbords?key={key}") as response:
            return await response.json()

    async def counts(self) -> dict:
        async with self.session.get('https://api.hypixel.net/gameCounts?key=' + key) as response:
            return await response.json()

    async def mcserver(self, ip: str, port: str=25565) -> dict:
        async with self.session.get(f'https://api.mcsrvstat.us/2/{ip}:{port}') as response:
            return await response.json()

    async def playerguild(self, uuid) -> str:
        async with self.session.get('https://api.hypixel.net/guild?key=' + key + '&player=' + uuid) as response:
            data = await response.json()
            if data['guild'] is None:
                return 'None'
            return data['guild']['name']


import requests
import json
import logging
import aiohttp
from discord.ext import commands
from util.logger import path
from util import config
import asyncio
import discord
from datetime import datetime

key = "29c790dd-9d29-4b73-bf1e-c7fa88cff4c8"
lg = logging.getLogger(__name__)


class HypixelAPI_Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="online")
    async def online(self, ctx, playername):
        async with aiohttp.clientsession() as session:
            data = json.load("players.json")
            for player in data.keys():
                playername = player["name"]
                status = player["status"]
                async with session.get(f'https://api.slothpixel.me/api/players/{playername}/status') as data:
                    online = data[10:-35]
                if online == 'true' and status == "False":
                    infoEmbed = discord.Embed(title="Online", description=f"{playername} is now online", color=discord.Colour(0x000030), timestamp=datetime.now())
                    await ctx.send(embed=infoEmbed)
                elif online == "false" and status == "True":
                    infoEmbed = discord.Embed(title="Offline", description=f"{playername} is now offline",
                                              color=discord.Colour(0x000030), timestamp=datetime.now())
                    await ctx.send(embed=infoEmbed)

    class Player:

        def __init__(self, name, uuid):
            self.name = name
            self.uuid = uuid
            self.save()

        @property
        def data(self):
            return requests.get(f"https://api.hypixel.net/player?key={self.key}&player={self.name}&uuid={self.uuid}").json()

        @property
        def profile_id(self):

            return self.data["player"]["_id"]

        def save(self):

            with open(f"../hypixel/{self.name}.json", "w+") as f:
                json.dump(self.data, f, indent=2)

        @property
        def keys(self):
            return self.data["player"].keys()

        @property
        def key(self):
            return "29c790dd-9d29-4b73-bf1e-c7fa88cff4c8"

        def getSkyBlock(self):
            return self.SkyBlock(self.data, self.name)

        class SkyBlock:

            def __init__(self, data: dict, name):
                self.name = name
                self.data = data
                self.profiles = self.data["player"]["stats"]["SkyBlock"]["profiles"]
                self.profiles_data = dict()
                for value in self.profiles.values():
                    content = self.Profile(value).content
                    self.profiles_data[value["cute_name"]] = content

                self.save()

            def save(self):
                with open(f"../hypixel/{self.name}-Skyblock.json", "w+") as f:
                    f.write(json.dumps(self.profiles_data, indent=2))

            class Profile:

                def __init__(self, profile: dict):
                    self.data = profile

                @property
                def content(self):
                    return requests.get(
                        f"https://api.hypixel.net/skyblock/profile?key={key}&profile={self.data['profile_id']}").json()

                @property
                def profile_id(self):
                    return self.data["profile_id"]

                @property
                def name(self):
                    return self.data["cute_name"]


def setup(bot):

    bot.add_cog(HypixelAPI_Handler(bot))


'''cuz_im_clicks = Player("Cuz_Im_Clicks", "9c9cac92-358e-47b8-8697-f1df72f0e3b5")

cuz_im_clicks.getSkyBlock()'''


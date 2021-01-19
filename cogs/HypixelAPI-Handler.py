import requests
import json
import logging
import aiohttp
import aiofiles
from discord.ext import commands, tasks
from util.logger import path
from util import config
import asyncio
import discord
from datetime import datetime
import os
from clicks_util.json_util import json_file

key = "29c790dd-9d29-4b73-bf1e-c7fa88cff4c8"
lg = logging.getLogger(__name__)
path = os.getcwd()


class HypixelAPI_Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.online.start()

    def cog_unload(self):
        self.online.cancel()

    @property
    def player_channel(self):
        return self.bot.get_channel(799291117425524756)

    @tasks.loop(seconds=20.0)
    async def online(self):

        channel = self.player_channel
        if not channel:
            await asyncio.sleep(5)
            channel = self.player_channel
        async with aiohttp.ClientSession() as session:
            jf = json_file("players.json", f"{path}\cogs")
            jf_data = jf.read()
            for player in jf_data.keys():
                playername = jf_data[player]["name"]
                uuid = jf_data[player]["uuid"]
                status = bool(jf_data[player]["status"])
                async with session.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid}') as data:
                    content = json.loads(await data.text())
                    online = content["session"]["online"]
                if online == True and status == False:
                    game = content["session"]["gameType"]
                    infoEmbed = discord.Embed(title="Online", description=f"{playername} is in {game} now online",
                                              color=discord.Colour(0x000030), timestamp=datetime.now())
                    await channel.send(embed=infoEmbed)

                elif not online and status:
                    infoEmbed = discord.Embed(title="Offline", description=f"{playername} is in now offline",
                                              color=discord.Colour(0x000030), timestamp=datetime.now())
                    await channel.send(embed=infoEmbed)

                jf_data[player]["status"] = online
                jf.write(jf_data)

    @commands.command("magmaboss")
    @commands.has_role(config.getBotAdminRole())
    async def magmaboss(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://lametric.th3shadowbroker.dev/getEstimation/magmaBoss?leadingZeros=true") as data:
                content = json.loads(await data.text())

                infoEmbed = discord.Embed(title="Magma Boss", description=f"The magma boss spawns in {str(content['frames'][0]['text'])} hours")
                await ctx.send(embed=infoEmbed)

    @commands.command(name="bazaar", aliases=["bz"])
    async def bazaar(self, ctx, *args):
        if not args:
            infoEmbed = discord.Embed(title="Bazaar Help", description="Please write the english name of the item next to the command. ")
        item = args[0].upper()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/skyblock/bazaar?key={key}&productId={item}") as data:
                content = json.loads(await data.text())
                jf = json_file("bazaar.json", path=f"{path}\hypixel")
                jf.write(content)
                if not item in content["products"]:
                    errorEmbed = discord.Embed(title="Bazaar Error", description=f"ItemNotFound: {item} is not a supported item",colour=discord.Colour(0x9D1309))
                    await ctx.send(embed=errorEmbed)
                    lg.info(f"ItemNotFound: {item} is not a supported item")
                    return

                infoEmbed = discord.Embed(title="Bazaar", description=f"Informations about the sell and buy value of {item.lower()}")
                infoEmbed.add_field(name="Buy", value=f"Last bought for {str(round(content['products'][item]['quick_status']['sellPrice'], 2))} coins")
                infoEmbed.add_field(name="Sell", value=f"Last sold for {str(round(content['products'][item]['quick_status']['buyPrice'], 2))} coins")
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


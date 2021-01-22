import requests
import json
import logging
import aiohttp
from discord.ext import commands, tasks
from util.logger import path
from util import config
import asyncio
import discord
from datetime import datetime
import os
from util.minecraft import User
from clicks_util.json_util import json_file
from util.hypixel.player import Player

key = config.getKey()
lg = logging.getLogger(__name__)
path = os.getcwd()


class HypixelAPI_Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.online.start()  # start the task
        self.magmaboss.start()  # start the task

    def cog_unload(self):
        """Unload the tasks"""
        self.online.cancel()
        self.magmaboss.cancel()

    @property
    def player_channel(self):
        """Get the player online channel"""
        return self.bot.get_channel(799291117425524756)

    @property
    def magma_boss_channel(self):
        """Get the magma boss channel"""
        return self.bot.get_channel(799220589243007007)

    @commands.command(name="add_player")
    @commands.has_role(config.getBotAdminRole())
    async def add_player(self, ctx, playername):
        """Add a player to the hypixel online task
        by typing the command with the player's username"""
        user = User(playername)
        data = self.jf.read()
        data[playername] = {"name": playername, "uuid": user.get_uuid(), "status": False}
        self.jf.write(data)

    @tasks.loop(seconds=20.0)
    async def online(self):
        """Announce when players join or leave the hypixel network"""
        channel = self.player_channel
        if not channel:
            await asyncio.sleep(5)
            channel = self.player_channel
        async with aiohttp.ClientSession() as session:
            self.jf = json_file("players.json", f"{path}\cogs")
            jf_data = self.jf.read()
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
                self.jf.write(jf_data)

    @tasks.loop(minutes=1)
    async def magmaboss(self):
        """Announce when the SkyBlock magma boss is about to spawn"""
        channel = self.magma_boss_channel
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "http://lametric.th3shadowbroker.dev/getEstimation/magmaBoss?leadingZeros=true") as data:
                content = json.loads(await data.text())
                value = float(str(content['frames'][0]['text']).replace(":", "."))
                infoEmbed = discord.Embed(title="Magma Boss",
                                          description=f"The magma boss spawns in {value} hours", timestamp=datetime.now())
                if value <= 0.1:
                    await channel.send(embed=infoEmbed)

    @commands.command(name="bazaar", aliases=["bz"])
    @commands.has_role(config.getDefaultRole())
    async def bazaar(self, ctx, *args):
        """Get the last prices for an item in the Hypixel SkyBlock bazaar"""
        if not args:
            infoEmbed = discord.Embed(title="Bazaar Help",
                                      description="Please write the english name of the item next to the command. ")
        item = args[0].upper()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.hypixel.net/skyblock/bazaar?key={key}&productId={item}") as data:
                content = json.loads(await data.text())
                jf = json_file("bazaar.json", path=f"{path}\hypixel")
                jf.write(content)
                if not item in content["products"]:
                    errorEmbed = discord.Embed(title="Bazaar Error",
                                               description=f"ItemNotFound: {item} is not a supported item",
                                               colour=discord.Colour(0x9D1309))
                    await ctx.send(embed=errorEmbed)
                    lg.info(f"ItemNotFound: {item} is not a supported item")
                    return

                infoEmbed = discord.Embed(title="Bazaar",
                                          description=f"Informations about the sell and buy value of {item.lower()}")
                infoEmbed.add_field(name="Buy",
                                    value=f"Last bought for {str(round(content['products'][item]['quick_status']['sellPrice'], 2))} coins")
                infoEmbed.add_field(name="Sell",
                                    value=f"Last sold for {str(round(content['products'][item]['quick_status']['buyPrice'], 2))} coins")
                infoEmbed.add_field(name="SkyBlock Tools", value=f"https://skyblock-tool.xyz/product.php?id={item}",
                                    inline=False)
                await ctx.send(embed=infoEmbed)

    @commands.command(name="fairy_souls")
    @commands.has_role(config.getDefaultRole())
    async def fairy_souls(self, ctx, playername):
        """Get the collected fairy souls of a player"""
        lg.info(playername)
        pl = Player(playername)
        skyblock = pl.SkyBlock(pl.data, pl.name, pl.uuid)
        infoEmbed = discord.Embed(title="Fairy Souls",
                                  description=f"Showing collected fairy souls for user {playername}")
        for profile in list(skyblock.profiles.keys()):
            infoEmbed.add_field(name=profile, value=f"{skyblock.profiles[profile].fairy_souls_collected} of 220")

        await ctx.send(embed=infoEmbed)


def setup(bot):
    bot.add_cog(HypixelAPI_Handler(bot))

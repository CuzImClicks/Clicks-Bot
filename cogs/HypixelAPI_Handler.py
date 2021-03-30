import requests
import json
import logging
import aiohttp
from discord.ext import commands, tasks
from util import config
import asyncio
import discord
from datetime import datetime
import os
from varname import nameof
from util.minecraft import User
from clicks_util.json_util import JsonFile
from util.hypixel.player import Player
from clicks_util import info
from util.logger import path

key = config.getHypixelKey()
lg = logging.getLogger(__name__[5:])


class HypixelAPI_Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.jf = JsonFile("players.json", f"{path}")
        if config.getHypixelOnline():  # check if the feature is enabled
            lg.info(f"Started the Hypixel Online Tracker")
            self.online.start()  # start the task
        if config.getMagmaboss():
            lg.info(f"Started the Hypixel Magma Boss Tracker")
            self.magmaboss.start()  # start the task

    def cog_unload(self):
        """Unload the tasks"""
        if config.getHypixelOnline():
            self.online.cancel()  # cancel the task 
        if config.getMagmaboss():
            self.magmaboss.cancel()  # cancel the task

    @property
    def player_channel(self):
        """Get the player online channel"""
        return self.bot.get_channel(799291117425524756)

    @property
    def magma_boss_channel(self):
        """Get the magma boss channel"""
        return self.bot.get_channel(799220589243007007)

    @commands.command(name="add_hypixel_player")
    @commands.is_owner()
    async def add_hypixel_player(self, ctx, playername):
        """Add a player to the hypixel online task
        by typing the command with the player's username"""
        user = User(playername)
        data = self.jf.read()
        data[playername] = {"name": playername, "uuid": user.get_uuid(), "status": False}
        infoEmbed = discord.Embed(description=f"Added {playername} to the database", colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name=playername, value=user.get_uuid())
        await ctx.send(embed=infoEmbed)
        self.jf.write(data)

    @commands.command(name="remove_hypixel_player")
    @commands.is_owner()
    async def remove_hypixel_player(self, ctx, playername):
        """Add a player to the hypixel online task
        by typing the command with the player's username"""
        user = User(playername)
        data = dict(self.jf.read())
        del(data[playername])
        infoEmbed = discord.Embed(description=f"Removed {playername} from the database", colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name=playername, value=user.get_uuid())
        await ctx.send(embed=infoEmbed)
        self.jf.write(data)

    @tasks.loop(seconds=20.0)
    async def online(self):
        """Announce when players join or leave the hypixel network"""
        channel = self.player_channel
        
        if not channel:
            return
        try:
            async with aiohttp.ClientSession() as session:
                self.jf = JsonFile("players.json", f"{path}")
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
                        infoEmbed = discord.Embed(title="Online", description=f"{playername} is now in {game}  online",
                                                  color=config.getDiscordColour("blue"), timestamp=datetime.now())
                        infoEmbed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")
                        infoEmbed.set_footer(text="mc.hypixel.net",
                                             icon_url="https://de.wsikipedia.org/wiki/Hypixel#/media/Datei:LogoHypixel.png")
                        await channel.send(embed=infoEmbed)

                    elif not online and status:
                        lg.info(f"{playername} is now in offline")
                        infoEmbed = discord.Embed(title="Offline", description=f"{playername} is in now offline",
                                                  color=config.getDiscordColour("blue"), timestamp=datetime.now())
                        infoEmbed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}")
                        infoEmbed.set_footer(text="mc.hypixel.net",
                                             icon_url="https://de.wikipedia.org/wiki/Hypixel#/media/Datei:LogoHypixel.png")
                        await channel.send(embed=infoEmbed)

                    jf_data[player]["status"] = online
                    self.jf.write(jf_data)

        except Exception as e:
            lg.info(e)
            pass

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
                                          description=f"The magma boss spawns in {value} hours",
                                          colour=config.getDiscordColour("blue"),
                                          timestamp=datetime.now())
                if value <= 0.1:
                    try:
                        await channel.send(embed=infoEmbed)

                    except AttributeError:
                        self.magmaboss

    @commands.command(name="bazaar", aliases=["bz"])
    @commands.has_role(config.getBotAccessRole())
    async def bazaar(self, ctx, *args):
        """Get the last prices for an item in the Hypixel SkyBlock bazaar"""
        if not args:
            infoEmbed = discord.Embed(title="Bazaar Help",
                                      description="Please write the english name of the item next to the command. ")
        item = args[0].upper()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.hypixel.net/skyblock/bazaar?key={key}&productId={item}") as data:
                    content = json.loads(await data.text())
                    jf = JsonFile("bazaar.json", path=f"{path}\hypixel")
                    jf.write(content)
                    if not item in content["products"]:
                        errorEmbed = discord.Embed(title="Bazaar Error",
                                                   description=f"ItemNotFound: {item} is not a supported item",
                                                   colour=config.getDiscordColour("red"))
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

        except:
            errorEmbed = discord.Embed(title="Bazaar Error",
                                       description="There was an error while connecting to the Hypixel API",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)

    #TODO: Add auctions

    @commands.command(name="fairy_souls")
    @commands.has_role(config.getBotAccessRole())
    async def fairy_souls(self, ctx, playername):
        """Get the collected fairy souls of a player"""
        #FIXME
        pl = Player(playername)
        skyblock = pl.SkyBlock(pl.data, pl.name, pl.uuid)
        infoEmbed = discord.Embed(title="Fairy Souls",
                                  description=f"Showing collected fairy souls for user {playername}", colour=config.getDiscordColour("blue"))
        for profile in list(skyblock.profiles.keys()):
            infoEmbed.add_field(name=profile, value=f"{skyblock.profiles[profile].fairy_souls_collected} of 220")

        await ctx.send(embed=infoEmbed)


def setup(bot):
    bot.add_cog(HypixelAPI_Handler(bot))

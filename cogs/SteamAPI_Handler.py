import logging
import discord
from discord.ext import commands, tasks
from clicks_util.json_util import JsonFile
from util.logger import path
from util.steam.user import User
import urllib.request
import json
import sys
import asyncio
from datetime import datetime
from util import config


lg = logging.getLogger(__name__[5:])


def translate_state_code(state: int):
    if state > 3:
        return "Unknown Code"

    if state == 1:
        return "online"

    elif state == 2:
        return "busy"

    elif state == 3:
        return "away"


class SteamAPI_Handler(commands.Cog):
    """A handler for the steam api, I get the key from config.getSteamKey()
    if you want a key for yourself log in on this official steam website
    https://steamcommunity.com/dev/apikey
    """
    def __init__(self, bot):

        self.bot = bot
        self.online.start()

    def cog_unload(self):
        self.online.cancel()

    @property
    def player_channel(self):
        """Get the player online channel"""
        return self.bot.get_channel(799291117425524756)

    @property
    def jf(self):
        return JsonFile(name="users.json", path=f"{path}/steam")

    @commands.command(name="add_steam_player")
    @commands.is_owner()
    async def add_steam_player(self, ctx, steam_id):
        """Add a player to the steam online task
        by typing the command with the player's steam id"""
        user = User(steam_id)
        data = self.jf.read()
        user = User(steam_id)
        data[user.name] = {"name": user.name, "steam_id": user.steam_id, "status": False}
        self.jf.write(data)

        infoEmbed = discord.Embed(title="Add Steam Player",
                                  description="Added player to the list of watched steam profiles",
                                  colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name="Name", value=user.name, inline=False)
        infoEmbed.add_field(name="Steam ID", value=str(user.steam_id))
        infoEmbed.add_field(name="State", value=translate_state_code(int(user.state)))
        infoEmbed.set_thumbnail(url=user.avatar)

        await ctx.send(embed=infoEmbed)

    @tasks.loop(seconds=20)
    async def online(self):
        channel = self.player_channel
        if not channel:
            await asyncio.sleep(5)
            channel = self.player_channel

        jf_data = self.jf.read()
        for user in jf_data.keys():
            user = User(self.jf.read()[user]["steam_id"])
            status = self.jf.read()[user.name]["status"]
            state = user.state
            if status == 0 and state == 1 or status == False and state == 2 or state == 3 and status == False:
                lg.info(f"{user.name} is now online - status code: {state}")
                infoEmbed = discord.Embed(title="Online", description=f"{user.name} is now in Steam  "
                                                                      f"{translate_state_code(user.state)}",
                                          color=config.getDiscordColour("blue"), timestamp=datetime.now())
                infoEmbed.set_thumbnail(url=user.avatar)
                await channel.send(embed=infoEmbed)

            elif state == 0 and status == 1:
                lg.info(f"{user.name} is now offline")
                infoEmbed = discord.Embed(title="Online", description=f"{user.name} is in Steam now offline",
                                          color=config.getDiscordColour("blue"), timestamp=datetime.now())
                await channel.send(embed=infoEmbed)

            jf_data[user.name]["status"] = state
            self.jf.write(jf_data)


def setup(bot):

    bot.add_cog(SteamAPI_Handler(bot))

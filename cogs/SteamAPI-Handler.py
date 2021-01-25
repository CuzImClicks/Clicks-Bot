import logging
import discord
from discord.ext import commands
from util.logger import path
import logging

lg = logging.getLogger(__name__)


class SteamAPI_Handler(commands.Cog):
    """A handler for the steam api, I get the key from config.getSteamKey()
    if you want a key for yourself log in on this official steam website
    https://steamcommunity.com/dev/apikey
    """
    def __init__(self, bot):

        self.bot = bot


def setup(bot):

    bot.add_cog(SteamAPI_Handler(bot))

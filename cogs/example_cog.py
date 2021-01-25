import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class example_cog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


def setup(bot):

    bot.add_cog(example_cog(bot))
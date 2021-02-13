import clicks_util
import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime
from clicks_util.timeconvert import TimeZone

lg = logging.getLogger(__name__[5:])


class TimeConvert(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="get_otto_time")
    @commands.has_role(config.getBotAdminRole())
    async def get_otto_time(self, ctx):
        tz = TimeZone("USA/Los_Angeles")
        infoEmbed = discord.Embed(description=f"Ottomated lives in PST, it's {tz.getTime()}")
        await ctx.send(embed=infoEmbed)


def setup(bot):

    bot.add_cog(TimeConvert(bot))

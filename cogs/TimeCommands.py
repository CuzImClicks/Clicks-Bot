import clicks_util
import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime
from clicks_util.timeconvert import TimeZone
from pytz import common_timezones_set

lg = logging.getLogger(__name__[5:])


class TimeConvert(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="get_otto_time", hidden=True)
    @commands.is_owner()
    async def get_otto_time(self, ctx):
        tz = TimeZone("America/Los_Angeles")
        lg.info(tz.time.time())
        infoEmbed = discord.Embed(description=f"Ottomated lives in PST, it's {tz.getTime()}")
        await ctx.send(embed=infoEmbed)

    @commands.command(name="getTime")
    async def get_time(self, ctx, timezone: str = "Europe/Berlin"):
        if not timezone in common_timezones_set:
            errorEmbed = discord.Embed(description="Not a valid timezone", colour=config.getDiscordColour("red"))
            await ctx.send(embed=errorEmbed)
            return
        tz = TimeZone(timezone)
        infoEmbed = discord.Embed(description=f"Time for timezone '{timezone}' is {tz.getTime()}")
        await ctx.send(embed=infoEmbed)

def setup(bot):

    bot.add_cog(TimeConvert(bot))

import logging
from attr import __title__
import discord
from discord.ext import commands

import ClicksBot
from util.logger import path
import logging
from util import config
import datetime
import aiohttp
from aiohttp import ClientSession
import json


lg = logging.getLogger(__name__[5:])
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class PiHoleAPI_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="get_pihole_summary", hidden=True)
    @commands.is_owner()
    async def get_pihole_summary(self, ctx):
        async with ClientSession() as session:
            async with session.get(url=f"http://{config.getPiHoleIp()}/admin/api.php?summary") as data:
                content = json.loads(await data.text())
                infoEmbed = discord.Embed(title="Pi Hole Summary", colour=config.getDiscordColour("blue"))
                infoEmbed.add_field(name="Blocked domains", value=content["domains_being_blocked"], inline=False)
                infoEmbed.add_field(name="DNS queries today", value=content["dns_queries_today"], inline=False)
                infoEmbed.add_field(name="Blocked ads today", value=content["ads_blocked_today"], inline=False)
                infoEmbed.add_field(name="Ads blocked today", value=content["ads_blocked_today"], inline=False)
                await ctx.send(embed=infoEmbed)

        

def setup(bot):

    bot.add_cog(PiHoleAPI_Handler(bot))

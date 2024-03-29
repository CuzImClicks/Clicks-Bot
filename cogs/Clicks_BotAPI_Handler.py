import logging
import discord
from discord.ext import commands

import ClicksBot
from util.logger import path
import logging
from util import config
import datetime
from web_server.database import create_key, get_key
from clicks_util import timeconvert


lg = logging.getLogger(__name__[5:])
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class Clicks_BotAPI_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="create_api_key")
    @commands.is_owner()
    async def create_api_key(self, ctx):
        user = ctx.message.mentions[0]
        username = user.name

        key = create_key(username)
        infoEmbed = discord.Embed(title="API Key",
                                  description=f"A API key has been generated and saved to the database",
                                  colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name="Key", value=key, inline=False)
        infoEmbed.add_field(name="Requested by", value=ctx.author.name)
        infoEmbed.set_author(name=username, icon_url=user.avatar_url)
        infoEmbed.set_footer(text=timeconvert.getTime())

        await ctx.send(embed=infoEmbed)

    @commands.command(name="get_api_key")
    @commands.is_owner()
    async def get_api_key(self, ctx):
        user = ctx.message.mentions[0]
        username = user.name
        key = get_key(username)
        infoEmbed = discord.Embed(title="API Key",
                                  description=f"Read the API key for {username} from the database",
                                  colour=config.getDiscordColour("green")) 
        infoEmbed.add_field(name="Key", value=key, inline=False)
        infoEmbed.add_field(name="Requested by", value=ctx.author.name)
        infoEmbed.set_author(name=username, icon_url=user.avatar_url)
        infoEmbed.set_footer(text=timeconvert.getStrDateAndTime())

        await ctx.send(embed=infoEmbed)


def setup(bot):

    bot.add_cog(Clicks_BotAPI_Handler(bot))

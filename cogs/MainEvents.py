import logging
import discord
from discord.ext import commands
from util import config

lg = logging.getLogger(__name__)


class MainEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        for guild in self.bot.guilds:

            if guild.name == "GUILD":
                break

            # print(
            # f'{client.user} is connected to the following guild:\n'
            # f'{guild.name}(id: {guild.id})'
            # )

            lg.info(
                f'{self.bot.user} is connected to the following guild:\n'
                f'{guild.name})'
            )

        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=config.getStatus()))

    @commands.Cog.listener()
    async def on_member_join(self, member):

        lg.info(member)

        # await member.create_dm()
        # await member.send("Wilkommen")


def setup(bot):

    bot.add_cog(MainEvents(bot))
import discord
from discord.ext import commands

from util import config
from util.logger import *

import logging
import os

lg = logging.getLogger(__name__)
lg_chat = logging.getLogger("CHAT")
#TODO: revert path
#path = os.getcwd()
path = "D:/GitHub Repos/Clicks-Bot"




class MessageEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author == self.bot.user:
            return

        elif config.getCommandPrefix() in message.content:
            return

        else:

            await message.channel.send("Deine Nachricht wurde gelöscht!", delete_after=5)
            lg.info(f"Deleted '{message.content}' from {message.channel} by {message.author.name}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if config.getCommandPrefix() in before.content:
            return

        elif before.author == self.bot.user:
            return

        else:
            await before.channel.send("Deine Nachricht wurde editiert!", delete_after=5)
            lg.info(f"Edited '{before.content}' to '{after.content} from {before.channel} by {before.author.nick}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):

        await log_typing(channel, user, when)



def setup(bot):

    bot.add_cog(MessageEvents(bot))

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
from util.logger import path
import logging
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class MessageEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if message.author.bot:
            return

        if config.getCommandPrefix() in message.content:
            return

        else:

            await message.channel.send("Deine Nachricht wurde gelöscht!", delete_after=5)
            lg.info(f"Deleted '{message.content}' from {message.channel} by {message.author.name}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if config.getCommandPrefix() in before.content:
            return

        if self.before.author.bot or self.after.author.bot:
            return

        else:
            await before.channel.send("Deine Nachricht wurde editiert!", delete_after=5)
            lg.info(f"Edited '{before.content}' to '{after.content} from {before.channel} by {before.author.nick}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):

        await log_typing(channel, user, when)


def setup(bot):

    bot.add_cog(MessageEvents(bot))

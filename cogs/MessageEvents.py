import discord
from discord.ext import commands

from util import config
from util.logger import *
from util.logger import path
import logging
import os

lg = logging.getLogger(__name__[5:])


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
            lg.info(f"Deleted '{message.content}' from {message.channel} by {message.author.name}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if config.getCommandPrefix() in before.content:
            return

        if before.author.bot or after.author.bot:
            return

        else:
            await before.channel.send("Deine Nachricht wurde editiert!", delete_after=5)
            lg.info(f"Edited '{before.content}' to '{after.content} from {before.channel} by {before.author.nick}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):

        lg.info(f"[{str(user)}] is typing in {str(channel)} since {when}")


def setup(bot):

    bot.add_cog(MessageEvents(bot))

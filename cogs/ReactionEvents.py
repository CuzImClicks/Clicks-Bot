import logging
import discord
from discord.ext import commands
from util.logger import *
from util.logger import path

lg = logging.getLogger(__name__)
from util.logger import path
import logging
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class ReactionEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        msg_id = "703236904551972905"

        if str(payload.message_id) == msg_id:

            role2 = payload.member.guild.roles[12]
            await payload.member.add_roles(role2)
            await log_role(payload, role2)

            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id)
            emoji = payload.emoji
            lg.info("Got emoji")
            await message.remove_reaction(emoji, user)

        else:
            pass

        await log_reaction(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        await log_reaction_remove(payload)


def setup(bot):

    bot.add_cog(ReactionEvents(bot))
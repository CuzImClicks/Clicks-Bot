import logging
import discord
from discord.ext import commands

import ClicksBot
from util.logger import *
from util.logger import path

from clicks_util import info

lg = logging.getLogger(__name__)
from util.logger import path
import logging
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class ReactionEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #if the message id is the rules message id
        msg_id = "703236904551972905"
        
        if str(payload.message_id) == msg_id:

            role2 = payload.member.guild.roles[12]
            await payload.member.add_roles(role2)
            await log_role(payload, role2)

            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id)
            emoji = payload.emoji
            await message.remove_reaction(emoji, user)
            return

        elif str(payload.message_id) == "819259300852662282":

            roles = payload.member.guild.roles
            role = discord.utils.get(roles, name="Mitglied")
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = payload.member
            emoji = payload.emoji
            
            await user.add_roles(role)
            await message.remove_reaction(emoji, user)
            return

        await log_reaction(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        await log_reaction_remove(payload)


def setup(bot):

    bot.add_cog(ReactionEvents(bot))

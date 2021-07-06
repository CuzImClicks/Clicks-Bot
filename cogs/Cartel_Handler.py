import logging
import time

import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime

lg = logging.getLogger(__name__[5:])

vorraum_id = 862061998966702110
council_id = 862043176294547497
white_check_mark = "✅"
x = "❌"

permission_messages = []
permitted = []


def get_Salutation(member_name: str):
    if member_name == "Big-Chungus":
        return "Don"

    elif member_name == "DasVakuum":
        return "Right Honorable Gentleman DasVakuum"

    elif member_name == "alex_":
        return "Your highness"

    elif member_name == "matildabrodehl":
        return ""

    elif member_name == "Cuz_Im_Clicks":  # FIXME: not giving back the right name
        return "Sir Clicks of Discord"


class Cartel_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):

        if not after.channel:
            return

        if member.bot:
            return

        if after.channel.id == vorraum_id:
            # lg.info("A stranger enters the lobby. You don't know him, but he seems to know what he is doing. You ask "
            #        "him how you can help him. He replies that he is here for an appointment with the "
            #        "council.")

            await member.create_dm()
            await member.dm_channel.send("You enter the room, its old and classy, only a few people are present. But "
                                         "you can hear a slight mumbling noise from the different conversations. You "
                                         "don't know what to do, should you sit and wait for the waiter to come or "
                                         "should you directly approach him? You decide to talk to him. After a few "
                                         "steps you stand at the counter and get a small note out of your pocket."
                                         "The waiter takes a look at it and compares something in the calendar.")
            # TODO: maybe music bot that play some piano music.
            council = self.bot.get_channel(council_id)
            if not council:
                return

            if len(council.members) == 0:
                await member.dm_channel.send("""I'm sorry, he says. But currently there are no members of the council 
                awaiting you. You may wait in here for one of them to return. In the mean time, have a look around or 
                read a newspaper.""")
                return

            else:
                council_member = council.members[0]  # in the order they are in the channel
                await council_member.create_dm()
                message = await council_member.dm_channel.send(f"'{get_Salutation(council_member.display_name)}?' the "
                                                               f"waiter asks, {member.display_name} "
                                                               f"is asking to join the meeting of the council. Shall "
                                                               f"I lead them "
                                                               f"in?")
                await message.add_reaction(white_check_mark)
                await message.add_reaction(x)

                msg = PermissionMessage(message, member)
                permission_messages.append(msg)

        elif after.channel.id == council_id and not before.channel.id == vorraum_id and not before.channel.id == council_id and member not in self.permitted:
            await member.create_dm()
            # FIXME: bot sends many messages
            vorraum = self.bot.get_channel(vorraum_id)
            if not vorraum:
                return
            if member.top_role.name == "Administrator":
                await member.dm_channel.send("Mind your manners?")
                await member.move_to(vorraum)
                return

            await member.dm_channel.send("Oh I'm sorry, could I have an id please? Its just that security is very "
                                         "important")

            await member.move_to(vorraum)

        # TODO: When a member of the council joins the "Council" channel, there should be another message sent to them to move the person waiting
        # TODO: Wenn Jan Paul da ist:

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        if not type(channel) == discord.DMChannel:
            return

        message = await channel.fetch_message(payload.message_id)
        perm_msg = PermissionMessage.get_reload_message(message)
        if not perm_msg:
            return
        user = self.bot.get_user(payload.user_id)
        if message in permission_messages and payload.emoji.name == white_check_mark and not user.bot:
            await perm_msg.target.create_dm()
            await perm_msg.target.dm_channel.send("The council members are ready to meet you. Please follow me, "
                                                  "we will arrive in a short time.")
            council = self.bot.get_channel(council_id)
            if not council:
                return
            time.sleep(5)
            await perm_msg.target.move_to(council)
            permitted.append(perm_msg.target)

        if message in permission_messages and payload.emoji.name == x and not user.bot:
            await perm_msg.target.create_dm()
            await perm_msg.target.dm_channel.send("I'm sorry to tell you but the council is not ready to receive you "
                                                  "at the moment. Please have a seat or leave if you wish.")


class PermissionMessage:
    message = discord.Message
    target = discord.Member

    def __init__(self, message: discord.Message, target: discord.Member):
        self.message = message
        self.target = target

    def __eq__(self, other):
        return self.message == other

    @classmethod
    def get_reload_message(cls, message: discord.Message):
        for msg in permission_messages:
            if message == msg.message:
                return msg


def setup(bot):
    bot.add_cog(Cartel_Handler(bot))

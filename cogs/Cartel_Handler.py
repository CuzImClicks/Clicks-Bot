import asyncio
import logging
import time

import discord
from discord.ext import commands

import ClicksBot
from cogs.MusicBot import YTDLSource, YouTubeVideo
from util.logger import path
import logging
from util import config
import datetime

lg = logging.getLogger(__name__[5:])
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)

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

    elif member_name == "Cuz_Im_Clicks":
        return "Sir Clicks of Discord"

    else:
        return member_name


def get_CouncilMember(channel: discord.VoiceChannel):
    for m in channel.members:
        for role in m.roles:
            if role.name == "Potato":
                return m


class Cartel_Handler(commands.Cog):

    users_in_vorraum = []

    def __init__(self, bot):

        self.bot = bot
        self.piano = YouTubeVideo(url="https://www.youtube.com/watch?v=kRawGw2HTmI")

    @commands.Cog.listener()
    async def on_ready(self):
        #await self.wait_for_end()
        pass

    async def wait_for_end(self):
        from discord.utils import get
        while True:
            guild = get(self.bot.guilds, name="RezURekted")
            if guild is None:
                return
            voice = guild.voice_client
            channel = self.bot.get_channel(vorraum_id)
            if not voice:
                voice = await channel.connect()
                lg.info(f"Connected to the Voice Channel: {channel.name}")

            player = await YTDLSource.from_url(str(self.piano.url), loop=self.bot.loop)
            error_msg = ""
            voice.play(player, after=lambda error: lg.info(error_msg.join(error)) if error else None)
            lg.info("Started playing the song")
            while voice.is_playing():
                await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):

        if not after.channel:
            return

        if member.bot:
            return

        try:
            if after.channel.id == vorraum_id and before.channel.id == council_id:
                await member.create_dm()
                await member.dm_channel.send(f"Ohh welcome back, you might just hang around here.")
                pass

            if before.channel.id == vorraum_id and after.channel.id == vorraum_id:
                return

        except AttributeError:
            pass

        if after.channel.id == vorraum_id and not before.channel.id == council_id:
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
            council = self.bot.get_channel(council_id)
            if not council:
                return

            council_member = get_CouncilMember(council)  # FIXME: doesnt work
            potato_role = discord.utils.get(member.guild.roles, name="Potato")
            lg.info(potato_role is None)
            lg.info(council_member is None)
            if potato_role in member.roles:
                await member.dm_channel.send(f"Welcome {get_Salutation(member.name)}, the waiter greets you, would "
                                             f"you like me to show you in")

            if len(council.members) == 0:
                await member.dm_channel.send("""I'm sorry, he says. But currently there are no members of the council 
                awaiting you. You may wait in here for one of them to return. In the mean time, have a look around or 
                read a newspaper.""")
                return

            else:
                # in the order they are in the channel

                if council_member is None:
                    await member.create_dm()
                    await member.dm_channel.send("Currently there is no person with the permission to get you into "
                                                 "the council room.")
                    return
                await council_member.create_dm()
                message = await council_member.dm_channel.send(f"'{get_Salutation(council_member.name)}?' the "
                                                               f"waiter asks, {member.display_name} "
                                                               f"is asking to join the meeting of the council. Shall "
                                                               f"I lead them in?")
                await message.add_reaction(white_check_mark)
                await message.add_reaction(x)

                msg = PermissionMessage(message, member)
                permission_messages.append(msg)

        elif after.channel.id == council_id and not before.channel.id == vorraum_id and not before.channel.id == council_id and member not in permitted:
            await member.create_dm()
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

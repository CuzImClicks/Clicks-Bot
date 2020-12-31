import logging
import discord
from discord.ext import commands
from discord.utils import get
from util import config
import datetime
from multiprocessing import Process, Lock
import os

path = os.getcwd()

lg = logging.getLogger(__name__)
lg_chat = logging.getLogger("CHAT")
fl_chat = logging.FileHandler(f"{path}/logs/chat.log")
fl_chat.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl_chat.setFormatter(fmt)

lg_chat.addHandler(fl_chat)

previous_message_id = ""


class MainEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.previous_message_id = ""

    @commands.Cog.listener()
    async def on_ready(self):
        
        total_users = 0
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
            total_users += len(guild.members)
        
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{total_users} Benutzer an"))

    @commands.Cog.listener()
    async def on_member_join(self, member):

        lg.info(f"{member} joined the {member.guild}")
        if member.guild == "RezURekted":
            await member.add_roles("Member")

            embed = discord.Embed(color=0x2b4f22, description=f"Ein wildes {member.name} erscheint!")
            embed.set_thumbnail(url=str(member.avatar_url))
            embed.set_footer(text=f"{member.guild} - {datetime.datetime.utcnow()}", icon_url=member.guild.icon_url)
            channel = self.bot.get_channel(get(member.guild.channels, "lobby"))

            await channel.send(embed=embed)

            await member.create_dm()

    @commands.Cog.listener()
    async def on_message(self, message):

        try:
            lg_chat.info(f"[{message.author}] in {message.channel} - {message.content}")

        except Exception as e:

            pass


def setup(bot):

    bot.add_cog(MainEvents(bot))

import logging
import discord
from discord.ext import commands
from util import config

path = "D:/GitHub Repos/Clicks-Bot"

lg = logging.getLogger(__name__)
lg_chat = logging.getLogger("CHAT")
fl_chat = logging.FileHandler(f"{path}\logs\chat.log")
fl_chat.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl_chat.setFormatter(fmt)

lg_chat.addHandler(fl_chat)


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

    @commands.Cog.listener()
    async def on_message(self, message):

        global previous_message_id

        if message.author == self.bot.user :
            pass

        else:
            if not str(previous_message_id) == str(message.id):
                await self.bot.process_commands(message)

        lg_chat.info(f"[{message.author}] in {message.channel} - {message.content}")


def setup(bot):

    bot.add_cog(MainEvents(bot))
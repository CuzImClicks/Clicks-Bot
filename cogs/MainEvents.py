import logging
import discord
from discord.ext import commands
from util import config
import datetime

path = "D:/GitHub Repos/Clicks-Bot"

lg = logging.getLogger(__name__)
lg_chat = logging.getLogger("CHAT")
fl_chat = logging.FileHandler(f"{path}\logs\chat.log")
fl_chat.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl_chat.setFormatter(fmt)

lg_chat.addHandler(fl_chat)

previous_message_id = ""


def getPreviousMessageID():
    return previous_message_id


def setPreviousMessageID(message_id):
    global previous_message_id
    previous_message_id = str(message_id)
    lg.info(f"Set Message ID to: {message_id}")


class MainEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.previous_message_id = ""

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

        lg.info(f"{member} joined the {member.guild}")
        await member.add_roles("Member")

        embed = discord.Embed(colour=1e6170, description=f"Ein wildes {member.name} erscheint!")
        embed.set_thumbnail(url=str(member.avatar_url))
        embed.setfoorter(text=str(member.guild), icon_url=str(member.guild.icon_url))
        embed.set_timestamp(datetime.datetime.utcnow())

        channel = self.bot.get_channel(764117625331908649)

        await channel.send(embed=embed)



        # await member.create_dm()
        # await member.send("Wilkommen")

'''    @commands.Cog.listener()
    async def on_message(self, message):

        lg_chat.info(f"[{message.author}] in {message.channel} - {message.content}")

        if message.author == self.bot.user:
            pass

        elif not getPreviousMessageID() == message.id:

            lg.info(f"Previous Message ID: {getPreviousMessageID()}")
            lg.info(f"Current Message ID: {message.id}")
            setPreviousMessageID(message.id)
            await self.bot.process_commands(message)
'''


def setup(bot):

    bot.add_cog(MainEvents(bot))

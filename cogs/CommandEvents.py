import time
import discord
from discord.ext import commands
import logging
from util import logger
from util.logger import path
from datetime import datetime
from util import config
import colorama

lg = logging.getLogger(__name__[5:])
import logging
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)

class CommandEvents(commands.Cog):
    '''
    instead of using @bot.event use @bot.Cog.listener()
    '''

    def __init__(self, client):

        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        time_now = datetime.now()
        if isinstance(error, commands.errors.CheckFailure):

            error_msg = "Du hast nicht genügend Rechte für diesen Befehl!"
            errorEmbed = discord.Embed(title="Command Error", description=error_msg, colour=config.getDiscordColour("red"))
            errorEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=errorEmbed)
            lg.error(colorama.Fore.RED+error_msg)

        elif isinstance(error, commands.errors.CommandNotFound):
                cmdnfEmbed = discord.Embed(title="Command Error", description="Command not found", colour=config.getDiscordColour("red"))
                cmdnfEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=cmdnfEmbed)
                lg.info(colorama.Fore.RED+str(error))

        else:
            errorEmbed = discord.Embed(title="Command Error", description= str(error),colour=config.getDiscordColour("red"))
            errorEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=errorEmbed)
            lg.error(colorama.Fore.RED+str(error))
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):

        lg.info(f"Command complete")


def setup(bot):

    bot.add_cog(CommandEvents(bot))

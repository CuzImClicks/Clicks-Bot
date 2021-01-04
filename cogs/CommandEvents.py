import time
import discord
from discord.ext import commands
import logging
from util import logger
from util.logger import path
from datetime import datetime

lg = logging.getLogger(__name__)
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

    '''    async def delete_cmd(self, ctx):

        time.sleep(5)
        await ctx.message.delete()'''

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        time_now = datetime.now()
        if isinstance(error, commands.errors.CheckFailure):

            error_msg = "Du hast nicht genügend Rechte für diesen Befehl!"
            errorEmbed = discord.Embed(title="Command Error", color = discord.Colour(0x9D1309), timestamp=time_now)
            errorEmbed.add_field(name="Error Message", value=error_msg)
            errorEmbed.add_field(name="Raised by", value=ctx.author.name)
            await ctx.send(embed=errorEmbed)
            await logger.log_error(error_msg)

        elif isinstance(error, commands.errors.CommandNotFound):
                cmdnfEmbed = discord.Embed(title="Command Error", color= discord.Colour(0x9D1309), timestamp=time_now)
                cmdnfEmbed.add_field(name="Error Message", value=f"Command not found")
                cmdnfEmbed.add_field(name="Raised by", value=ctx.author.name)
                await ctx.send(embed=cmdnfEmbed)
        else:
            lg.error(error)
            errorEmbed = discord.Embed(title="Command Error", color=discord.Colour(0x9D1309), timestamp=time_now)
            errorEmbed.add_field(name="Error Message", value=str(error))
            errorEmbed.add_field(name="Raised by", value=ctx.author.name)
            await ctx.send(embed=errorEmbed)
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):

        lg.info(f"Command complete")


def setup(bot):

    bot.add_cog(CommandEvents(bot))

import time
import discord
from discord.ext import commands
import logging
from util import logger

lg = logging.getLogger(__name__)


class CommandEvents(commands.Cog):
    '''
    instead of using @bot.event use @bot.Cog.listener()
    '''

    def __init__(self, client):

        self.bot = client

    async def delete_cmd(self, ctx):

        time.sleep(5)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.errors.CheckFailure):

            error_msg = "Du hast nicht genügend Rechte für diesen Befehl!"

            await ctx.send(error_msg, delete_after=5)
            await logger.log_error(error_msg)

        else:
            await logger.log_error(error)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            await self.delete_cmd(ctx)
            lg.info(f"Command complete")
        except discord.errors.NotFound as e:
            pass


def setup(bot):

    bot.add_cog(CommandEvents(bot))

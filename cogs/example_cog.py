import logging

from discord.ext import commands

lg = logging.getLogger(__name__[5:])


class example_cog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


def setup(bot):

    bot.add_cog(example_cog(bot))

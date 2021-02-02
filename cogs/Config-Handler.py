from util import config
import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime
from clicks_util import timeconvert

lg = logging.getLogger(__name__[5:])


class Config_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="enable")
    @commands.has_role(config.getBotAdminRole())
    async def enable_command(self, ctx, feature):
        if not config.enable(feature):
            return
        infoEmbed = discord.Embed(title="Enable",
        description=f"Enabled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="disable")
    @commands.has_role(config.getBotAdminRole())
    async def disable_command(self, ctx, feature):
        if not config.disable(feature):
            return
        infoEmbed = discord.Embed(title="Disable",
        description=f"Disabled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="toggle")
    @commands.has_role(config.getBotAdminRole())
    async def toggle_command(self, ctx, feature):
        if not config.toggle(feature):
            return
        infoEmbed = discord.Embed(title="Toggle",
        description=f"Toggled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)




def setup(bot):

    bot.add_cog(Config_Handler(bot))

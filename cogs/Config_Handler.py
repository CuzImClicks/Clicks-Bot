import ClicksBot
from clicks_util.json_util import JsonFile
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
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)

jf_blocked_channels = JsonFile("blocked_channels.json", path)


class Config_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="enable")
    @commands.is_owner()
    async def enable_command(self, ctx, feature):
        if not config.enable(feature):
            errorEmbed = discord.Embed(description=f"{feature} is not a changeable feature in the config file", colour=config.getDiscordColour("red"))
            await ctx.send(embed=errorEmbed)
            return
        infoEmbed = discord.Embed(title="Enable",
        description=f"Enabled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="disable")
    @commands.is_owner()
    async def disable_command(self, ctx, feature):
        if not config.disable(feature):
            errorEmbed = discord.Embed(description=f"{feature} is not a changeable feature in the config file", colour=config.getDiscordColour("red"))
            await ctx.send(embed=errorEmbed)
            return
        infoEmbed = discord.Embed(title="Disable",
        description=f"Disabled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="toggle")
    @commands.is_owner()
    async def toggle_command(self, ctx, feature):
        if not config.toggle(feature):
            errorEmbed = discord.Embed(description=f"{feature} is not a changeable feature in the config file", colour=config.getDiscordColour("red"))
            await ctx.send(embed=errorEmbed)
            return
        infoEmbed = discord.Embed(title="Toggle",
        description=f"Toggled the feature {feature} and wrote the changes to the config file",
        colour=config.getDiscordColour("green"))
        infoEmbed.set_footer(text=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="add_blocked_channel")
    @commands.is_owner()
    async def add_blocked_channel(self, ctx):
        channel_id = ctx.channel.id
        blocked_channels = jf_blocked_channels.read()
        blocked_channels.append(channel_id)
        jf_blocked_channels.write(blocked_channels)

    @commands.command(name="remove_blocked_channel")
    @commands.is_owner()
    async def remove_blocked_channel(self, ctx, channel_id):
        channel_id = int(channel_id)
        blocked_channels = list(jf_blocked_channels.read())
        lg.info(blocked_channels)
        try:
            blocked_channels.remove(channel_id)
            jf_blocked_channels.write(blocked_channels)
            infoEmbed = discord.Embed(description=f"The channel id '{channel_id}' has been removed from the list of blocked channels. Note that the channel will only be unblocked after the next restart of the bot")
            await ctx.send(embed=infoEmbed)
        except ValueError as e:
            errorEmbed = discord.Embed(description=f"The channel id {channel_id}' is not in the list of blocked channels")
            await ctx.send(embed=errorEmbed)



def setup(bot):

    bot.add_cog(Config_Handler(bot))

import logging
import discord
from discord.ext import commands
from util import MessageHandler

from util import config
from util.logger import *
from util import embed
import logging
from discord import Color
import os
from datetime import datetime
from clicks_util import timeconvert

path = os.getcwd()

lg = logging.getLogger(__name__[5:])


class Commands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="github")
    @commands.has_role(config.getBotAccessRole())
    async def github(self, ctx):
        #await ctx.send("Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", delete_after=5)
        gitEmbed = discord.Embed(title="GitHub", description= "Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", color=config.getDiscordColour("blue"))
        await ctx.send(embed=gitEmbed)

    @commands.command(name="ping")
    @commands.has_role(config.getBotAccessRole())
    async def ping(self, ctx):
        pingEmbed = discord.Embed(title="Bot Latency", description=f"Pong! Dein Ping ist {round(self.bot.latency, 2) * 1000}ms", color=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())

        await ctx.send(embed=pingEmbed)

    @commands.command(name="count", help="Zählt hoch bis zu der eingegebenen Zahl")
    @commands.is_owner()
    async def count(self, ctx, target):

        target = int(target)
        x = 0

        while x != target:

            x += 1
            await ctx.send(x)

    @commands.command(name="setup", hidden=True)
    async def setup(self, ctx):

        guild = ctx.guild
        await ctx.send(embed=discord.Embed(title="Server Setup", description="Setting up the server roles", color=config.getDiscordColour("blue"), timestamp=timeconvert.getTime()))
        await guild.create_role(name="Bot Access", color=Color.orange())
        await guild.create_role(name="Dev", color=Color.purple())
        await guild.create_role(name="Bot Admin Access", color=Color.dark_red())

        for role in ctx.guild.roles:

            if role.name == "Clicks Bot":

                bot_role = int(role.position)
                lg.info(f"{bot_role} | {type(bot_role)}")
                break

    @commands.command(name="delete_roles")
    @commands.has_role(config.getBotAdminRole())
    async def delete_roles(self, ctx):
        '''Delete double roles created by the bot
        This is a command created for testing purposes
        '''
        try:
            for role in ctx.guild.roles:

                if role.name == "Dev":

                    await role.delete()

                elif role.name == "Bot Access":

                    await role.delete()

                elif role.name == "Bot Admin Access":

                    await role.delete()

        except discord.errors.Forbidden:

            pass

    @commands.command(name="shout", hidden=True)
    @commands.is_owner()
    async def shout(self, ctx, *args):
        if not args:
            errorEmbed = discord.Embed(title="Shout Error", description="Missing text", colour=discord.Colour(0x9D1309))
            await ctx.send(embed=errorEmbed)
            return

        string = ""
        args = list(args)
        for word in args:
            lg.info(word)
            string = f"{string} {word}"

        await ctx.send(string)


def setup(bot):

    bot.add_cog(Commands(bot))

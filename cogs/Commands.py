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

path = os.getcwd()

lg = logging.getLogger(__name__[5:])

fl = logging.FileHandler(f"{path}/logs/log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class Commands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="github")
    @commands.has_role(config.getDefaultRole())
    async def github(self, ctx):
        #await ctx.send("Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", delete_after=5)
        gitEmbed = discord.Embed(title="GitHub", description= "Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", color=discord.Colour(0x000030))
        await ctx.send(embed=gitEmbed)

    @commands.command(name="ping")
    @commands.has_role(config.getBotAccessRole())
    async def ping(self, ctx):
        pingEmbed = discord.Embed(title="Bot Latency", description=f"Pong! Dein Ping ist {round(self.bot.latency, 2) * 1000}ms", color=discord.Colour(0x000030), timestamp=datetime.now())

        await ctx.send(embed=pingEmbed)

    @commands.command(name="credits", help="Gibt dir eine Übersicht von wem der Bot erstellt und geschrieben wurde.")
    @commands.has_role(config.getBotAccessRole())
    async def credits(self, ctx):

        await embed.send_embed(ctx=ctx, infos=("Credits", "Credits to the ones who deserve", 0x2b4f22),
                               names=("Idee und Coding", "Textgestaltung", "Server Owner"), values=(
            "Henrik | Clicks", "Kai | K_Stein",
            "Luis | DasVakuum"), inline=(False, False, False))

    @commands.command(name="count", help="Zählt hoch bis zu der eingegebenen Zahl")
    async def count(self, ctx, target):

        target = int(target)
        x = 0

        while x != target:

            x += 1
            await ctx.send(x)

    @commands.command(name="setup")
    async def setup(self, ctx):

        guild = ctx.guild
        await ctx.send(embed=discord.Embed(title="Server Setup", description="Setting up the server roles", color=discord.Colour(0x000030), timestamp=datetime.now()))
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

    @commands.command(name="shout")
    @commands.has_role(config.getBotAdminRole())
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

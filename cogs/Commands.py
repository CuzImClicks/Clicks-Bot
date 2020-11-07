import logging
import discord
from discord.ext import commands

from util.logger import *
from util import embed

lg = logging.getLogger(__name__)


class Commands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="github")
    @commands.has_role("Member")
    async def github(self, ctx):
        await ctx.send("Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot")

    @commands.command(name="ping")
    @commands.has_role("Bot Access")
    async def ping(self, ctx):
        msg = f"Pong! Dein Ping ist {round(self.bot.latency, 2) * 1000}ms"

        await ctx.send(msg, delete_after=5)
        await log_send(ctx, msg)

    @commands.command(name="credits", help="Gibt dir eine Übersicht von wem der Bot erstellt und geschrieben wurde.")
    @commands.has_role("Bot Access")
    async def credits(self, ctx):
        # await ctx.send(strings.get_credits())
        # await logger.log_send(ctx, strings.get_credits())

        await embed.send_embed(bot=self.bot, ctx=ctx, infos=("Credits", "Credits to the ones who deserve", 0x2b4f22),
                               names=("Idee und Coding", "Textgestaltung", "Server Owner"), values=(
            "Idee und coding: Henrik | Clicks", "Textgestaltung : Kai | K_Stein",
            "Bereitstellung des Servers : Luis | DasVakuum"), inline=(False, False, False))

    @commands.command(name="command_message")
    @commands.has_role("Dev")
    async def command_mesage(self, ctx):
        pass


def setup(bot):

    bot.add_cog(Commands(bot))
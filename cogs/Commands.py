import logging
import discord
from discord.ext import commands
from util import MessageHandler

from util import config
from util.logger import *
from util import embed

lg = logging.getLogger(__name__)


class Commands(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="github")
    @commands.has_role(config.getDefaultRole())
    async def github(self, ctx):
        #await ctx.send("Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", delete_after=5)
        await MessageHandler.send(ctx, title="GitHub", description= "Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot", content="github")
        await log_send(ctx, "Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot")

    @commands.command(name="ping")
    @commands.has_role(config.getBotAccessRole())
    async def ping(self, ctx):
        msg = f"Pong! Dein Ping ist {round(self.bot.latency, 2) * 1000}ms"

        await ctx.send(msg, delete_after=5)
        await log_send(ctx, msg)

    @commands.command(name="credits", help="Gibt dir eine Übersicht von wem der Bot erstellt und geschrieben wurde.")
    @commands.has_role(config.getBotAccessRole())
    async def credits(self, ctx):

        await embed.send_embed(ctx=ctx, infos=("Credits", "Credits to the ones who deserve", 0x2b4f22),
                               names=("Idee und Coding", "Textgestaltung", "Server Owner"), values=(
            "Henrik | Clicks", "Kai | K_Stein",
            "Luis | DasVakuum"), inline=(False, False, False))


def setup(bot):

    bot.add_cog(Commands(bot))

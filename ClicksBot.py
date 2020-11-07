import discord
import logging
from util import logger, config
from discord.ext import commands

from util.logger import *

import os

path = os.getcwd()
#config.getLoggingLevel()
logging.basicConfig(level=config.getLoggingLevel(), format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)

fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")


fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(config.getFileLoggingLevel())
fl.setFormatter(fmt)

lg.addHandler(fl)

intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)


@bot.command()
async def load(ctx, extension):

    bot.load_extension(f"cogs.{extension}")


@bot.command()
async def unload(ctx, extension):

    bot.unload_extension(f"cogs.{extension}")


try:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if not filename == "example_cog.py":
                bot.load_extension(f"cogs.{filename[:-3]}")

        else:
            pass

    bot.run(config.getToken())

except KeyboardInterrupt as e:

    pass

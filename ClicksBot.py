import discord
import logging
from util import logger, config
from discord.ext import commands
from util.logger import *
import os

#TODO: revert path
#path = os.getcwd()
path = "D:/GitHub Repos/Clicks-Bot"
#config.getLoggingLevel()


logging.basicConfig(level=config.getLoggingLevel(), format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)

fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

fl = logging.FileHandler(f"{path}/logs/log.log")
fl.setLevel(config.getFileLoggingLevel())
fl.setFormatter(fmt)

lg.addHandler(fl)


intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)


@bot.command(name="load")
async def load(ctx, extension):

    bot.load_extension(f"cogs.{extension}")


@bot.command(name="reload")
async def reload(ctx, extension):

    if str(extension) == "all":

        for filename_ in os.listdir(f"{path}/cogs"):
            if filename_.endswith(".py"):
                if not filename_ == "example_cog.py":
                    bot.reload_extension(f"cogs.{filename_[:-3]}")
                    lg.info(f"Loaded Extension: {filename_}")

            else:
                pass

    else:

        lg.info(f"Realoading extension: {extension}")
        bot.reload_extension(f"cogs.{extension}")
        lg.info(f"Reloaded the extension: {extension}")


@bot.command(name="unload")
async def unload(ctx, extension):

    bot.unload_extension(f"cogs.{extension}")


try:
    for filename in os.listdir(f"{path}/cogs"):
        if filename.endswith(".py"):
            if not filename == "example_cog.py":
                bot.load_extension(f"cogs.{filename[:-3]}")
                lg.info(f"Loaded Extension: {filename}")

        else:
            pass
except KeyboardInterrupt as e:

    pass

bot.run(config.getToken())


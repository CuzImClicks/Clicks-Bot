import discord
import logging
from util import config
from discord.ext import commands
import os


#TODO: hard coded path
path = os.getcwd()
#path = "/home/pi/Downloads/Clicks-Bot"
#config.getLoggingLevel()


logging.basicConfig(level=logging.INFO, format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)

fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

fl = logging.FileHandler(f"{path}/logs/log.log")
fl.setLevel(logging.INFO)
fl.setFormatter(fmt)

lg.addHandler(fl)


intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)

files = []
for filename_ in os.listdir(f"{path}/cogs"):
    if filename_.endswith(".py"):
        if not filename_ == "example_cog.py":
            files.append(filename_[:-3])

    else:
        pass

#load, unload, reload files and extension while the bot is running


@bot.command(name="load", aliases=["l"])
async def load(ctx, extension):

    if str(extension) == "all":

        for file in files:

            bot.load_extension(file)
            lg.info(f"Loaded the extension: {file[:-3]}")

    else:
        bot.load_extension(f"cogs.{extension}")
        lg.info(f"Realoading extension: {extension[:-3]}")


@bot.command(name="reload", aliases=["rl"])
async def reload(ctx, extension):

    if str(extension) == "all" or "":

        await ctx.send(f"Reloaded all Extensions", delete_after=5)

        for file in files:

            bot.reload_extension(f"cogs.{file}")
            lg.info(f"Reloaded the extension: {file}")

    else:

        lg.info(f"Realoading extension: {extension}")
        bot.reload_extension(f"cogs.{extension}")
        lg.info(f"Reloaded the extension: {extension}")


@bot.command(name="unload", aliases=["ul"])
async def unload(ctx, extension):

    if str(extension) == "all":

        for file in files:

            bot.unload_extension(f"cogs.{file}")
            lg.info(f"Unloaded the extension: {file[:-3]}")

    else:

        bot.unload_extension(f"cogs.{extension}")
        lg.info(f"Unloaded the extension: {extension[:-3]}")

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


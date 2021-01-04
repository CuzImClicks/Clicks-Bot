import discord
import logging
from util import config
from discord.ext import commands
import os
from clicks_util.json_util import json_file

path = os.getcwd()

logging.basicConfig(level=logging.INFO, format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)

fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

fl = logging.FileHandler(f"{path}/logs/log.log")
fl.setLevel(logging.INFO)
fl.setFormatter(fmt)

lg.addHandler(fl)

#read the file containing all the blacklisted people
jf = json_file("blacklist.json", path)
blacklisted = jf.read()["blacklisted"]

#gain the ability to access all guild members
intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)
#go through all files in the cogs folder and add them to the list of cogs
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
    '''Load extension'''
    if str(extension) == "all":

        for file in files:

            bot.load_extension(file)
            lg.info(f"Loaded the extension: {file[:-3]}")

    else:
        bot.load_extension(f"cogs.{extension}")
        lg.info(f"Realoading extension: {extension[:-3]}")


@bot.command(name="reload", aliases=["rl"])
async def reload(ctx, extension):
    '''Reload extension'''
    if str(extension) == "all" or "":

        await ctx.send(f"Reloaded all Extensions", delete_after=5)

        for file in files:

            bot.reload_extension(f"cogs.{file}")
            lg.info(f"Reloaded the extension: {file}")
            await ctx.send(f"Reloaded the extension: {file}")
    else:

        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded the extension: {extension}")
        lg.info(f"Reloaded the extension: {file}")

@bot.command(name="unload", aliases=["ul"])
@bot.has_role("Dev")
async def unload(ctx, extension):
    '''Unload extensions'''
    if str(extension) == "all":

        for file in files:

            bot.unload_extension(f"cogs.{file}")
            lg.info(f"Unloaded the extension: {file[:-3]}")

    else:

        bot.unload_extension(f"cogs.{extension}")
        lg.info(f"Unloaded the extension: {extension[:-3]}")

@bot.event
async def on_message(message):
    '''Message Even'''
    if message.author.bot:
        return

    if not message.guild:
        return await message.channel.send((
            "You can't use commands in direct messages"
            ))
    if str(message.author.id) in blacklisted:
        #Blacklisted people can't send messages on servers that the bot is runnning on
        lg.info(f"Blacklisted user {message.author.name} tried to send '{message.content}' in the channel {message.channel}")
        return
    
    lg.info(f"[{message.guild}] -  {message.channel}: {message.author.name}: {message.content}")
    await bot.process_commands(message)

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


import discord
import logging
from util import config
from discord.ext import commands
import os
from clicks_util.json_util import JsonFile
from datetime import datetime
import colorama

colorama.init()

path = os.getcwd()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s"+colorama.Fore.RESET, datefmt="%H:%M:%S")

lg = logging.getLogger("Clicks-Bot")
lg_pl = logging.getLogger("Extension Loader")
lg_chat = logging.getLogger("Chat") #TODO: Add chat log file handler
logging.getLogger("discord.gateway").disabled = True
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

fl = logging.FileHandler(f"{path}/logs/log.log")
fl.setLevel(logging.INFO)
fl.setFormatter(fmt)

lg.addHandler(fl)

fl_chat = logging.FileHandler(f"{path}/logs/chat.log")
fl_chat.setLevel(logging.INFO)
fl_chat.setFormatter(fmt)

lg_chat.addHandler(fl_chat)

#read the file containing all the blacklisted people
jf = JsonFile("blacklist.json", path)
blacklisted = jf.read()["blacklisted"]

#gain the ability to access all guild members
intentions = discord.Intents.all()
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

bot.remove_command("help")

#load, unload, reload files and extension while the bot is running


@bot.command(name="load", aliases=["l"])
@commands.has_role("Dev")
async def load(ctx, extension):
    '''Load extension'''
    if str(extension) == "all":
        extEmbed = discord.Embed(title="Load Extensions", description="Loading all extensions", color=discord.Colour(0x0BAF07), timestamp=datetime.now())

        for file in files:
            try:
                bot.load_extension(file)
                extEmbed.add_field(name=file, value="Load complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Loaded the extension: {file[:-3]}")

            except Exception as e:
                extEmbed.insert_field_at(index=0, name=file, value="Failed to load")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed to load extension: {file}")

        await ctx.send(embed=extEmbed)

    else:
        if not str(extension) + ".py" in os.listdir(f"{path}/cogs"):
            raise commands.errors.ExtensionNotFound(extension)
            return
        await ctx.send(
            embed=discord.Embed(title="Loading Extensions", description=f"Loading extension '{extension}'",
                                color=discord.Colour(0x0BAF07)))
        bot.load_extension(f"cogs.{extension}")
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Loading extension: {extension}")


@bot.command(name="reload", aliases=["rl"])
@commands.has_role("Dev")
async def reload(ctx, extension):
    '''Reload extension'''
    if str(extension) == "all" or "":

        extEmbed = discord.Embed(title="Reload Extensions", description="Reloading all extensions", color=discord.Colour(0x0BAF07), timestamp=datetime.now())
        for file in files:
            try:
                bot.reload_extension(f"cogs.{file}")
                extEmbed.add_field(name=file, value="Reload complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Reloaded the extension: {file}")

            except Exception as e:
                extEmbed.insert_field_at(index=0, name=file, value="Failed to reload")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed to reload extension: {file}")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed with: {e}")

        await ctx.send(embed=extEmbed)
            
    else:
        if not str(extension) + ".py" in os.listdir(f"{path}/cogs"):
            raise commands.errors.ExtensionNotFound(extension)
            return
        bot.reload_extension(f"cogs.{extension}")
        await ctx.send(embed=discord.Embed(title="Reloading Extensions",
                                           description=f"Reloading extension '{extension}'",
                                           color=discord.Colour(0x0BAF07)))
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Reloaded the extension: {extension}")


@bot.command(name="unload", aliases=["ul"])
@commands.has_role("Dev")
async def unload(ctx, extension):
    '''Unload extensions'''
    if str(extension) == "all":
        extEmbed = discord.Embed(title="Unloading Extensions",
                                 descriptions="Unloading all extensions",
                                 color=discord.Colour(0x0BA07),
                                 timestamp=datetime.now())
        await ctx.send(embed=extEmbed)
        for file in files:
            try:
                bot.unload_extension(f"cogs.{file}")
                extEmbed.add_field(name=file, value="Unload complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Unloaded the extension: {file[:-3]}")

            except Exception as e:
                extEmbed.insert_field_at(index=0, name=file, value="Failed to unload")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed to unload extension: {file}")

    else:
        if not str(extension) + ".py" in os.listdir(f"{path}/cogs"):
            raise commands.errors.ExtensionsNotFound(extension)
            return
        extEmbed = discord.Embed(title="Unloading Extension",
                                 description=f"Unloading extension '{extension}'",
                                 color=discord.Colour(0x0BA07),
                                 timestamp=datetime.now())
        await ctx.send(embed=extEmbed)
        bot.unload_extension(f"cogs.{extension}")
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Unloaded the extension: {extension[:-3]}")


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
        #Blacklisted people can't send messages on servers that the bot is running on
        lg.info(f"Blacklisted user {message.author.name} tried to send '{message.content}' in the channel {message.channel}")
        return

    elif message.channel.id == 799291117425524756:  #TODO: add list of channels that are blocked  
        await message.delete()
    
    lg_chat.info(f"{colorama.Fore.LIGHTYELLOW_EX}[{message.guild}] -  {message.channel}: {message.author.name}: {message.content}")
    await bot.process_commands(message)

try:
    for filename in os.listdir(f"{path}/cogs"):
        if filename.endswith(".py"):
            if not filename == "example_cog.py":
                try:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Loaded Extension: {filename}")

                except Exception as e:
                    lg_pl.error(f"{colorama.Fore.LIGHTRED_EX}Failed to load extension: {filename}")
                    lg_pl.error(f"Failed with: {e}")

        else:
            pass

except KeyboardInterrupt as e:

    pass

bot.run(config.getToken())


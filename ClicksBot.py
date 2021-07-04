import sys

import discord
import logging
from util import config
from discord.ext import commands
import os
from clicks_util.json_util import JsonFile
from datetime import datetime
import colorama
from util import cleanup

os.system("git pull")

cleanup.remove_songs()
cleanup.remove_hypixel_jsons()

path = os.getcwd()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s"
                                               + colorama.Fore.RESET, datefmt="%H:%M:%S", encoding='utf-8')

lg = logging.getLogger("Clicks-Bot")
lg_pl = logging.getLogger("Extension Loader")
lg_chat = logging.getLogger("Chat")
logging.getLogger("discord.gateway").disabled = True
fmt = logging.Formatter(fmt="[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

fl = logging.FileHandler(f"{path}/logs/log-{datetime.today().date()}.log", encoding='utf-8')
fl.setLevel(logging.INFO)
fl.setFormatter(fmt)

lg.addHandler(logging.StreamHandler(sys.stdout))
lg.addHandler(fl)

fl_chat = logging.FileHandler(f"{path}/logs/chat-{datetime.today().date()}.log", encoding="utf-8")
fl_chat.setLevel(logging.INFO)
fl_chat.setFormatter(fmt)

lg_chat.addHandler(fl_chat)

# read the file containing all the blacklisted people
jf = JsonFile("blacklist.json", path)
blacklisted = jf.read()["blacklisted"]

# read the file containing all the blocked channels
jf_blocked_channels = JsonFile("blocked_channels.json", path)
blocked_channels = jf_blocked_channels.read()

# gain the ability to access all guild members
intentions = discord.Intents.all()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)
# go through all files in the cogs folder and add them to the list of cogs
files = []
for filename_ in os.listdir(f"{path}/cogs"):
    if filename_.endswith(".py"):
        if not filename_ == "example_cog.py":
            files.append(filename_[:-3])

    else:
        pass


# bot.remove_command("help")

# load, unload, reload files and extension while the bot is running


@bot.command(name="load", aliases=["l"])
@commands.is_owner()
async def load(ctx, extension):
    """Load extension"""
    if str(extension) == "all":
        extEmbed = discord.Embed(title="Load Extensions", description="Loading all extensions",
                                 colour=config.getDiscordColour("green"), timestamp=datetime.now())

        for file in files:
            try:
                bot.load_extension(file)
                extEmbed.add_field(name=file, value="Load complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Loaded the extension: {file[:-3]}")

            except Exception:
                extEmbed.insert_field_at(index=0, name=file, value="Failed to load")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed to load extension: {file}")

        await ctx.send(embed=extEmbed)

    else:
        if not str(extension) + ".py" in os.listdir(f"{path}/cogs"):
            raise commands.errors.ExtensionNotFound(extension)
            return
        await ctx.send(
            embed=discord.Embed(title="Loading Extensions", description=f"Loading extension '{extension}'",
                                colour=config.getDiscordColour("green")))
        bot.load_extension(f"cogs.{extension}")
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Loading extension: {extension}")


@bot.command(name="reload", aliases=["rl"])
@commands.is_owner()
async def reload(ctx, extension):
    """Reload extension"""
    if str(extension) == "all" or "":

        extEmbed = discord.Embed(title="Reload Extensions", description="Reloading all extensions",
                                 colour=config.getDiscordColour("green"), timestamp=datetime.now())
        for file in files:
            try:
                bot.reload_extension(f"cogs.{file}")
                extEmbed.add_field(name=file, value="Reload complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Reloaded the extension: {file}")

            except Exception as error:
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
                                           colour=config.getDiscordColour("green")))
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Reloaded the extension: {extension}")


@bot.command(name="unload", aliases=["ul"])
@commands.is_owner()
async def unload(ctx, extension):
    """Unload extensions"""
    if str(extension) == "all":
        extEmbed = discord.Embed(title="Unloading Extensions",
                                 descriptions="Unloading all extensions",
                                 colour=config.getDiscordColour("green"),
                                 timestamp=datetime.now())
        await ctx.send(embed=extEmbed)
        for file in files:
            try:
                bot.unload_extension(f"cogs.{file}")
                extEmbed.add_field(name=file, value="Unload complete")
                lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Unloaded the extension: {file[:-3]}")

            except Exception as error:
                extEmbed.insert_field_at(index=0, name=file, value="Failed to unload")
                lg_pl.info(f"{colorama.Fore.LIGHTRED_EX}Failed to unload extension: {file}")

    else:
        if not str(extension) + ".py" in os.listdir(f"{path}/cogs"):
            raise commands.errors.ExtensionNotFound
            return
        extEmbed = discord.Embed(title="Unloading Extension",
                                 description=f"Unloading extension '{extension}'",
                                 colour=config.getDiscordColour("green"),
                                 timestamp=datetime.now())
        await ctx.send(embed=extEmbed)
        bot.unload_extension(f"cogs.{extension}")
        lg_pl.info(f"{colorama.Fore.LIGHTGREEN_EX}Unloaded the extension: {extension[:-3]}")


@bot.event
async def on_message(message):
    """Message Even"""
    if message.author.bot:
        return

    if message.is_system():
        return

    lg_chat.info(
        f"{colorama.Fore.LIGHTYELLOW_EX}[{str(message.guild)}] -  {str(message.channel)}: {str(message.author.name)}: {str(message.content)}")

    if message.author.id in blacklisted:
        # Blacklisted people can't send messages on servers that the bot is running on
        lg.info(
            f"Blacklisted user {message.author.name} tried to send '{message.content}' in the channel {message.channel}")
        await message.delete()
        return

    if message.channel.id in blocked_channels:
        # check if the message is in the list of blocked channels
        await message.delete()
        return

    if str(message.content).startswith(config.getCommandPrefix()) and message.channel.id == 773499837270196224:
        await message.channel.send(f"Please use {bot.get_channel(773974638963195942).mention} for commands. If you don't have the permission to use this channel please ask a admin of the server for the permissions.", delete_after = 5)
        await message.delete()
        return

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

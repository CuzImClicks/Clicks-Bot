import discord
import logging
from util import logger, MessageHandler, config
from discord.ext import commands
from util import strings
import os

path = os.getcwd()
print(path)

logging.basicConfig(level=config.getLoggingLevel(), format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl.setFormatter(fmt)

lg.addHandler(fl)

intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix=config.getCommandPrefix(), intents=intentions)


@bot.event
async def on_ready():

    for guild in bot.guilds:

        if guild.name == "GUILD":

            break


        #print(
            #f'{client.user} is connected to the following guild:\n'
            #f'{guild.name}(id: {guild.id})'
        #)

        lg.info(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name})'
        )

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=config.getStatus()))


@bot.event
async def on_member_join(member):

    lg.info(member)

    #await member.create_dm()
    #await member.send("Wilkommen")


@bot.event
async def on_message_delete(message):

    if message.author == bot.user:
        return

    await message.channel.send("Deine Nachricht wurde gelöscht!", delete_after=5)
    lg.info(f"Deleted '{message.content}' from {message.channel} by {message.author.name}")


@bot.event
async def on_message_edit(before, after):

    await before.channel.send("Deine Nachricht wurde editiert!", delete_after=5)
    lg.info(f"Edited '{before.content}' to '{after.content} from {before.channel} by {before.author.nick}")


@bot.event
async def on_raw_reaction_add(payload):

    msg_id = "703236904551972905"

    if str(payload.message_id) == msg_id:

        role2 = payload.member.guild.roles[11]
        await payload.member.add_roles(role2)
        await logger.log_role(payload, role2)

        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = bot.get_user(payload.user_id)
        emoji = payload.emoji
        lg.info("Got emoji")
        await message.remove_reaction(emoji, user)

    else:
        pass

    await logger.log_reaction(payload)


@bot.event
async def on_raw_reaction_remove(payload):

    await logger.log_reaction_remove(payload)



@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.errors.CheckFailure):

        error_msg = "Du hast nicht genügend Rechte für diesen Befehl!"

        await ctx.send(error_msg)
        await logger.log_error(error_msg)

    else:
        await logger.log_error(error)


@bot.event
async def on_typing_start(channel, user, when):

    await logger.log_typing(channel, user, when)


@bot.command(name="shutdown", help="Shuts the Bot off.")
@commands.has_role("Administrator")
async def shutdown(ctx):

    shutdown_msg = "Bot1 going dark... ... ..."

    await ctx.send(shutdown_msg)
    await logger.log_send(ctx, shutdown_msg)
    await lg.warning(f"Shutting down")



    await ctx.bot.logout()


@bot.command(name="mute", help="Mutes a user")
@commands.has_role("Administrator")
async def mute(ctx, user):
    user_list = user.split("#")
    user = discord.utils.get(ctx.author.guild.members, name=str(user_list[0]))

    lg.info(user_list)

    user = discord.utils.get(ctx.author.guild.members, name=str(user_list[0]))

    await ctx.send(f"Muted {user_list[0]}#{user_list[1]}")

    lg.info(f"Muted {user}")
    await user.edit(mute=True)


@bot.command(name="muteall", help=strings.get_help("help_muteall"))
@commands.has_role("Administrator")
async def muteall(ctx):

    try:
        for user in ctx.author.voice.channel.members:
            await user.edit(mute=True)

        await ctx.send(f"Muted all users in {ctx.author.voice.channel.name}")

    except Exception as e:
        await ctx.send("Du bist in keinem Voice Channel")
        lg.error(e)


@bot.command(name="unmuteall", help=strings.get_help("help_unmuteall"))
@commands.has_role("Administrator")
async def muteall(ctx):

    try:
        for user in ctx.author.voice.channel.members:
            await user.edit(mute=False)

        await ctx.send(f"Unmuted all users in '{ctx.author.voice.channel.name}'")

    except Exception as e:
        await ctx.send("Du bist in keinem Voice Channel")
        lg.error(e)


@bot.command(name="status", help="Changes the Status of the bot")
@commands.has_role("Developer Access")
async def status(ctx, *args):

    lg.info(args)

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}".format(" ".join(args))))
    await ctx.send("Changing status to {}".format(" ".join(args)))


@bot.event
async def on_message(message):

    if message.author == bot.user:

        return

    await MessageHandler.log(message)
    await bot.process_commands(message)


bot.run(config.getToken())
import discord
import logging
import logger
from discord.ext import commands
import os
import MessageHandler
import config
from configparser import ConfigParser




path = os.getcwd()

logging.basicConfig(level=config.getLoggingLevel(), format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl.setFormatter(fmt)

lg.addHandler(fl)

intentions = discord.Intents.default()
intentions.members = True

bot = commands.Bot(command_prefix='$', intents=intentions)


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

        for member in guild.members:

            if member.nick == None:
                lg.info(f"- {member.name}")

            else:
                lg.info(f"- {member.nick}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dich an"))


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
'''
@bot.event
async def on_error(event, *args, **kwargs):

    lg.error(event)
'''

@bot.event
async def on_raw_reaction_add(payload):

    msg_id = "703236904551972905"

    if str(payload.message_id) == msg_id:

        role2 = payload.member.guild.roles[9]
        await payload.member.add_roles(role2)
        await logger.log_role(payload, role2)

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


@bot.command(name='test', help="A test command")
@commands.has_role("Bot Access")
async def helpcmd(ctx):

    test_string = "This is my test message"

    await ctx.author.create_dm()
    await ctx.author.send(test_string)

    await ctx.send(test_string)
    await logger.log_recv(ctx)
    await logger.log_send(ctx, test_string)


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


@bot.command(name="muteall", help="Mutes all users in channels")
@commands.has_role("Administrator")
async def muteall(ctx):

    try:
        for user in ctx.author.voice.channel.members:
            await user.edit(mute=True)

        await ctx.send(f"Muted all users in {ctx.author.voice.channel.name}")

    except Exception as e:
        await ctx.send("Du bist in keinem Voice Channel")
        lg.error(e)


@bot.command(name="unmuteall", help="Unmutes all users in channels")
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
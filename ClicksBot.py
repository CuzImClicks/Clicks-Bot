import discord
import logging
import clicks_util.file_io
from clicks_util.json_util import *
from clicks_util.ansi_util import getColorCode

import logger
from discord.ext import commands
import os

white = getColorCode("white")


logging.basicConfig(level=logging.INFO, format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)
fl = logging.FileHandler(r"C:\Users\Henrik\PycharmProjects\Clicks-Bot\logs\log.log")
fl.setLevel("ERROR")

path = os.path.expanduser("~")

bot = commands.Bot(command_prefix='$')


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
            f'{guild.name}(id: {guild.id})'
        )


@bot.event
async def on_member_join(member):

    logger.log_join(member)

    await member.create_dm()
    await member.dm_channel.send(f"Test {member.name}")


@bot.event
async def on_error(event, *args, **kwargs):

    lg.error(event)
    fl.emit(event)



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

    await ctx.send(test_string)
    await logger.log_recv(ctx)
    await logger.log_send(ctx, test_string)


@bot.event
async def on_typing(channel, user, when):

    await logger.log_typing(channel, user, when)


@bot.command(name="shutdown", help="Shuts the Bot off.")
@commands.has_role("Administrator")
async def shutdown(ctx):

    shutdown_msg = "Bot1 going dark... ... ..."

    await ctx.send(shutdown_msg)
    await logger.log_send(ctx, shutdown_msg)
    await lg.warning(f"Shutting down")



    await ctx.bot.logout()





'''@bot.event
async def on_message(message):

    if message.author == bot.user:

        return

    await MessageHandler.log(message)'''



bot.run("NzcxNDY5NDA1NTM1MjA3NDY1.X5sk3w.7R3_Jma2q6yibAVTVjSMGeLW3Ao")
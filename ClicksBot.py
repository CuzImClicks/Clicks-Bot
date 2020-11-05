import asyncio

import discord
import logging
from util import logger, MessageHandler, config
from discord.ext import commands
from util import strings
from util import embed
import youtube_dl
from random import choice
import ffmpeg
import time
import os

path = os.getcwd()
print(path)
#config.getLoggingLevel()
logging.basicConfig(level=logging.DEBUG, format="\u001b[37m[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")

lg = logging.getLogger(__name__)

lg_chat = logging.getLogger("CHAT")

fl_chat = logging.FileHandler(f"{path}\logs\chat.log")
fl_chat.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl_chat.setFormatter(fmt)

fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(config.getFileLoggingLevel())
fl.setFormatter(fmt)

lg_chat.addHandler(fl_chat)
lg.addHandler(fl)

youtube_dl.utils.bug_reports_message = lambda msg: lg.error(msg)

queue = []


ytdl = youtube_dl.YoutubeDL(strings.get_ytdl_format_options())

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **strings.get_ytdl_ffmpeg_options()), data=data)


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


async def delete_cmd(ctx):

    time.sleep(5)
    await ctx.message.delete()


@bot.event
async def on_member_join(member):

    lg.info(member)

    #await member.create_dm()
    #await member.send("Wilkommen")


@bot.event
async def on_message_delete(message):

    if message.author == bot.user:
        return

    elif "$" in message.content:
        return

    else:

        await message.channel.send("Deine Nachricht wurde gelöscht!", delete_after=5)
        lg.info(f"Deleted '{message.content}' from {message.channel} by {message.author.name}")


@bot.event
async def on_message_edit(before, after):

    if "$" in before.content:
        return

    elif before.author == bot.user:
        return

    else:
        await before.channel.send("Deine Nachricht wurde editiert!", delete_after=5)
        lg.info(f"Edited '{before.content}' to '{after.content} from {before.channel} by {before.author.nick}")


@bot.event
async def on_raw_reaction_add(payload):

    msg_id = "703236904551972905"

    if str(payload.message_id) == msg_id:

        role2 = payload.member.guild.roles[12]
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

        await ctx.send(error_msg, delete_after=5)
        await logger.log_error(error_msg)

    else:
        await logger.log_error(error)

    await delete_cmd(ctx)


@bot.event
async def on_typing(channel, user, when):

    await logger.log_typing(channel, user, when)


@bot.command(name="shutdown", help="Shuts the Bot off.")
@commands.has_role("Administrator")
async def shutdown(ctx):

    shutdown_msg = "Bot1 going dark... ... ..."

    await ctx.send(shutdown_msg, delete_after=5)
    await logger.log_send(ctx, shutdown_msg)
    await lg.warning(f"Shutting down")
    await ctx.bot.logout()

    await delete_cmd(ctx)


@bot.command(name="mute", help="Mutes a user")
@commands.has_role("Administrator")
async def mute(ctx, target):

    user = discord.utils.get(ctx.author.guild.members, name=str(target))

    lg.info(user.name)

    await ctx.send(f"Muted {user.name}", delete_after=5)

    lg.info(f"Muted {user.name}")
    await user.edit(mute=True)

    await delete_cmd(ctx)


@bot.command(name="unmute", help="Unmutes a user")
@commands.has_role("Administrator")
async def unmute(ctx, target):

    user = discord.utils.get(ctx.author.guild.members, name=str(target))

    lg.info(user)

    await ctx.send(f"Unmuted {user.name}", delete_after=5)

    lg.info(f"Unmuted {user.name}")
    await user.edit(mute=False)

    await delete_cmd(ctx)


@bot.command(name="muteall", help=strings.get_help("help_muteall"))
@commands.has_role("Bot Access")
async def muteall(ctx):

    try:
        for user in ctx.author.voice.channel.members:

            if user == bot.user:
                return

            else:
                await user.edit(mute=True)

        await ctx.send(f"Muted all users in {ctx.author.voice.channel.name}", delete_after=5)

    except Exception as e:
        await ctx.send("Du bist in keinem Voice Channel", delete_after=5)
        lg.error(e)

    await delete_cmd(ctx)


@bot.command(name="unmuteall", help=strings.get_help("help_unmuteall"))
@commands.has_role("Bot Access")
async def unmuteall(ctx):

    try:
        for user in ctx.author.voice.channel.members:
            await user.edit(mute=False)

        await ctx.send(f"Unmuted all users in '{ctx.author.voice.channel.name}'", delete_after=5)

    except Exception as e:
        await ctx.send("Du bist in keinem Voice Channel", delete_after=5)
        lg.error(e)

    await delete_cmd(ctx)


@bot.command(name="status", help="Changes the Status of the bot")
@commands.has_role("Developer Access")
async def status(ctx, *args):

    lg.info(args)

    await delete_cmd(ctx)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="{}".format(" ".join(args))))
    await ctx.send("Changing status to {}".format(" ".join(args)), delete_after=5)


@bot.command(name="github")
@commands.has_role("Member")
async def github(ctx):

    await ctx.send("Die GitHub Page des Bots ist https://github.com/CuzImClicks/Clicks-Bot")


@bot.command(name="botaccess")
@commands.has_role("Dev")
async def bot_access(ctx, target):

    lg.info(target)
    user = discord.utils.get(ctx.author.guild.members, name=str(target))

    lg.info(f"Got User {user.name} as target for promotion")
    
    role = ctx.author.guild.roles[15]

    await user.add_roles(role)
    lg.info(f"Added '{role.name}' to '{user.name}'")

    #await embed.send_embed_dm(bot, user, infos=("Bot Access", "Bot Access Output"), names=("Granted bot access"), values=(strings.get_promotion_text(ctx.author, user)))

    await ctx.send(f"Added '{role.name}' to '{user.name}'")
    await logger.log_send(ctx, f"Added '{role.name} to {user.name}'")

    await user.create_dm()
    await user.dm_channel.send(strings.get_promotion_text(ctx.author, user))


@bot.command(name="ping")
@commands.has_role("Bot Access")
async def ping(ctx):

    msg = f"Pong! Dein Ping ist {round(bot.latency, 2)*1000}ms"

    await ctx.send(msg, delete_after=5)
    await logger.log_send(ctx, msg)

    await delete_cmd(ctx)


@bot.command(name="credits", help="Gibt dir eine Übersicht von wem der Bot erstellt und geschrieben wurde.")
@commands.has_role("Bot Access")
async def credits(ctx):

    #await ctx.send(strings.get_credits())
    #await logger.log_send(ctx, strings.get_credits())

    await embed.send_embed(bot=bot, ctx=ctx, infos=("Credits", "Credits to the ones who deserve", 0x2b4f22), names=("Idee und Coding", "Textgestaltung", "Server Owner"), values=("Idee und coding: Henrik | Clicks", "Textgestaltung : Kai | K_Stein", "Bereitstellung des Servers : Luis | DasVakuum"), inline=(False, False, False))


# Music bot

@bot.command(name="join")
@commands.has_role("Bot Access")
async def join(ctx):

    channel = ctx.author.voice.channel

    delete_cmd(ctx)

    if not ctx.message.author.voice:

        await ctx.send("You are not connected to a voice channel!")
        return

    else:

        channel = ctx.message.author.voice.channel

        await channel.connect()

    await channel.connect()


@bot.command(name="play")
@commands.has_role("Bot Access")
async def play(ctx):

    global queue
    server = ctx.message.author.guild

    voice_channel = server.voice_client

    async with ctx.typing():

        player = await YTDLSource.from_url(queue[0], loop=bot.loop)

        voice_channel.play(player, after=lambda e: lg.error(e) if e else None)

    await ctx.send(f"Now playing: {player.title}")

    del(queue[0])


@bot.command(name="die")
@commands.has_role("Bot Access")
async def die(ctx):

    responses = ["Clicks Bot going dark ... ... ...", ]

    await ctx.send(choice(responses))


@bot.command(name="queue")
@commands.has_role("Bot Access")
async def queue_func(ctx, url):

    global queue

    queue.append(url)
    await ctx.send(f"Added {url} to queue")


@bot.command(name="remove")
@commands.has_role("Bot Access")
async def remove(ctx, number):

    global queue

    try:
        del(queue[int(number)])
        await ctx.send("The song was added to the Queue")

    except:
        await ctx.send(f"The Queue is either empty or the number is too high")


@bot.command(name="rick")
@commands.has_role("Dev")
async def rick(ctx):

    pass




@bot.command(name="pause")
@commands.has_role("Bot Access")
async def pause(ctx):

    server = ctx.message.author.guild
    voice_channel = server.voice_client

    voice_channel.pause()


@bot.command(name="resume")
@commands.has_role("Bot Access")
async def resume(ctx):

    server = ctx.message.author.guild
    voice_channel = server.voice_client

    voice_channel.resume()


@bot.command(name="volume")
@commands.has_role("Bot Access")
async def volume(ctx):

    pass


@bot.command(name="leave")
@commands.has_role("Bot Access")
async def leave(ctx):

    if not ctx.message.author.voice:

        await ctx.send("You are not connected to a voice channel!")

        return

    else:

        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()







@bot.event
async def on_message(message):

    if message.author == bot.user:

        return

    lg_chat.info(f"[{message.author}] in {message.channel} - {message.content}")
    await bot.process_commands(message)

try:
    bot.run(config.getToken())

except KeyboardInterrupt as e:

    pass

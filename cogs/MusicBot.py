import discord
from discord.ext import commands
import asyncio

from multiprocessing import Process, Lock
import youtube_dl
import logging
from random import choice

from util import strings
from util import logger
from util.logger import *
from util import config


lg = logging.getLogger(__name__)

global ytdl, queue
ytdl = youtube_dl.YoutubeDL(strings.get_ytdl_format_options())
queue = []
youtube_dl.utils.bug_reports_message = lambda msg: lg.error(msg)


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


class MusicBot(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="join", help="Mit $join joint der Musikbot deinem Sprachchannel.")
    @commands.has_role(config.getBotAdminRole())
    async def join(self, ctx):

        channel = ctx.author.voice.channel

        if not ctx.message.author.voice:

            await ctx.send("You are not connected to a voice channel!")
            return

        else:

            channel = ctx.message.author.voice.channel

            await logger.log_send(ctx,
                                  "If you want to add songs to the queue ues $queue, then if you want to play it use $play")
            try:
                await channel.connect()

            except discord.ClientException:
                await ctx.send(f"Already connected to your voice channel")

        await ctx.send("If you want to add songs to the queue ues $queue, then if you want to play it use $play")
        await log_send(ctx, "If you want to add songs to the queue ues $queue, then if you want to play it use $play")

    @commands.command(name="play", help="Mit $play startest du die Wiedergabe der Musik in deinem Channel."
                                   " Dies funktioniert nur wenn du einem Sprachchannel bist und nur wenn bereits Songs"
                                   " in der Queue sind. Gebe $queue ohne Argumente ein um zu sehen ob songs in der Queue sind.")
    @commands.has_role(config.getBotAdminRole())
    async def play(self, ctx, *args):

        global queue
        server = ctx.message.author.guild

        voice_channel = server.voice_client
        playing = False

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(str(queue[0]), loop=self.bot.loop)
                self.currently_playing = str(queue[0])
                voice_channel.play(player, after=lambda e: lg.error(e) if e else None)
                playing = True

        except IndexError as e:

            lg.error(f"No songs left in queue!")
            await ctx.send(f"No songs left in queue!")

        if not args:
            return

        if args[0] == "loop":
            await ctx.send(f"Now playing: {player.title}", delete_after=5)
            await log_send(ctx, f"Now playing: {player.title}")
        else:
            del(queue[0])
            lg.info(f"Removed song {queue[0]} from queue")

    @commands.command(name="among_us", help="Dieser Befehl setzt alle Lieder die als Among Us Lied gespeichert wurden"
                                            " in zufälliger Reihenfolge in die Warteschleife. Mit .skipall"
                                            "werden alle Songs die der Bot und die Queue hinzugefügt hat übersprungen. "
                                            )
    @commands.has_role(config.getBotAdminRole())
    async def among_us(self, ctx):

        interstellar_no_time_for_caution = "https://www.youtube.com/watch?v=m3zvVGJrTP8"
        interstellar_main_theme = "https://www.youtube.com/watch?v=UDVtMYqUAyw"
        inception_main_theme = "https://www.youtube.com/watch?v=RxabLA7UQ9k"

        global queue

        queue.clear()
        list = []

        list.append(interstellar_no_time_for_caution)
        list.append(interstellar_main_theme)
        list.append(inception_main_theme)

        for i in range(0, len(list)):
            song = choice(list)
            lg.info(f"Added song {song} to queue")
            queue.append(song)
            del (list[list.index(song)])

        await ctx.send("Queued the Among Us songs", delete_after=5)
        await log_send(ctx, "Queued the Among Us songs")
        for i in range(0, len(queue)):
            await self.play(ctx)

    @commands.command(name="die")
    @commands.has_role(config.getBotAdminRole())
    async def die(self, ctx):

        global queue
        server = ctx.message.author.guild
        voice_channel = server.voice_client

        voice_channel.pause()
        queue.clear()
        lg.info(queue)

        responses = ["Clicks Bot going dark ... ... ...", ]

        await ctx.send(choice(responses))
        await logger.log_send(ctx, choice(responses))

    @commands.command(name="loop", help="Continues to play the same song")
    @commands.has_role(config.getBotAdminRole())
    async def loop(self, ctx, *args):

        if not self.loop:
            loop = True
            global queue
            queue.append(self.currently_playing)

        else:
            loop = False
            queue.clear()
            await self.pause()

        lg.info(f"Looping song")
        await ctx.send("Looping song")

    @commands.command(name="queue", help=strings.get_help("queue_help"))
    @commands.has_role(config.getBotAdminRole())
    async def queue_func(self, ctx, *args):

        global queue
        if args:
            url = args[0]

        else:
            url = None

        if url is None:
            if len(queue) == 0:
                await ctx.send("There are no songs in the queue")

            for i in range(0, len(queue)):
                await ctx.send("This is the full queue right now:")
                await ctx.send(queue[i], delete_after=5)
                await log_send(ctx, queue[i])

        else:

            queue.append(url)
            lg.info(f"Added {url} to queue")
            await ctx.send(f"Added {url} to queue", delete_after=5)
            await logger.log_send(ctx, f"Added {url} to queue")

            lg.info(args)
            if not args[0] == "loop":
                await self.play(ctx)
                self.loop = False
            else:
                await self.loop(ctx)



    @commands.command(name="remove")
    @commands.has_role(config.getBotAdminRole())
    async def remove(self, ctx, number):

        global queue

        try:
            del (queue[int(number)])
            lg.info(f"Deleted {queue[int(number)]} from queue")
            await ctx.send("The song was added to the Queue", delete_after=5)
            await logger.log_send(ctx, "The song was added to the Queue")

        except:
            await ctx.send(f"The Queue is either empty or the number is too high", delete_after=5)
            await logger.log_send(ctx, f"The Queue is either empty or the number is too high")

    @commands.command(name="rick")
    @commands.has_role(config.getBotAdminRole())
    async def rick(self, ctx):

        queue.insert(0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        await self.play(ctx)

    @commands.command(name="skipall", help="Dieser Befehl löscht die gesamte Song-Warteschleife und hört auf Musik "
                                           "abzuspielen. Nun kannst du neue Songs in die Queue stellen.")
    @commands.has_role(config.getBotAdminRole())
    async def skipall(self, ctx):

        global queue

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        queue.clear()

        await ctx.send(f"Cleared the playlist!", delete_after=5)
        await log_send(ctx, f"Cleared the playlist!")

        voice_channel.pause()

    @commands.command(name="skip",
                 help="Mit $skip überspringst du den aktuell spielenden Song und der Bot spielt automatisch "
                      "den nächsten Song in der Queue ab.")
    @commands.has_role(config.getBotAdminRole())
    async def skip(self, ctx):

        global queue

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        await ctx.send(f"Skipped the song!", delete_after=5)
        await log_send(ctx, f"Skipped the song!")

        voice_channel.pause()
        await self.play(ctx)

    @commands.command(name="pause", help="Pausiert den aktuell spielenden Song.")
    @commands.has_role(config.getBotAdminRole())
    async def pause(self, ctx):

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        voice_channel.pause()
        lg.info(f"Paused the song currently playing!")
        await ctx.send(f"Der aktuell spielende Song wurde pausiert. Mit .resume spielt der Song weiter.", delete_after=5)
        await logger.log_send(ctx, f"Paused song currently playing!")

    @commands.command(name="resume", help="Der pausierte Song wird weiter abgespielt.")
    @commands.has_role(config.getBotAdminRole())
    async def resume(self, ctx):

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        voice_channel.resume()
        lg.info(f"Resumed the song currently playing!")

        await ctx.send(f"Resumed song currently playing!", delete_after=5)
        await logger.log_send(ctx, f"Resumed song currently playing!")

    @commands.command(name="volume")
    @commands.has_role(config.getBotAdminRole())
    async def volume(self, ctx):

        pass

    @commands.command(name="leave")
    @commands.has_role(config.getBotAdminRole())
    async def leave(self, ctx):

        if not ctx.message.author.voice:

            await ctx.send("You are not connected to a voice channel!", delete_after=5)
            await logger.log_send(ctx, "You are not connected to a voice channel!")

            return

        else:

            voice_client = ctx.message.guild.voice_client
            await voice_client.disconnect()
            await lg.info(f"Disconnected from channel {ctx.message.author.voice.channel}")
            await logger.log_send(ctx, f"Disconnected from channel {ctx.message.author.voice.channel}")


def setup(bot):
    bot.add_cog(MusicBot(bot))

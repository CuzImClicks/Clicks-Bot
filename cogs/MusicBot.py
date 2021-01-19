import discord
from discord.ext import commands
import asyncio
from datetime import datetime
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

global last_song, loop
last_song = ""
loop = False

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

    @commands.command(name="join", help="Mit .join joint der Musikbot deinem Sprachchannel.")
    @commands.has_role(config.getBotAdminRole())
    async def join(self, ctx):

        channel = ctx.author.voice.channel

        if not ctx.message.author.voice:
            errorEmbed = discord.Embed(title="Command Error", description="You are not connected to a voice channel", color=discord.Colour(0x9D1309), timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            return

        else:

            channel = ctx.message.author.voice.channel

            try:
                await channel.connect()

            except discord.ClientException:
                errorEmbed = discord.Embed(title="Command Error", description="Already connected to your voice channel", color=discord.Colour(0x9D1309), timestamp=datetime.now())
                await ctx.send(embed=errorEmbed)

        infoEmbed = discord.Embed(title="Join", description="If you want to add songs to the queue use .queue, then if you want to play use .play", color=discord.Colour(0x000030), timestamp=datetime.now())
        await ctx.send(embed=infoEmbed)

    @commands.command(name="play", help="Mit .play startest du die Wiedergabe der Musik in deinem Channel."
                                   " Dies funktioniert nur wenn du einem Sprachchannel bist und nur wenn bereits Songs"
                                   " in der Queue sind. Gebe .queue ohne Argumente ein um zu sehen ob songs in der Queue sind.")
    @commands.has_role(config.getBotAdminRole())
    async def play(self, ctx):

        global queue
        server = ctx.message.author.guild

        voice_channel = server.voice_client
        playing = False

        try:
            async with ctx.typing():
                player = await YTDLSource.from_url(str(queue[0]), loop=self.bot.loop)
                voice_channel.play(player, after=lambda e: lg.error(e) if e else None)
                playing = True
                global last_song 
                last_song = str(queue[0])
                if not loop:
                    lg.info(f"Removed song {queue[0]} from the queue ")
                    del(queue[0])

                infoEmbed = discord.Embed(title="Play", description=f"Now playing {player.title}", color=discord.Colour(0x000030), timestamp=datetime.now())
                await ctx.send(embed=infoEmbed)
                        
        except IndexError as e:

            lg.error(f"No songs left in queue!")
            errorEmbed = discord.Embed(title="Command Error", description="No songs left in the queue", color=discord.Colour(0x9D1309), timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)

    async def wait_for_end(self, guild: discord.Guild):
        from discord.utils import get
        voice = get(self.bot.voice_clients, guild=guild)
        while voice.is_playing():
            await asyncio.sleep(1)

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

        infoEmbed = discord.Embed(title="Among Us", description="Queued the Among Us songs", color=discord.Colour(0x000030), timestamp=datetime.now())
        await ctx.send(embed=infoEmbed)

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
        lg.info(f"Cleared the queue!")

        responses = ["Clicks Bot going dark ... ... ...", ]

        infoEmbed = discord.Embed(title="Shutdown", description=responses[0], color=discord.Colour(0x000030), timestamp=datetime.now())
        await ctx.send(choice(embed=infoEmbed))

    @commands.command(name="loop", help="Continues to play the same song")
    @commands.has_role(config.getBotAdminRole())
    async def loop(self, ctx, *args):
        global queue, loop
        loop = True
        queue.append(last_song)
        infoEmbed = discord.Embed(title="Loop", description="Looping song", color=discord.Colour(0x000030), timestamp=datetime.now())
        await ctx.send(embed=infoEmbed)

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
                errorEmbed = discord.Embed(title="Command Error", description="There are no songs in the queue", color=discord.Colour(0x9D1309), timestamp=datetime.now())
                await ctx.send(embed=errorEmbed)

            else:
                for i in range(0, len(queue)):
                    await ctx.send("This is the full queue right now:")
                    await ctx.send(queue[i], delete_after=5)
                    await log_send(ctx, queue[i])

        else:

            queue.append(url)
            lg.info(f"Added {url} to queue")
            infoEmbed = discord.Embed(title="Queue", description=f"Added {url} to the queue", color=discord.Colour(0x000030), timestamp=datetime.now())
            await ctx.send(embed=infoEmbed)
            lg.info(args)


    @commands.command(name="remove")
    @commands.has_role(config.getBotAdminRole())
    async def remove(self, ctx, number):

        global queue

        try:
            if number > len(queue):
                errorEmbed = discord.Embed(title="Command Error", description="The queue isn't that long", color=discord.Colour(0x9D1309), timestamp=datetime.now())
                await ctx.send(embed=errorEmbed)
            del (queue[int(number)])
            lg.info(f"Deleted {queue[int(number)]} from queue")
            infoEmbed = discord.Embed(title="Remove", description="The song was removed from the queue", color=discord.Colour(0x000030), timestamp=datetime.now())
            await ctx.send(embed=infoEmbed)

        except:
            errorEmbed = discord.Embed(title="Command Error", description="The queue is empty", color=discord.Colour(0x9D1309), timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)

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
        if len(queue) > 0:
            lg.info(f"Removed the song {queue[0]} from the queue")
            del(queue[0])
            await self.play(ctx)

        else:
            await ctx.send(f"There are no more songs in the queue")
            voice_channel.pause()

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
            return

        else:

            voice_client = ctx.message.guild.voice_client
            await voice_client.disconnect()
            lg.info(f"Disconnected from channel {ctx.message.author.voice.channel}")


def setup(bot):
    bot.add_cog(MusicBot(bot))

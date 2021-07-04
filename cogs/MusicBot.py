import asyncio
import json
import sys
from random import choice

import discord
import youtube_dl
from aiohttp import ClientSession
from discord.ext import commands
from discord.utils import get
from lyricsgenius import Genius

from clicks_util import timeconvert
from util import config, strings
from util.cleanup import remove_songs
from util.genius.Song import Song
from util.logger import *

lg = logging.getLogger(__name__[5:])

youtube_dl.utils.bug_reports_message = lambda msg: lg.error(msg)

genius = Genius(config.getGeniusKey())

ytdl = youtube_dl.YoutubeDL(strings.get_ytdl_format_options())

global current_song
current_song = ""


async def getLastSong():
    return current_song


class HiddenPrints:
    """
    Usage:
    with HiddenPrints():
        ...
    """

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class YTDLSource(discord.PCMVolumeTransformer):

    # YouTube said: Unable to extract video data
    # pip install -U youtube-dl
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
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **strings.get_ytdl_ffmpeg_options()), data=data)


class YouTubeVideo:

    def __init__(self, url: str, author: discord.Member = None, original_search: str = None) -> None:
        self.id = url.split("https://www.youtube.com/watch?v=")[1]
        if url.startswith("https://youtu.be/"):
            url = "https://www.youtube.com/watch?v=" + url.split("https://youtu.be/")[1]
        self.url = url
        self.author = author
        self.original_search = original_search

    async def data(self) -> dict:
        async with ClientSession() as session:
            async with session.get(
                    "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + self.id + "&key=" + config.getYoutubeKey()) as data:
                video = json.loads(await data.text())["items"][0]["snippet"]
                return video

    async def title(self):
        return str(dict(await self.data())["title"])

    async def description(self):
        return str(dict(await self.data())["description"])

    async def channel(self):
        return str(dict(await self.data())["channel"])

    async def thumbnail(self):
        return f"https://img.youtube.com/vi/{self.id}/sddefault.jpg"


class MusicBot(commands.Cog):
    paused = False
    save_queue = False
    loop = False

    queue = []

    def __init__(self, bot):

        self.bot = bot
        remove_songs()

    def cog_unload(self):
        remove_songs()

    @commands.command(name="join", help="The bot joins your channel")
    @commands.has_role(config.getBotMusicRole())
    async def join(self, ctx):

        channel = ctx.author.voice.channel
        if not ctx.message.author.voice:
            errorEmbed = discord.Embed(title="Command Error",
                                       color=config.getDiscordColour("red"), timestamp=datetime.now())
            errorEmbed.add_field(name="Error Message", value="You are not connected to a voice channel")
            errorEmbed.add_field(name="Raised by", value=ctx.author.nick)
            await ctx.send(embed=errorEmbed)
            return

        else:

            try:
                channel = ctx.message.author.voice.channel
                await channel.connect()

            except discord.ClientException:
                errorEmbed = discord.Embed(title="Command Error",
                                           color=config.getDiscordColour("red"), timestamp=datetime.now())
                errorEmbed.add_field(name="Error Message", value="Already connected to your voice channel")
                errorEmbed.add_field(name="Raised by", value=ctx.author.nick)
                await ctx.send(embed=errorEmbed)

        infoEmbed = discord.Embed(title="Join",
                                  description=f"Joined the channel {channel} in guild {ctx.author.guild.name}",
                                  colour=config.getDiscordColour("blue"))
        infoEmbed.add_field(name="Queue commands", value=f"""
        .queue <url> - add a song to the queue(the bot will start playing automaticly)
        .insert <url> - insert a song at the start of the queue
        .skip - skip a song(the next song will start playing)
        .skipall - clear the entire queue
        .remove <index(starts at 0)> - remove the song at the given index
        .loop - play the current song endlessly
        .pause - pause the current song
        .play - force the bot to play
         """)
        infoEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=infoEmbed)

    @commands.command(name="play", help="Starts playing the first song in the queue")
    @commands.has_role(config.getBotMusicRole())
    async def play(self, ctx):

        global current_song

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        try:
            if not voice_channel.is_connected():
                return
            async with ctx.typing():
                player = await YTDLSource.from_url(str(self.queue[0].url), loop=self.bot.loop)
                error_msg = ""
                voice_channel.play(player, after=lambda error: error_msg.join(error) if error else None)
                if error_msg.__contains__("DownloadError"):
                    raise youtube_dl.DownloadError("error_msg")
                self.paused = False
                current_song = self.queue[0]
                if not self.loop:
                    if self.save_queue:
                        self.queue.append(self.queue[0])
                    lg.info(f"Removed song {await self.queue[0].title()} from the queue ")
                    del (self.queue[0])

                infoEmbed = discord.Embed(description=f"Now playing [{player.title}]({current_song.url})",
                                          color=config.getDiscordColour("blue"))
                infoEmbed.set_image(url=await current_song.thumbnail())
                if current_song.author:
                    infoEmbed.set_author(name=current_song.author.nick, icon_url=current_song.author.avatar_url)

                if not self.loop:
                    await ctx.send(embed=infoEmbed)

            await self.wait_for_end(ctx)
            if self.queue and not self.paused:
                await self.play(ctx)

        except IndexError:
            if len(self.queue) == 0:
                errorEmbed = discord.Embed(title="Command Error", description="No songs left in the queue",
                                           color=config.getDiscordColour("red"), timestamp=timeconvert.getTime())
                await ctx.send(embed=errorEmbed)
                return

        except youtube_dl.DownloadError as e:
            if e.args.__contains__("This video is not available"):
                errorEmbed = discord.Embed(title="Download Error",
                                           description="This video is not available.",
                                           colour=config.getDiscordColour("red"))
                await ctx.send(embed=errorEmbed)

            elif e.args.__contains__("This video is only available to Music Premium members"):
                errorEmbed = discord.Embed(title="Download Error",
                                           description="This video is only available to Music Premium members",
                                           colour=config.getDiscordColour("red"))
                await ctx.send(embed=errorEmbed)

    async def wait_for_end(self, ctx):
        from discord.utils import get
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if not voice:

            await self.join(ctx)
            await self.play(ctx)

        while voice.is_playing():
            await asyncio.sleep(1)

    @commands.command(name="among_us", help="Queues all configured Among Us songs")
    @commands.has_role(config.getBotMusicRole())
    async def among_us(self, ctx):

        interstellar_no_time_for_caution = "https://www.youtube.com/watch?v=m3zvVGJrTP8"
        interstellar_main_theme = "https://www.youtube.com/watch?v=UDVtMYqUAyw"
        inception_main_theme = "https://www.youtube.com/watch?v=RxabLA7UQ9k"

        self.queue.clear()
        list_ = [YouTubeVideo(interstellar_no_time_for_caution), YouTubeVideo(interstellar_main_theme),
                 YouTubeVideo(inception_main_theme)]

        for i in range(0, len(list_)):
            song = choice(list_)
            lg.info(f"Added song {song.title} to queue")
            self.queue.append(song)
            del (list_[list_.index(song)])

        infoEmbed = discord.Embed(title="Among Us", description="Queued the Among Us songs",
                                  color=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
        await ctx.send(embed=infoEmbed)

        for i in range(0, len(self.queue)):
            await self.play(ctx)

    @commands.command(name="die", help="Hard resets the queue and stops playing")
    @commands.has_role(config.getBotMusicRole())
    async def die(self, ctx):
        try:
            server = ctx.message.author.guild
            voice_channel = server.voice_client
            voice_channel.pause()
        except AttributeError:
            errorEmbed = discord.Embed(title="Die Error",
                                       description="You are not connected to a voice channel",
                                       colour=config.getDiscordColour("red"))
            errorEmbed.set_author(name=ctx.author.nick, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=errorEmbed)
            return
        self.queue.clear()
        lg.info(f"Cleared the queue!")
        self.loop = False
        self.save_queue = False
        infoEmbed = discord.Embed(title="Die", description="Resetted the MusicBot",
                                  color=config.getDiscordColour("red"))
        await ctx.send(embed=infoEmbed)
        await self.leave(ctx)
        await asyncio.sleep(2)
        await self.join(ctx)

    @commands.command(name="loop", help="Continues to play the same song")
    @commands.has_role(config.getBotMusicRole())
    async def loop(self, ctx):
        if not self.loop:
            self.loop = True
            self.queue.append(current_song)
            infoEmbed = discord.Embed(title="Loop", description="Looping the current song",
                                      color=config.getDiscordColour("blue"))
            await ctx.send(embed=infoEmbed)

        elif self.loop:
            self.loop = False
            infoEmbed = discord.Embed(title="Loop", description="Not looping song anymore",
                                      color=config.getDiscordColour("blue"))
            self.queue.remove(0)
            await ctx.send(embed=infoEmbed)

    @commands.command(name="queue", help=strings.get_help("queue_help"), aliases=["q"])
    @commands.has_role(config.getBotMusicRole())
    async def queue_func(self, ctx, *args):
        url = None
        if args:
            if str(args[0]) == "loop":
                self.save_queue = not self.save_queue
                infoEmbed = discord.Embed(
                    description="Don't remove songs from the queue has been set to " + str(self.save_queue),
                    colour=config.getDiscordColour(self.save_queue))
                await ctx.send(embed=infoEmbed)
                if not self.save_queue:
                    del(self.queue[0])
                return

            elif str(args[0]).startswith("https://"):
                url = args[0]

            else:
                convertTuple = lambda tup: str(tup).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
                msg = convertTuple(args)
                infoEmbed = discord.Embed(title=f"Searching song '{msg}'")
                await ctx.send(embed=infoEmbed)
                try:
                    song = Song(msg)
                    url = ""
                    for provider in song.media:
                        if provider["provider"] == "youtube":
                            url = song.media[int(song.media.index(provider))]["url"].replace("http", "https")

                    if url == "":
                        errorEmbed = discord.Embed(title="Command Error",
                                                   description="Could not find song on YouTube",
                                                   colour=config.getDiscordColour("red"))
                        await ctx.send(embed=errorEmbed)
                        return

                except AttributeError as e:
                    lg.error(e)
                    errorEmbed = discord.Embed(title="Command Error",
                                               description="Could not find song on Genius, please provide more information or post the song directly with a youtube.com link",
                                               colour=config.getDiscordColour("red"))
                    await ctx.send(embed=errorEmbed)
                    return

                except Exception as e:
                    lg.error(e)
                    return

        else:
            url = None

        if url is None:
            if len(self.queue) == 0:
                errorEmbed = discord.Embed(title="Command Error", description="There are no songs in the queue",
                                           colour=config.getDiscordColour("red"))
                await ctx.send(embed=errorEmbed)

            else:
                infoEmbed = discord.Embed(title="Queue", description="This is the full queue right now")
                for i in range(0, len(self.queue)):
                    song = self.queue[i]
                    infoEmbed.add_field(name="Song", value=f"[{await song.title()}]({song.url})", inline=False)
                    if song.author.nick:
                        infoEmbed.add_field(name="Requested by", value=song.author.nick, inline=True)
                    elif song.author.name:
                        infoEmbed.add_field(name="Requested by", value=song.author.name, inline=True)
                await ctx.send(embed=infoEmbed)

        else:

            try:
                video = YouTubeVideo(url, ctx.author)
                self.queue.append(video)
                lg.info(f"Added {url} to queue")

            except IndexError:
                errorEmbed = discord.Embed(title="Command Error", description="Invalid URL",
                                           color=config.getDiscordColour("red"))
                errorEmbed.add_field(name="Possible causes",
                                     value="youtube short urls and indirect links can cause errors while downloading")
                errorEmbed.set_footer(text=timeconvert.getTime())

                await ctx.send(embed=errorEmbed)
                return

            infoEmbed = discord.Embed(title="Queue",
                                      description=f"Added [{await video.title()}]({video.url}) to the queue",
                                      colour=config.getDiscordColour("blue"))
            infoEmbed.set_image(url=await video.thumbnail())
            if video.author.nick:
                infoEmbed.add_field(name="Requested by", value=video.author.nick, inline=True)
            elif video.author.name:
                infoEmbed.add_field(name="Requested by", value=video.author.name, inline=True)
            infoEmbed.add_field(name="Position in queue", value=str(len(self.queue)))
            await ctx.send(embed=infoEmbed)
            try:
                voice = get(self.bot.voice_clients, guild=ctx.author.guild)
                if not voice:
                    raise AttributeError
            except AttributeError:
                await self.join(ctx)
                await self.play(ctx)
            try:
                if not voice.is_playing() & voice.is_connected():
                    await self.play(ctx)
            except AttributeError:
                pass

    @commands.command(name="remove")
    @commands.has_role(config.getBotMusicRole())
    async def remove(self, ctx, number):

        number = int(number)
        if number > len(self.queue):
            errorEmbed = discord.Embed(title="Command Error", description="The queue isn't that long",
                                       color=config.getDiscordColour("red"), timestamp=timeconvert.getTime())
            await ctx.send(embed=errorEmbed)

        if not len(self.queue) == 0:
            del (self.queue[int(number)])
            lg.info(f"Deleted {self.queue[int(number)]} from queue")
            infoEmbed = discord.Embed(title="Remove", description="The song was removed from the queue",
                                      color=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
            await ctx.send(embed=infoEmbed)

        else:
            errorEmbed = discord.Embed(title="Command Error", description="The queue is empty",
                                       color=config.getDiscordColour("red"), timestamp=timeconvert.getTime())
            await ctx.send(embed=errorEmbed)

    @commands.command(name="insert")
    @commands.has_role(config.getBotMusicRole())
    async def insert(self, ctx, url):
        if url.startswith("https://youtu.be/"):
            url = "https://www.youtube.com/watch?v=" + url.split("https://youtu.be/")[1]
        video = YouTubeVideo(url, ctx.author)
        self.queue.insert(0, video)
        infoEmbed = discord.Embed(title="Queue",
                                  description=f"Inserted [{await video.title()}]({video.url}) at index 0",
                                  colour=config.getDiscordColour("blue"))
        await ctx.send(embed=infoEmbed)

    @commands.command(name="rick")
    @commands.has_role(config.getBotMusicRole())
    async def rick(self, ctx):

        self.queue.insert(0, YouTubeVideo("https://www.youtube.com/watch?v=dQw4w9WgXcQ", ctx.author))
        await self.play(ctx)

    @commands.command(name="skipall", help="Dieser Befehl löscht die gesamte Song-Warteschleife und hört auf Musik "
                                           "abzuspielen. Nun kannst du neue Songs in die Queue stellen.",
                      aliases=["sa", "queue_clear", "qc"])
    @commands.has_role(config.getBotMusicRole())
    async def skipall(self, ctx):

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        self.queue.clear()

        # TODO: convert to embed
        await ctx.send(f"Cleared the playlist!")

        voice_channel.pause()

    @commands.command(name="skip",
                      help="Mit .skip überspringst du den aktuell spielenden Song und der Bot spielt automatisch "
                           "den nächsten Song in der Queue ab.")
    @commands.has_role(config.getBotMusicRole())
    async def skip(self, ctx):

        server = ctx.message.author.guild
        voice_channel = server.voice_client

        await ctx.send(f"Skipped the song!")
        if len(self.queue) > 0:
            voice_channel.pause()
            await self.play(ctx)

        else:
            infoEmbed = discord.Embed(title="Queue Error",
                                      colour=config.getDiscordColour("red"))
            infoEmbed.add_field(name="Error Message", value=f"There are no more songs in the queue")
            infoEmbed.set_author(name=ctx.author, url=ctx.author.avatar_url)
            voice_channel.pause()

    @commands.command(name="pause", help="Pausiert den aktuell spielenden Song.")
    @commands.has_role(config.getBotMusicRole())
    async def pause(self, ctx):

        server = ctx.message.author.guild
        voice_channel = server.voice_client
        if self.paused:
            voice_channel.resume()
            self.paused = False
            infoEmbed = discord.Embed(description="Resumed song currently playing",
                                      colour=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
            lg.info("Resumed the song currently playing!")

        else:
            voice_channel.pause()
            self.paused = True
            infoEmbed = discord.Embed(description="Paused song currently playing",
                                      colour=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
            lg.info(f"Paused the song currently playing!")

        await ctx.send(embed=infoEmbed)

    @commands.command(name="resume", help="Der pausierte Song wird weiter abgespielt.")
    @commands.has_role(config.getBotMusicRole())
    async def resume(self, ctx):
        server = ctx.message.author.guild
        voice_channel = server.voice_client

        voice_channel.resume()
        self.paused = False
        lg.info(f"Resumed the song currently playing!")
        await ctx.send(
            embed=discord.Embed(description="Resumed song currently playing", colour=config.getDiscordColour("blue"),
                                timestamp=timeconvert.getTime()))

    @commands.command(name="leave")
    @commands.has_role(config.getBotMusicRole())
    async def leave(self, ctx):

        if not ctx.message.author.voice:
            # TODO: convert to embed
            await ctx.send("You are not connected to a voice channel!")
            return

        else:

            voice_client = ctx.message.guild.voice_client
            await voice_client.disconnect()
            lg.info(f"Disconnected from channel {ctx.message.author.voice.channel}")
            remove_songs()


def setup(bot):
    bot.add_cog(MusicBot(bot))

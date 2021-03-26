import discord
from discord.ext import commands
import logging
from util import config
import lyricsgenius
from clicks_util import text, numbers, HiddenPrints
from cogs.MusicBot import getLastSong
import sys, os
import logging
import os
import sys

import discord
import lyricsgenius
from discord.ext import commands

from clicks_util import text, numbers, HiddenPrints
from cogs.MusicBot import getLastSong
from util import config

lg = logging.getLogger(__name__[5:])


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


class GeniusAPI_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="lyrics")
    @commands.has_role(config.getBotMusicRole())
    async def lyrics(self, ctx, *args):
        if not args:
            last_song = await getLastSong()
            title = last_song.title()
            title = str(title).replace("(Official Video)", "").replace("(Lyric Video)", "")
            #channel = await last_song.channel()
            args = title  # + channel
        lg.info(args)
        convertTuple = lambda tup: str(tup).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
        msg = convertTuple(args)
        genius = lyricsgenius.Genius(config.getGeniusKey())
        genius_yellow = config.getDiscordColour("genius_yellow")
        with HiddenPrints():
            song = genius.search_song(msg)
            lyric = song.lyrics

        infoEmbed = discord.Embed(colour=config.getDiscordColour("genius_yellow"))
        infoEmbed.set_author(name=song.title)#, icon_url=song.song_art_image_url)

        parts = text.split( lyric, numbers.find_lowest_under(len_text=len(lyric)))

        for part in parts:
            embed = discord.Embed(description=part, colour=genius_yellow)
            await ctx.send(embed=embed)


def setup(bot):

    bot.add_cog(GeniusAPI_Handler(bot))

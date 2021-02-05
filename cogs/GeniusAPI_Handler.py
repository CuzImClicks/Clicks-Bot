import logging
from attr import __description__
import discord
from discord.ext import commands
import lyricsgenius
from util.logger import path
import logging
from util import config
import datetime
from aiohttp import ClientSession
import json
import lyricsgenius

lg = logging.getLogger(__name__[5:])

import os, sys

class HiddenPrints:
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
        convertTuple = lambda tup: str(tup).replace("(", "").replace("'", "").replace(")", "").replace(",", "")
        msg = convertTuple(args)
        genius = lyricsgenius.Genius(config.getGeniusKey())
        with HiddenPrints():
            song = genius.search_song(msg)
            lyric = song.lyrics

        infoEmbed = discord.Embed(title=f"Lyrics of '{song.title}'",
        description=f"Lyrics are provided by genius.com")
        first_half = lyric[:int(len(lyric)/2)]
        second_half = lyric[int(len(lyric)/2):]
        infoEmbed.add_field(name="Lyrics", value=first_half)
        await ctx.send(embed=infoEmbed)
        secondEmbed = discord.Embed(description=second_half)
        await ctx.send(embed=secondEmbed)


def setup(bot):

    bot.add_cog(GeniusAPI_Handler(bot))

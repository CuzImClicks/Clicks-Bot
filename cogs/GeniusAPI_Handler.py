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
import numpy

lg = logging.getLogger(__name__[5:])

import os, sys

def split(sentence, num_chunks):
    """Split the given sentence into num_chunk pieces.

    If the length of the sentence is not exactly divisible by
    num_chunks, some slices will be 1 character shorter than
    the others.
    https://codereview.stackexchange.com/questions/145489/slicing-a-string-into-three-pieces-and-also-controlling-manipulating-through-lo
    """

    size, remainder = divmod(len(sentence), num_chunks)
    chunks_sizes = [size + 1] * remainder + [size] * (num_chunks - remainder)
    offsets = [sum(chunks_sizes[:i]) for i in range(len(chunks_sizes))]

    return [sentence[o:o+s] for o, s in zip(offsets, chunks_sizes)]

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
        genius_yellow = config.getDiscordColour("genius_yellow")
        with HiddenPrints():
            song = genius.search_song(msg)
            lyric = song.lyrics

        infoEmbed = discord.Embed(colour=config.getDiscordColour("genius_yellow"))
        infoEmbed.set_author(name=f"[{song.title}]({song.url})", icon_url=song.song_art_image_url)
        parts = split(lyric, 3)

        for part in parts:
            embed = discord.Embed(description=part, colour=genius_yellow)
            await ctx.send(embed=embed)

def setup(bot):

    bot.add_cog(GeniusAPI_Handler(bot))

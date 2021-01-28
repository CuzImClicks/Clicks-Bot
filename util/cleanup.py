import os
from clicks_util import file_io
from clicks_util import logger
import logging

lg = logging.getLogger(__name__[5:])


async def remove_songs():
    for song in os.listdir(os.getcwd()):

        if song.endswith(".webm"):
            lg.info(f"Removing the file of {song[:-5]}")

            file_io.remove(f"{os.getcwd()}/{song}")



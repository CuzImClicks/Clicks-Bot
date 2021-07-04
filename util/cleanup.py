import logging
import os

from clicks_util import file_io

lg = logging.getLogger(__name__[5:])


def remove_songs():
    # Removes all files created by the music bot ending on .webm or .m4a
    for song in os.listdir(os.getcwd()):

        if song.endswith(".webm") or song.endswith(".m4a"):
            lg.info(f"Removing the file of {song[:-5]}")

            file_io.remove(f"{os.getcwd()}/{song}")


def remove_song(name: str):
    # Removes a specific file created by the music bot ending on .webm or .m4a
    for song in os.listdir(os.getcwd()):

        if (song.endswith(".webm") or song.endswith(".m4a")) and song.__contains__(name):
            lg.info(f"Removing the file of {song[:-5]}")

            file_io.remove(f"{os.getcwd()}/{song}")


def remove_hypixel_jsons():
    for file in os.listdir(os.getcwd()+"/hypixel"):
        lg.info(f"Removing the file {file[:-5]}")
        file_io.remove(f"{os.getcwd()}/hypixel/{file}")


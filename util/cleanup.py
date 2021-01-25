import os
from clicks_util import file_io


def remove_songs():
    for song in os.listdir(".."):
        if song.endswith(".webm") or song.endswith(".m4a"):
            print(song)
            file_io.remove(f"../{song}")



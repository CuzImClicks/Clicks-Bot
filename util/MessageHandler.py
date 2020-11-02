import logging
import discord
import os
from util import config

path = os.getcwd()

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\chat.log")
fl.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl.setFormatter(fmt)

lg.addHandler(fl)


async def log(msg):

    lg.info(f"[{msg.author}] - {msg.content}")


async def send_back(msg):

    await msg.channel.send(f"This is a test message!")
    lg.info(f"Sent message to {str(msg.channel)} containing 'This is a test message!'")
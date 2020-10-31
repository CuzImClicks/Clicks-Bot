import logging
import discord

lg = logging.getLogger(__name__)


async def log(msg):

    lg.info(f"[{msg.author}] - {msg.content}")


async def send_back(msg):

    await msg.channel.send(f"This is a test message!")
    lg.info(f"Sent message to {str(msg.channel)} containing 'This is a test message!'")
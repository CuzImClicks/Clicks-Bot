import logging
from util import config
from util.embed import send_embed
from util.logger import *

path = os.getcwd()

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}/logs/chat.log")
fl.setLevel(config.getFileLoggingLevel())
fmt = logging.Formatter("[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
fl.setFormatter(fmt)

lg.addHandler(fl)

#A new send command that makes sending embeds easier
#TODO: Convert all ctx.send to this function
async def send(ctx, title, description, content):

    await send_embed(ctx=ctx, infos=(title, description), values=(content,), inline=False)


async def log(msg):

    lg.info(f"[{msg.author}] - {msg.content}")


async def send_back(msg):

    await msg.channel.send(f"This is a test message!", delete_after=5)
    lg.info(f"Sent message to {str(msg.channel)} containing 'This is a test message!'")

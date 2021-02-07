import logging

from discord import colour
from clicks_util import json_util
import os
import discord

path = str(os.getcwd())

lg = logging.getLogger(__name__[5:])

jf = json_util.JsonFile("config.json", f"{path}/util")
data = jf.read()
boolean_settings = ["magmaboss", "hypixel_online"]
changeable_settings = ["command_prefix", "status"]

def enable(feature: str) -> bool:
    if feature not in boolean_settings:
        return False
    data[feature] = True
    lg.info(f"Enabled feature '{feature}' and wrote the change to the config file")
    jf.write(data)
    return True

def disable(feature: str) -> bool:
    if feature not in boolean_settings:
        return False
    data[feature] = False
    lg.info(f"Disabled feature '{feature}' and wrote the change to to the config file")
    jf.write(data)
    return True

def toggle(feature: str) -> bool:
    if feature not in boolean_settings:
        return False
    data[feature] = not data[feature]
    lg.info(f"Toggled feature '{feature}' and wrote the change to the config file")
    jf.write(data)
    return True

def change(feature: str, new_value) -> bool:
    if feature not in changeable_settings:
        return False
    old_value = data[feature]
    data[feature] = new_value
    lg.info(f"Changed value of feature '{feature}' from {old_value} to {new_value}")
    jf.write(data)
    return True


def getLoggingLevel():
    level = data["level"]

    if level.upper() == "INFO":

        return logging.INFO

    elif level.upper() == "WARNING":

        return logging.WARNING

    elif level.upper() == "DEBUG":

        return logging.DEBUG

    elif level.upper() == "ERROR":

        return logging.ERROR


def getFileLoggingLevel():
    flevel = data["file_level"]

    if flevel.upper() == "INFO":

        return logging.INFO

    elif flevel.upper() == "WARNING":

        return logging.WARNING

    elif flevel.upper() == "DEBUG":

        return logging.DEBUG

    elif flevel.upper() == "ERROR":

        return logging.ERROR


def getToken():
    return data["token"]


def getCommandPrefix():
    return data["command_prefix"]


def getStatus():
    return data["status"]


def getBotAccessRole():
    return data["Bot Access Role"]


def getBotAdminRole():
    return data["Bot Admin Role"]


def getBotMusicRole():
    return data["Bot Music Role"]


def getHypixelKey():
    return data["hypixel_key"]


def getSteamKey():
    return data["steam_key"]


def getGeniusKey():
    return data["genius_key"]


def getDiscordColour(colourname):
    if colourname == "red":
        return discord.Colour(0x9D1309)

    elif colourname == "blue":
        return discord.Colour(0x000030)

    elif colourname == "green":
        return discord.Colour(0x0BAF07)

    elif colourname == "genius_yellow":
        return discord.Colour(0xffff64)


def getPiHoleIp() -> str:
    return data["pihole_ip"]


def getMagmaboss() -> bool:
    return data["magmaboss"]


def getHypixelOnline() -> bool:
    return data["hypixel_online"]

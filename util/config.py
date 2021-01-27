import logging
from clicks_util import json_util
import os
import discord

path = str(os.getcwd())


jf = json_util.JsonFile("config.json", f"{path}/util")


def getLoggingLevel():

    level = jf.read()["level"]

    if level.upper() == "INFO":

        return logging.INFO

    elif "WARNING":

        return logging.WARNING

    elif "DEBUG":

        return logging.DEBUG

    elif "ERROR":

        return logging.ERROR


def getFileLoggingLevel():

    flevel = jf.read()["file_level"]

    if flevel.upper() == "INFO":

        return logging.INFO

    elif "WARNING":

        return logging.WARNING

    elif "DEBUG":

        return logging.DEBUG

    elif "ERROR":

        return logging.ERROR


def getToken():

    return jf.read()["token"]


def getCommandPrefix():

    return jf.read()["command_prefix"]


def getStatus():

    return jf.read()["status"]


def getBotAccessRole():

    return jf.read()["Bot Access Role"]


def getBotAdminRole():

    return jf.read()["Bot Admin Role"]


def getDefaultRole():

    return jf.read()["Default Role"]

def getKey():

    return jf.read()["key"]

def getSteamKey():

    return jf.read()["steam_key"]

def getDiscordColour(colourname):

    if colourname == "red":
        return discord.Colour(0x9D1309)

    elif colourname == "blue":
        return discord.Colour(0x000030)
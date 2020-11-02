from configparser import ConfigParser
import logging
from clicks_util import json_util

'''file = 'config.ini'
config = ConfigParser()
config.read(file)'''

jf = json_util.json_file("config.json", "D:/GitHub Repos/Clicks-Bot/util")



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

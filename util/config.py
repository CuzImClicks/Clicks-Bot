import logging
from clicks_util import json_util
import os

path = os.getcwd()

jf = json_util.json_file("config.json", f"{path}/util")


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

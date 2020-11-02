from configparser import ConfigParser
import logging

file = '../config.ini'
config = ConfigParser()
config.read(file)


def getLoggingLevel():

    level = config.get("options_logging", "level")

    if level.upper() == "INFO":

        return logging.INFO

    elif "WARNING":

        return logging.WARNING

    elif "DEBUG":

        return logging.DEBUG

    elif "ERROR":

        return logging.ERROR


def getFileLoggingLevel():

    flevel = config.get("options_logging", "file_level")

    if flevel.upper() == "INFO":

        return logging.INFO

    elif "WARNING":

        return logging.WARNING

    elif "DEBUG":

        return logging.DEBUG

    elif "ERROR":

        return logging.ERROR


def getToken():

    return config.get("token", "token")
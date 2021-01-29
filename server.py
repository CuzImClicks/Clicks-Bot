from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from web_server.database import *
from clicks_util import logger
from PIL import Image
import asyncio
import logging
from util.hypixel.player import Player

server = FastAPI()

lg = logging.getLogger(__name__)


@server.get("/")
async def index():
    return {"message": "Clicks Bot API"}


@server.get("/api", status_code=status.HTTP_200_OK)
async def api(key: str = ""):
    key_valid = check_key(key)
    lg.info(key_valid)
    return {"key": key_valid}


@server.get("/api/assets/steam_icon")
async def steam_icon(key: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        return FileResponse(f"{os.getcwd()}/assets/steam_icon.jpg")


@server.get("/api/assets/Clicks-Bot_API")
async def steam_icon(key: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        return FileResponse(f"{os.getcwd()}/assets/Clicks-Bot API.jpg")


@server.get("/api/Hypixel")
async def hypixel(key: str = "", username: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        pl = Player(username)

        return pl.data


@server.get("/api/Hypixel/SkyBlock")
async def hypixel(key: str = "", username: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        pl = Player(username)

        return pl.skyblock.profiles


@server.get("/api/steam")
async def steam(key: str = "", username: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        lg.info(os.getcwd())

        data = json.load(open(f"{os.getcwd()}/steam/users.json"))
        if username in data.keys():
            return data[username]

        else:
            return status.HTTP_204_NO_CONTENT


from fastapi import FastAPI, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from web_server.database import *
from clicks_util import logger
from PIL import Image
import asyncio
import logging
from util.hypixel.player import Player
from util.hypixel.hypixel_server import Hypixel
import qrcode
from util.steam.user import User
from lyricsgenius import Genius
from util import config

server = FastAPI()

#uvicorn server:server --host 127.0.0.1 --port 5000
#can't be executed with os.popen()

lg = logging.getLogger("Server")

@server.get("/")
async def index():
    return RedirectResponse("/docs")


@server.get("/api", status_code=status.HTTP_200_OK)
async def api(key: str = ""):
    key_valid = check_key(key)
    lg.info(key_valid)
    return JSONResponse(status_code=200, content={"key": key_valid})


@server.get("/api/assets/steam_icon")
async def steam_icon(key: str = ""):
    if not check_key(key):
        return status.HTTP_401_UNAUTHORIZED

    else:
        return FileResponse(f"{os.getcwd()}/assets/steam_icon.jpg")


@server.get("/api/assets/Clicks-Bot_API")
async def clicks_bot_api_image(key: str = ""):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        return FileResponse(f"{os.getcwd()}/assets/Clicks-Bot API.jpg")


@server.get("/api/Hypixel")
async def hypixel(key: str = "", username: str = ""):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        pl = Player(username)

        return JSONResponse(status_code=200, content=pl.data)

@server.get("/api/Hypixel/WatchDog")
async def hypixel_watchdog(key: str = ""):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")
    
    else:
        return JSONResponse(status_code=200, content=await Hypixel.watchdog())


@server.get("/api/Hypixel/SkyBlock")
async def skyblock(key: str = "", username: str = ""):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        pl = Player(username)
        msg = {"profiles": [pl.skyblock.profiles[profile].data_profile for profile in list(pl.skyblock.profiles.keys())]}
        return JSONResponse(status_code=200, content=msg)

@server.get("/api/Hypixel/SkyBlock/User/")
async def skyblock_user(key: str = "", username: str = "", value: str = ""):
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        pl = Player(username)
        profile = pl.skyblock.profiles[list(pl.skyblock.profiles.keys())[0]]
        user = profile.user
        print(vars(user))
        if value in list(user.__dict__.keys()): #FIXME: doesnt return the right variables -> always False
            return JSONResponse(status_code=200, content={value: dict(user)[value]})

        else:
            #FIXME: TypeError: Object of type Stats is not JSON serializable
            return JSONResponse(status_code=404, content=user.__dict__)

@server.get("/api/Hypixel/SkyBlock/User/Stats")
async def skyblock_user_stats(key: str = "", username: str = ""):
    
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        pl = Player(username)
        profile = pl.skyblock.profiles[list(pl.skyblock.profiles.keys())[0]]

        return JSONResponse(status_code=200, content={"stats": dict(profile.user.stats.__dict__())})

@server.get("/api/steam")
async def steam(key: str = "", username: str = "", steam_id: int =0):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        lg.info(os.getcwd())

        data = json.load(open(f"{os.getcwd()}/steam/users.json"))
        if username in data.keys():
            return JSONResponse(status_code=200, content=data[username])

        elif steam_id:
            return JSONResponse(status_code=200, content=User(steam_id).__dict__())

        else:
            return JSONResponse(status_code=204, content="Invalid key")

@server.get("/api/qr_code")
async def qr_code(key: str = "", content: str = "", version: int = 1):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        qr = qrcode.QRCode(version=version, border=2, error_correction=qrcode.ERROR_CORRECT_L)
        qr.add_data(content)
        qr.make()

        img = qr.make_image()
        img.save(f"{os.getcwd()}/qr_codes/qr.png")

        return FileResponse(f"{os.getcwd()}/qr_codes/qr.png")

@server.get("/api/lyrics")
async def lyrics(key: str="", song_name: str=""):
    if not check_key(key):
        return JSONResponse(status_code=401, content="Invalid key")

    else:
        genuis = Genius(config.getGeniusKey())
        song = genuis.search_song(song_name)
        if song == None:
            return JSONResponse(status_code=204, content={"success": False, "error": {""}})
        return JSONResponse(status_code=200, content={"success": True, song_name: song.lyrics})

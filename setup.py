import subprocess
import sys


def get_python_version():
    """get the current python version"""
    return float(f"{sys.version_info.major}.{sys.version_info.minor}")


def install(package):
    """install a python package"""
    subprocess.check_call(["python", "-m", "pip", "install", package])  # windows
    #subprocess.check_call([f"python{get_python_version()}", "-m", "pip", "install", package])  # linux


packages = ["discord", "youtube-dl", "ffmpeg-python", "aiohttp", "aiofiles", "mojang", "qrcode", "varname"]

for package in packages:
    install(package)

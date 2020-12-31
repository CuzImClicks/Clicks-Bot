import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executeable, "-m", "pip", "install", package])

packages = ["discord", "youtube-dl", "ffmpeg-python"]

for package in packages:
    install(package)

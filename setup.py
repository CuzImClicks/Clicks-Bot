import subprocess


def install(package):
    subprocess.check_call(["python", "-m", "pip", "install", package])


packages = ["discord", "youtube-dl", "ffmpeg-python"]

for package in packages:
    install(package)

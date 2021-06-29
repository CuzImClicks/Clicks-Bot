import os

while True:
    try:
        os.system("git pull")
        os.system("python ClicksBot.py")

    except Exception as e:
        print(e)

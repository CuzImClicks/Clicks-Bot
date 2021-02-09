from exceptions import RestartException
import os
import time
import datetime

#https://github.com/The-Coding-Academy/Coding-Academy-Bot/blob/master/auto.py

while True:
    try:
        os.system("python ClicksBot.py")

    except KeyboardInterrupt:
        break

    except RestartException:
        pass

    except Exception as e:
        print(f"An excption occured preventing restart: {e}")
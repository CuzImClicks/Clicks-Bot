from datetime import datetime
from dateutil import tz

#https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime

# METHOD 2: Auto-detect zones:
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

utc = datetime.utcnow()

# Tell the datetime object that it's in UTC time zone since 
# datetime objects are 'naive' by default
utc = utc.replace(tzinfo=from_zone)

# Convert time zone
timezone = utc.astimezone(to_zone)

def getTime() -> str:
    #FIXME: returns utc time
    return str(utc.now())[:-7].split(" ")[1]

def getDateAndTime() -> str:
    return str(utc.now())[:-7]

def timefromtimestamp(timestamp: int) -> str:
    return str(utc.fromtimestamp(timestamp/1000).time())[:-7]

def datefromtimestamp(timestamp: int) -> str:
    return str(utc.fromtimestamp(timestamp/1000).date())

def fulldatefromtimestamp(timestamp: int) -> str:
    return str(utc.fromtimestamp(timestamp/1000).now())[:-7]

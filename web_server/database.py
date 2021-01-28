import json
from clicks_util.json_util import JsonFile
import os
import random
import string

jf = JsonFile("keys.json", path=os.getcwd()+"/web_server")


def get_random_string(length):
    
    letters = string.ascii_letters
    result = "".join(random.choice(letters) for i in range(length))
    return result


def create_key(username):
    
    data = jf.read()
    key = get_random_string(10)
    data[username] = key

    jf.write(data)
    return key


def check_key(key):

    if compare_key(key):
        print(True)
        return True

    else:
        return False


def compare_key(key2):
    for key in jf.read().values():
        if key == key2:
            return True

    return False

    
def get_key(username):
    
    data = jf.read()
    if username in data.keys():
        return data[username]
    
    else:
        return False
    
    
def check_for_key(username):
    data = jf.read()
    print(list(data.values()))
    if username in list(data.values()):
        print(True)
        return True
    
    else:
        return False
    
    
    


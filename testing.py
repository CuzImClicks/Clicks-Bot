from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)

print(str(config.get("options_logging", "level")))
print(config.sections())
'''
config["token"] = {"token": "NzcxNDY5NDA1NTM1MjA3NDY1.X5sk3w.MEioKKBdRJ319WErZoCZ4edZo8Q"}
config["command_prefix"] = {"command_prefix": "$"}
config["logging"] = {"formatter": r"[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s"}

with open(file, "w+") as f:

    config.write(f)
'''

'''
[token]
token = NzcxNDY5NDA1NTM1MjA3NDY1.X5sk3w.MEioKKBdRJ319WErZoCZ4edZo8Q

[command_prefix]
command_prefix = $

[logging]
formatter = [%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s
datefmt = %H:%M:%S
'''

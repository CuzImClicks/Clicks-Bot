'''
Created on 28.10.2020

@author: bruno
'''

import logging
import colorama

colorama.init()

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] - %(name)s - [%(levelname)s]: %(message)s"+colorama.Fore.RESET, datefmt="%H:%M:%S")

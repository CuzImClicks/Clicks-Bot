'''
Findet die Quwurzeldrwurzeltwurzel von der eingebenen Nummer und returnt diese

'''
import logger
import logging

lg = logging.getLogger(__name__)

def iterations(wurzel):

    b = 2

    while True:

        previous_b = round(b, 2)

        b = 0.5*(b+wurzel/b)
        
        lg.info(b)

        if round(b, 2) == previous_b:

            return b

            break

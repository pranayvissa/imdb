#!/usr/bin/env python

import sys
import logging
import datetime
import traceback

# The Class that will replace the asctime with what this generates, aka
# microsecond

class MyFormatter(logging.Formatter):
    _converter = datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self._converter(record.created)
        if datefmt:
            stamp = ct.strftime(datefmt)
        else:
            tm = ct.strftime("%Y-%m-%d %H:%M:%S")
            stamp = "%s.%03d" % (tm, record.msecs)
        return stamp

# Create the logget
logger = logging.getLogger('imdb')

if not len(logger.handlers):
    # Setup the correct formatter
    console = logging.StreamHandler(sys.stdout)
    FORMAT = '%(asctime)s: %(levelname)8s: %(message)s'
    formatter = MyFormatter(fmt=FORMAT, datefmt='%Y-%m-%d %H:%M:%S.%f')
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)      # Default level

# Create the helper function
INFO  = logger.info
DEBUG = logger.debug
CRIT  = logger.critical
WARN  = logger.warning

# Print the details of the last exception
def printExeptionDetails():
    type, value, tb = sys.exc_info()
    WARN("Exception: Type: " + str(type) + ", Traceback : " + traceback.format_exc())

def addFileHandler(filename):
    if filename is None:
        return

    logger = logging.getLogger('imdb')

    # Add line separator
    with open(filename, 'a+') as fh:
        fh.write(">>>>>>>>>>>>NEW IMDB OUTPUT STARTS<<<<<<<<<<<<<<\n\n")
        fh.close()

    filehandler = logging.FileHandler(filename, mode='a')
    FORMAT = '%(asctime)s: %(levelname)8s: %(message)s'
    formatter = MyFormatter(fmt=FORMAT, datefmt='%Y-%m-%d %H:%M:%S.%f')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)

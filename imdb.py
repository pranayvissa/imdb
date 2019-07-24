#!/usr/bin/python

import os
import sys
import inspect
import imp
import fnmatch
import argparse

scriptDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir+"/inc")

from Log import (printExeptionDetails, logger, logging)
from BaseModule import BaseModule

plugins = None

# Return a list of all plugins
def load_plugins():
    global plugins

    pluginDir = scriptDir + "/plugins/"
    plugins = {}

    # Load plugins
    for root, _, filenames in os.walk(pluginDir):
        for filename in fnmatch.filter(filenames, '*.py'):
            fname = os.path.join(root, filename)
            p = imp.load_source('Plugin' , fname)
            classes = inspect.getmembers(p, inspect.isclass)
            for cname, cls in classes:
                if BaseModule in cls.__bases__:
                    plugins[cname] = cls()

    return plugins


# Our main function
def main(args):
    global plugins
    rc = 0
    try:
        # Execute the action function of all plugins
        for cname, plugin in plugins.iteritems():
            rc = plugin.action(args)
            if rc != 0:
                break
    except:
        printExeptionDetails()
        os._exit(1)
    pass

    return rc


if __name__ == '__main__':

    global plugins
    rc = 0

    try:
        plugins = load_plugins()

        # Create a parser Object
        parser = argparse.ArgumentParser(
            description="Innovium - Automated Switch Management (iSwitch)",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # Load plugins, as they provide extensible args
        for cname, plugin in plugins.iteritems():
            plugin.add_args(parser)

        parser.add_argument('--title', dest='title', default=None, required=True,
            help='Movie/show title')
        parser.add_argument('--year', dest='year', default=None,
            help='Release year')
        parser.add_argument('--id', dest='id', default=None,
            help='IMDB ID')
        parser.add_argument('--insert_watched', dest='insert_watched', default=None,
            action='store_true', help='Insert watched data into DB')
        parser.add_argument('--ignore_watched', dest='insert_watched', default=False,
            action='store_true', help='Ignore watched stuff from DB')
        parser.add_argument('--quiet', dest='quiet', default=None,
            help='Quiet mode')
        parser.add_argument('--verbose', dest='verbose', default=None,
            help='Verbose mode')

        args = parser.parse_args()

        # Set logging level
        logger.setLevel(logging.INFO)
        if args.quiet:
            logger.setLevel(logging.ERROR)
        if args.verbose:
            logger.setLevel(logging.DEBUG)

        rc = main(args)

    except SystemError:
        pass

    except:
        printExeptionDetails()
        os._exit(1)

    os._exit(rc)


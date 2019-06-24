#!/usr/bin/python

from BaseModule import BaseModule

class Shows(BaseModule):
    def __init__(self):
        pass

    def add_args(self, parser):
        parser.add_argument('--season', dest='season', default=None,
                            help='Season No.')

    def action(self, args):
        pass

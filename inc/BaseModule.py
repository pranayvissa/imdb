#!/usr/bin/python

import omdb
from DB import DB

class BaseModule:
    def __init__(self):
        # Set up basic omdb library
        self.api_key = '57f4b0ed'
        omdb.set_default('apikey', self.api_key)

        self.omdb_client = omdb.OMDBClient(apikey=self.api_key)

        self.main_url = 'http://www.omdbapi.com/?apikey=%s&' % (self.api_key)

        self.db = DB()

    def add_args(self, parser):
        raise NotImplementedError("Subclass to implement add_args()")


    def action(self, args):
        raise NotImplementedError("Subclass to implement action()")

#!/usr/bin/python

import requests
from BaseModule import BaseModule


class Shows(BaseModule):

    def __init__(self):
        BaseModule.__init__(self)
        self.title = None
        self.num_seasons = 0
        self.info = {}
        self.year = ''
        self.season_rating = {}


    def add_args(self, parser):
        parser.add_argument('--season', dest='season', default=None,
                            help='Season No.')


    def action(self, args):
        self.title = args.title
        if args.season is None:
            url = self.main_url+"t=%s" % (self.title)
            rsp = requests.get(url)
            self.info = rsp.json()
            self.num_seasons = int(self.info['totalSeasons'])
            self.year = self.info['Year']
            self._get_seasons_info()
        else:
            self._get_season_info(self, args.season)


    def _get_info_for_all_seasons(self):
        self.info['Seasons'] = {}
        num_seasons = int(self.info['totalSeasons'])
        for num_season in range(1, (num_seasons+1)):
            url = self.main_url+"t=%s&season=%s" % (self.title, num_season)
            rsp = requests.get(url)
            self.info['Seasons'][num_season] = rsp.json()


    def _get_season_info(self, season):
        self.info['Seasons'] = {}
        self.info['Seasons'][season] = {}
        url = self.main_url+"t=%s&season=%s" % (self.title, season)
        rsp = requests.get(url)
        self.info['Seasons'][season] = rsp.json()


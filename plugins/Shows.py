#!/usr/bin/python

import requests

from BaseModule import BaseModule
from Log import (INFO)


class Shows(BaseModule):

    def __init__(self):
        BaseModule.__init__(self)
        self.title = None
        self.num_seasons = 0
        self.info = {}
        self.year = ''
        self.season_rating = {}
        self.ratings = {}

        self.user = 'Pranay Vissa'

        self.top_rated_shows = {}


    def add_args(self, parser):
        '''
        Argument parser for this plugin
        '''

        parser.add_argument('--season', dest='season', default=None, type=int,
                            help='Season No.')
        parser.add_argument('--episode', dest='episode', default=None, type=int,
                            help='Episode No.')
        parser.add_argument('--top', dest='top', default=1,
                            help='Best episode')


    def action(self, args):
        '''
        Actions taken by this plugin
        '''

        rc = 0
        self.title = args.title

        # Get show info
        if args.season is None:
            url = self.main_url+"t=%s" % (self.title)
            rsp = requests.get(url)
            self.info = rsp.json()
            self.num_seasons = int(self.info['totalSeasons'])
            self.year = self.info['Year']
            self.get_info_for_all_seasons()
        else:
            self.get_season_info(args.season, args.episode)

        if args.insert_watched:
            season = int(args.season)
            ep_indx = int(args.episode)-1
            info = self.info['Seasons'][season]['Episodes'][ep_indx]

            episode = int(info['Episode'])

            # Get show id
            condition = "`show_title` LIKE \"%s\" AND `season`=%d AND `episode`=%d" % (self.title, season, episode)
            show_id = self.db.get_id("Shows", condition)
            record = {}
            record['fk_show_id'] = str(show_id)
            record['show_title'] = self.title
            record['season'] = str(season)
            record['episode'] = str(episode)
            record['imdb_id'] = info['imdbID']

            self.db.insert_row('ShowsWatched', record)

            return rc

        # Get top rated show(s)
        #self.get_top_rated_shows(args.top)

        return rc


    def get_info_for_all_seasons(self):
        '''
        Get IMDB info for all seasons and store it
        '''

        self.info['Seasons'] = {}
        num_seasons = int(self.info['totalSeasons'])
        for num_season in range(1, (num_seasons+1)):
            url = self.main_url+"t=%s&season=%s" % (self.title, num_season)
            rsp = requests.get(url)
            self.info['Seasons'][num_season] = rsp.json()

            # Insert stat into DB
            episodes = self.info['Seasons'][num_season]['Episodes']
            for episode in episodes:
                record = {}
                record['show_title'] = self.info['Title']
                record['season'] = str(num_season)
                record['episode'] = episode['Episode']
                record['episode_title'] = episode['Title']
                record['rating'] = episode['imdbRating']
                record['imdb_id'] = episode['imdbID']
                record['release_date'] = episode['Released']

                self.db.insert_row('Shows', record)


    def get_season_info(self, season, ep):
        '''
        Get info for this season (and episode if given)
        '''

        self.info['Seasons'] = {}
        self.info['Seasons'][season] = {}
        url = self.main_url+"t=%s&season=%s" % (self.title, season)
        rsp = requests.get(url)
        self.info['Seasons'][season] = rsp.json()
        episodes = self.info['Seasons'][season]['Episodes']
        self.info['Title'] = self.title


        if ep is not None:
            episodes = self.info['Seasons'][season]['Episodes']
            for episode in episodes:
                record = {}
                record['show_title'] = self.info['Title']
                record['season'] = str(season)
                record['episode'] = episode['Episode']
                record['episode_title'] = episode['Title']
                record['rating'] = episode['imdbRating']
                record['imdb_id'] = episode['imdbID']
                record['release_date'] = episode['Released']

                self.db.insert_row('Shows', record)
        else:
            for episode in episodes:
                if int(episode['Episode']) == int(ep):
                    record = {}
                    record['show_title'] = self.info['Title']
                    record['season'] = str(season)
                    record['episode'] = episode['Episode']
                    record['episode_title'] = episode['Title']
                    record['rating'] = episode['imdbRating']
                    record['imdb_id'] = episode['imdbID']
                    record['release_date'] = episode['Released']

                    self.db.insert_row('Shows', record)


    def get_top_rated_shows(self, top):
        ''' Get top rated shows based off imdb ratings '''

        INFO("xxx")

        for season in self.info['Seasons']:
            episodes = self.info['Seasons'][season]['Episodes']
            for episode in episodes:
                rating = episode['imdbRating']
                title = self.info['Title']
                season = str(season)
                ep = episode['Episode']
                show_info = (title, season, ep)

                if rating in self.top_rated_shows:
                    self.top_rated_shows[rating].append(show_info)
                else:
                    self.top_rated_shows[rating] = [show_info]

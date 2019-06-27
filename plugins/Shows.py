#!/usr/bin/python

import requests
import os
from BaseModule import BaseModule
from Log import (CRIT, INFO)


class Shows(BaseModule):

    def __init__(self):
        BaseModule.__init__(self)
        self.title = None
        self.num_seasons = 0
        self.info = {}
        self.year = ''
        self.season_rating = {}
        self.ratings = {}
        self.num_best = 10   # Pick 10 best by default


    def add_args(self, parser):
        parser.add_argument('--season', dest='season', default=None,
                            help='Season No.')
        parser.add_argument('--num_best', dest='num_best', default=None,
                            help='Season No.')


    def action(self, args):
        rc = 0
        self.title = args.title

        if args.num_best is None:
            num_best = 10
        else:
            num_best = int(args.num_best)

        if args.season is None:
            url = self.main_url+"t=%s" % (self.title)
            rsp = requests.get(url)
            self.info = rsp.json()
            self.num_seasons = int(self.info['totalSeasons'])
            self.year = self.info['Year']
            self.get_info_for_all_seasons()
        else:
            self.get_season_info(self, args.season)

        self.get_episode_rating()

        top_rated = self.get_top_rated_episodes(num_best)
        self.print_shows(top_rated)

        return rc


    def get_info_for_all_seasons(self):
        self.info['Seasons'] = {}
        num_seasons = int(self.info['totalSeasons'])
        for num_season in range(1, (num_seasons+1)):
            url = self.main_url+"t=%s&season=%s" % (self.title, num_season)
            rsp = requests.get(url)
            self.info['Seasons'][num_season] = rsp.json()


    def get_season_info(self, season):
        self.info['Seasons'] = {}
        self.info['Seasons'][season] = {}
        url = self.main_url+"t=%s&season=%s" % (self.title, season)
        rsp = requests.get(url)
        self.info['Seasons'][season] = rsp.json()


    def get_episode_rating(self):
        seasons = self.info['Seasons']
        for num_season in seasons:
            season = seasons[num_season]
            all_episodes = season['Episodes']
            num_episodes = len(all_episodes)

            for num_episode in range(num_episodes):
                episode = all_episodes[num_episode]
                rating = float(episode['imdbRating'])
                name = episode['Title']
                ep = episode['Episode']

                ep_info = (name, ep, num_season, rating)

                if rating in self.ratings:
                    self.ratings[rating].append(ep_info)
                else:
                    self.ratings[rating] = []
                    self.ratings[rating].append(ep_info)


    def get_top_rated_episodes(self, num):
        ratings = self.ratings.keys()
        if len(ratings) == 0:
            CRIT("No ratings defined")
            os._exit(1)

        ratings.sort(reverse=True)
        cnt = 0
        best_shows = []
        rindx = 0

        while (cnt < num):
            shows = self.ratings[ratings[rindx]]
            num_shows = len(shows)
            for i in range(num_shows):
                if cnt >= num:
                    break

                best_shows.append(shows[i])
                cnt = cnt + 1

            rindx += 1

        if len(best_shows) != num:
            CRIT("Internal Error. Shows more than requested for")
            os._exit(1)

        return best_shows


    def print_shows(self, shows):
        num_shows = len(shows)
        if num_shows == 0:
            CRIT("No shows defined")
            os._exit(1)

        INFO("Here are the top %d shows" % num_shows)
        INFO("    Season, Episode, Title, Rating")
        for show in shows:
            name = show[0]
            episode = show[1]
            season = show[2]
            rating = show[3]
            INFO("    %s, %s, %s, %s" % (season, episode, name, rating))











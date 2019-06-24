#!/usr/bin/python

import omdb
import requests
import argparse

API_KEY = '57f4b0ed'
omdb.set_default('apikey', API_KEY)

parser = argparse.ArgumentParser(description='IMDB loookup', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--title',dest='title')
parser.add_argument('--season',dest='season')
parser.add_argument('--year',dest='year')
args = parser.parse_args()

client = omdb.OMDBClient(apikey=API_KEY)

movie = args.title
year = args.year

info = omdb.get(title=movie,year=year)

score = info['metascore']
imdb_votes = info['imdb_votes']
imdb_rating = info['imdb_rating']
cast = info['actors']
runtime = info['runtime']
imdb_id = info['imdb_id']
num_seasons = int(info['total_seasons'])


# Print Movie Info
print "Movie: %s" % movie
print "    Metascore: %s" % score
print "    Votes: %s" % imdb_votes
print "    Rating: %s" % imdb_rating
print "    Cast: %s" % cast
print "    Runtime %s" % runtime


# https://www.imdb.com/title/tt0106004/episodes?season=3&ref_=tt_eps_sn_3
# http://www.omdbapi.com/?apikey=57f4b0ed&t=Frasier&y=1993&season=3
url = 'http://www.omdbapi.com/?apikey=%s&' % (API_KEY)

for season in range(1, (num_seasons+1)):
    seasonUrl = url + 't=%s&y=%s&season=%s' % (movie, year, season)
    rsp = requests.get(url=seasonUrl)
    data = rsp.json()



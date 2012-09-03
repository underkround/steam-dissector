import pymongo
import ConfigParser
from copy import copy
from time import time

class Statistics(object):
    
    def __init__(self):
        cfg = ConfigParser.RawConfigParser()
        cfg.read('config.cfg')
        connString = cfg.get('MongoDB', 'connectionString')
        
        self.connection = pymongo.Connection(connString)
        self.db = self.connection['steam-dissector']
        self.stats_profiles = self.db.stats_profiles
        self.stats_games_for_profiles = self.db.stats_games_for_profiles
        self.stats_games = self.db.stats_games


    def putUser(self, user):
        u = copy(user)
        u['timestamp'] = time()
        self.stats_profiles.insert(u)


    def putGamesForUser(self, userId, games):
        self.stats_games_for_profiles.insert({ 'userId': userId, 'timestamp': time(), 'games': games })


    def detailsFetched(self, gameId):
        self.stats_games.insert({ 'gameId': gameId, 'timestamp': time() })


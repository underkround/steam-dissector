import pymongo
import ConfigParser

class Cache(object):
    
    def __init__(self):
        cfg = ConfigParser.RawConfigParser()
        cfg.read('config.cfg')
        connString = cfg.get('MongoDB', 'connectionString')
        
        self.connection = pymongo.Connection(connString)
        self.db = self.connection['steam-dissector']
        self.games = self.db.games
        self.games.ensure_index('id')


    def clear(self):
        self.games.remove({})


    def putGame(self, game):
        return self.games.insert(game)


    def getGame(self, gameId):
        return self.games.find_one({'id': gameId})


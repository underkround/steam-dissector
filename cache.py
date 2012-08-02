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
        self.games.ensure_index('id', unique=True)


    def clear(self):
        self.games.remove({})


    def putGame(self, game):
        self.games.update({'id': game['id']}, game, upsert=True)


    def getGame(self, gameId):
        game = self.games.find_one({'id': gameId})
        if game is not None:
            del game['_id']
        return game


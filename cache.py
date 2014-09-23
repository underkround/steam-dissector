import pymongo

class Cache(object):
    
    def __init__(self, mongoUri):
        self.connection = pymongo.Connection(mongoUri)
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


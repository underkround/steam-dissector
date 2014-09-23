import pymongo

class Cache(object):
    
    def __init__(self, mongoUri):
        client = pymongo.MongoClient(mongoUri)
        dbName = pymongo.uri_parser.parse_uri(mongoUri)['database']
        db = client[dbName]
        self.games = db.games


    def clear(self):
        self.games.remove({})


    def putGame(self, game):
        self.games.update({'id': game['id']}, game, upsert=True)


    def getGame(self, gameId):
        game = self.games.find_one({'id': gameId})
        if game is not None:
            del game['_id']
        return game


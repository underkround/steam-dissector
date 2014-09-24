import pymongo
import nullmongo
import datetime


class Cache(object):

    def __init__(self, mongoUri):
        try:
            client = pymongo.MongoClient(mongoUri)
            dbName = pymongo.uri_parser.parse_uri(mongoUri)['database']
            db = client[dbName]
            self.games = db.games
        except:
            print("WARNING: Cache is using null storage")
            self.games = nullmongo.NullCollection()


    def clear(self):
        self.games.remove({})


    def putGame(self, game):
        game['cache_created'] = datetime.datetime.utcnow()
        game['cache_hits'] = 0
        self.games.update({'id': game['id']}, game, upsert=True)


    def getGame(self, gameId):
        game = self.games.find_one({'id': gameId})
        if game is not None:
            del game['_id']
            self.games.update({'id': gameId}, {'$inc': {'cache_hits': 1}})
        return game

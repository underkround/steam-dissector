import pymongo
import nullmongo
import datetime


class Cache(object):

    def __init__(self, dbUri, dbName=''):
        try:
            client = pymongo.MongoClient(dbUri)
            if dbName == '':
                dbName = pymongo.uri_parser.parse_uri(dbUri)['database']
            db = client[dbName]
            self.games = db.games
        except Exception, err:
            print "WARNING: Cache is using null storage"
            print "  Exception: %s" % err
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

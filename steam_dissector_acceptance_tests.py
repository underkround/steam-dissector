from cache import Cache
import unittest
from steam_dissector import SteamDissector, GameNotFoundException
import json


class TestSteamDissector(unittest.TestCase):
    
    def setUp(self):
        self.cache = Cache()
        #self.cache.clear()

        self.steamDissector = SteamDissector(self.cache)


    def testForRealz(self):
        user = self.steamDissector.getUser('76561197972272127')
        print json.dumps(user)
        games = self.steamDissector.getGamesForUser('76561197972272127')
        print json.dumps(games)
        for game in games:
            try:
                g = self.steamDissector.getDetailsForGame(game['id'])
                print json.dumps(g)
            except GameNotFoundException:
                print "Game %s, %s not found!" % (game['id'], game['name'])

if __name__ == "__main__":
    unittest.main()

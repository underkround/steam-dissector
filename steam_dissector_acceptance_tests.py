from cache import Cache
import unittest
from steam_dissector import SteamDissector, GameNotFoundException
import json
from statistics import Statistics


class TestSteamDissector(unittest.TestCase):
    
    def setUp(self):
        self.cache = Cache()
        self.statistics = Statistics()

        self.steamDissector = SteamDissector(self.cache, self.statistics)


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


class TestCache(unittest.TestCase):
    
    def setUp(self):
        self.cache = Cache()
        self.cache.clear()


    def testGetGame(self):
        game = self.cache.getGame({'id': '105600'})
        self.assertIsNone(game)
        
        self.cache.putGame({'id': '105600', 'name': 'Terraria', 'features': ['Single-player', 'Multi-player', 'Co-op']})
        game = self.cache.getGame('105600')
        self.assertIsNotNone(game)
        self.assertEqual(game['id'], '105600')
        self.assertEqual(game['name'], 'Terraria')
        self.assertItemsEqual(game['features'], ['Single-player', 'Multi-player', 'Co-op'])
        
        
    def testUpdateGame(self):
        game = self.cache.getGame({'id': '105600'})
        self.assertIsNone(game)
        
        self.cache.putGame({'id': '105600', 'name': 'Terraria', 'features': ['Single-player', 'Multi-player', 'Co-op'], 'test': 'test'})
        self.cache.putGame({'id': '105600', 'name': 'Terraria2', 'features': []})
        game = self.cache.getGame('105600')
        self.assertIsNotNone(game)
        self.assertEqual(game['id'], '105600')
        self.assertEqual(game['name'], 'Terraria2')
        self.assertItemsEqual(game['features'], [])
        self.assertFalse('test' in game)
        self.assertFalse('_id' in game)
        self.assertEqual(self.cache.games.count(), 1)
        

if __name__ == "__main__":
    unittest.main()

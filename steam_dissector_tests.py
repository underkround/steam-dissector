import unittest
from steam_dissector import SteamDissector, UserNotFoundException,\
    GameNotFoundException
from cache import Cache
from mock_cache import MockCache

class TestSteamDissector(unittest.TestCase):
    
    def setUp(self):
        self.mockCache = MockCache()
        self.steamDissector = SteamDissector(self.mockCache)
        

    def testGetVanityProfile(self):
        user = self.steamDissector.getUser('zemm', True)

        self.assertEqual(user['id'], '76561198027383614')
        self.assertEqual(user['name'], 'zemm')
        

    def testGetGamesForUserWithVanityProfile(self):
        games = self.steamDissector.getGamesForUser('zemm', True)
        self.assertTrue(len(games) > 20)

    
    def testGetUser(self):
        user = self.steamDissector.getUser('76561197972272127')

        self.assertEqual(user['id'], '76561197972272127')
        self.assertEqual(user['name'], 'murgo')
        self.assertEqual(user['avatarIcon'], 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2.jpg')
        self.assertEqual(user['avatarMedium'], 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_medium.jpg')
        self.assertEqual(user['avatarFull'], 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_full.jpg')
        self.assertEqual(user['onlineState'], 'online')
        
        
    def testGetGamesForUser(self):
        games = self.steamDissector.getGamesForUser('76561197972272127')
        self.assertTrue(len(games) > 200)
        
        terraria = [game for game in games if game['name'] == 'Terraria'][0]

        self.assertIsNotNone(terraria)
        self.assertEqual(terraria['id'], '105600')
        self.assertEqual(terraria['name'], 'Terraria')
        self.assertEqual(terraria['logo'], 'http://media.steampowered.com/steamcommunity/public/images/apps/105600/e3f375e78ada9d2ec7ffa521fe1b0052d1d2bbb5.jpg')
        self.assertEqual(terraria['storeLink'], 'http://store.steampowered.com/app/105600')
        self.assertNotEqual(terraria['hoursLast2Weeks'], '')
        self.assertTrue(float(terraria['hoursOnRecord']) > 0)

        
    def testGetDetailsForGame(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertIsNotNone(terraria)
        self.assertEqual(terraria['id'], '105600')
        self.assertEqual(terraria['logoBig'], 'http://cdn.steampowered.com/v/gfx/apps/105600/header_292x136.jpg')
        self.assertEqual(terraria['logoSmall'], 'http://cdn.steampowered.com/v/gfx/apps/105600/capsule_184x69.jpg')
        self.assertEqual(terraria['storeLink'], 'http://store.steampowered.com/app/105600')
        self.assertEqual(terraria['metascore'], '83')
        self.assertEqual(terraria['name'], 'Terraria')
        self.assertItemsEqual(terraria['genres'], ['Action', 'Adventure', 'RPG', 'Indie', 'Platformer'])
        self.assertItemsEqual(terraria['developers'], ['Re-Logic'])
        self.assertItemsEqual(terraria['publishers'], [''])
        self.assertEqual(terraria['releaseDate'], '1305504000')
        self.assertItemsEqual(terraria['features'], ['Single-player', 'Multi-player', 'Co-op'])
        
        self.assertEqual(self.mockCache.getCount, 2)
        self.assertEqual(self.mockCache.putCount, 1)
        self.assertEqual(self.mockCache.games[0], terraria)


    def testCacheIsUsed(self):
        game1 = self.steamDissector.getDetailsForGame('105600')
        game2 = self.steamDissector.getDetailsForGame('105600')
        self.assertSequenceEqual(game1, game2)
        
        self.assertEqual(self.mockCache.getCount, 3)
        self.assertEqual(self.mockCache.putCount, 1)
        self.assertEqual(self.mockCache.games[0], game2)
        self.assertEqual(self.mockCache.games[0], game1)


    def testGetUserThrowsUserNotFoundException(self):
        ex = None
        try:
            self.steamDissector.getUser('asd')
        except UserNotFoundException as e:
            ex = e
        self.assertIsNotNone(ex)  


    def testGetGamesForUserThrowsUserNotFoundException(self):
        ex = None
        try:
            self.steamDissector.getGamesForUser('asd')
        except UserNotFoundException as e:
            ex = e
        self.assertIsNotNone(ex)  


    def testtestGetDetailsForGameThrowsGameNotFoundException(self):
        ex = None
        try:
            self.steamDissector.getDetailsForGame('asd')
        except GameNotFoundException as e:
            ex = e
        self.assertIsNotNone(ex)  
    

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
    
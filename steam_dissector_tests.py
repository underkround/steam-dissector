# coding=utf-8
import unittest
from steam_dissector import SteamDissector, UserNotFoundException,\
    GameNotFoundException
from mock_cache import MockCache
from mock_statistics import MockStatistics

class TestSteamDissector(unittest.TestCase):
    
    def setUp(self):
        self.mockCache = MockCache()
        self.mockStatistics = MockStatistics()
        self.steamDissector = SteamDissector(self.mockCache, self.mockStatistics)
        

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
        self.assertTrue(user['avatarIcon'].endswith('/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2.jpg'))
        self.assertTrue(user['avatarMedium'].endswith('/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_medium.jpg'))
        self.assertTrue(user['avatarFull'].endswith('/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_full.jpg'))
        self.assertEqual(user['onlineState'], 'online')
        
        
    def testGetGamesForUser(self):
        games = self.steamDissector.getGamesForUser('76561197972272127')
        self.assertTrue(len(games) > 200)

        terraria = [game for game in games if game['name'] == 'Terraria'][0]

        self.assertIsNotNone(terraria)
        self.assertEqual(terraria['id'], '105600')
        self.assertEqual(terraria['name'], 'Terraria')
        self.assertTrue(terraria['logo'].endswith('/steamcommunity/public/images/apps/105600/e3f375e78ada9d2ec7ffa521fe1b0052d1d2bbb5.jpg'))
        self.assertEqual(terraria['communityUrl'], 'http://steamcommunity.com/app/105600')
        self.assertNotEqual(terraria['hoursLast2Weeks'], '')
        self.assertTrue(float(terraria['hoursOnRecord']) > 0)

        
    def testGetGamesForUserSpeed(self):
        for x in xrange(10):
            self.steamDissector.getGamesForUser('76561197972272127')


    def testGetDetailsForGame(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertIsNotNone(terraria)
        self.assertEqual(terraria['id'], '105600')
        self.assertTrue(terraria['logoBig'].endswith('header.jpg'), terraria['logoBig'])
        self.assertTrue(terraria['logoSmall'].endswith('capsule_184x69.jpg'), terraria['logoSmall'])
        self.assertEqual(terraria['storeLink'], 'http://store.steampowered.com/app/105600')
        self.assertEqual(terraria['communityUrl'], 'http://steamcommunity.com/app/105600')
        self.assertEqual(terraria['metascore'], '83')
        self.assertEqual(terraria['name'], 'Terraria')
        self.assertItemsEqual(terraria['developers'], ['Re-Logic'])
        self.assertItemsEqual(terraria['publishers'], ['Re-Logic'])
        self.assertEqual(terraria['releaseDate'], '1305504000')

        self.assertEqual(self.mockCache.getCount, 2)
        self.assertEqual(self.mockCache.putCount, 1)
        self.assertEqual(self.mockCache.games[0], terraria)


    def testGenresForGame(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertIsNotNone(terraria)
        self.assertItemsEqual(terraria['genres'], ['Action', 'Adventure', 'RPG', 'Indie'])


    def testFeaturesForGame(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertIsNotNone(terraria)
        self.assertItemsEqual(terraria['features'], ['Single-player', 'Multi-player', 'Co-op', 'Steam Trading Cards'])


    def testUserTagsForGame(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertIsNotNone(terraria)
        self.assertEqual(terraria['userTags'], ['Sandbox', 'Adventure', 'Indie', '2D', 'Crafting'])


    def testCacheIsUsed(self):
        game1 = self.steamDissector.getDetailsForGame('105600')
        game2 = self.steamDissector.getDetailsForGame('105600')
        self.assertSequenceEqual(game1, game2)

        self.assertEqual(self.mockCache.getCount, 2)
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


    def testGetDetailsForGameThrowsGameNotFoundException(self):
        ex = None
        try:
            self.steamDissector.getDetailsForGame('asd')
        except GameNotFoundException as e:
            ex = e
        self.assertIsNotNone(ex)  
    
    
    def testMetascores(self):
        terraria = self.steamDissector.getDetailsForGame('105600')
        self.assertEqual(terraria['metascore'], '83')
        
        gameWithoutMetascore = self.steamDissector.getDetailsForGame('15700')
        self.assertEqual(gameWithoutMetascore['metascore'], '')

        ponipeli = self.steamDissector.getDetailsForGame('45100')
        self.assertEqual(ponipeli['metascore'], '')
        
    # something is fishy here
    def testAlienSwarm(self):
        game = self.steamDissector.getDetailsForGame('630')

        self.assertIsNotNone(game)
        self.assertItemsEqual(game['genres'], ['Action'])
        self.assertItemsEqual(game['developers'], ['Valve'])
        self.assertItemsEqual(game['publishers'], ['Valve'])
        

    def testEmptyPublishers(self):
        game = self.steamDissector.getDetailsForGame('1280')

        self.assertIsNotNone(game)
        self.assertItemsEqual(game['publishers'], [])


    def testUnicode(self):
        game = self.steamDissector.getDetailsForGame('62100')

        self.assertIsNotNone(game)
        self.assertItemsEqual(game['developers'], [u"Zoë Mode"])

        
    # Crysis Wars is merged with Crysis Warhead, so it shouldn't be found (redirect)
    def testCrysisWars(self):
        ex = None
        try:
            self.steamDissector.getDetailsForGame('17340')
        except GameNotFoundException as e:
            ex = e
        self.assertIsNotNone(ex) 
        
    
    def testMonkeyIsland2(self):
        game = self.steamDissector.getDetailsForGame('32460')
        self.assertIsNotNone(game)
        self.assertEqual(game['name'], u'Monkey Island™ 2 Special Edition: LeChuck’s Revenge™')


    def testStatistics(self):
        self.assertEqual(0, self.mockStatistics.userCount)
        self.steamDissector.getUser('zemm', True)
        self.assertEqual(1, self.mockStatistics.userCount)
        self.steamDissector.getUser('76561197972272127')
        self.assertEqual(2, self.mockStatistics.userCount)

        self.assertEqual(0, self.mockStatistics.gamesForUserCount)
        self.steamDissector.getGamesForUser('zemm', True)
        self.assertEqual(1, self.mockStatistics.gamesForUserCount)
        self.steamDissector.getGamesForUser('76561197972272127')
        self.assertEqual(2, self.mockStatistics.gamesForUserCount)

        self.assertEqual(0, self.mockStatistics.detailsFetchedCount)
        self.steamDissector.getDetailsForGame('105600')
        self.assertEqual(1, self.mockStatistics.detailsFetchedCount)
        self.steamDissector.getDetailsForGame('630')
        self.assertEqual(2, self.mockStatistics.detailsFetchedCount)


    def testUserWithUnicodeName(self):
        user = self.steamDissector.getUser('76561198002592825', False)
        self.assertEqual(user['name'], u'ぴえれ')

        games = self.steamDissector.getGamesForUser('76561198002592825', False)
        self.assertTrue(len(games) > 5)

if __name__ == "__main__":
    unittest.main()
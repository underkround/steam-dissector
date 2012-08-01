import unittest
from steam_dissector import SteamDissector

class Test(unittest.TestCase):
    
    def setUp(self):
        self.steamDissector = SteamDissector()

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
        self.assertEqual(terraria['metascore'], '83')
        self.assertEqual(terraria['name'], 'Terraria')
        self.assertItemsEqual(terraria['genres'], ['Action', 'Adventure', 'RPG', 'Indie', 'Platformer'])
        self.assertItemsEqual(terraria['developers'], ['Re-Logic'])
        self.assertItemsEqual(terraria['publishers'], [''])
        self.assertEqual(terraria['releaseDate'], '1305504000')
        self.assertItemsEqual(terraria['features'], ['Single-player', 'Multi-player', 'Co-op'])


#    def testForRealz(self):
#        import json
#        user = self.steamDissector.getUser('76561197972272127')
#        print json.dumps(user)
#        games = self.steamDissector.getGamesForUser('76561197972272127')
#        print json.dumps(games)
#        for game in games:
#            g = self.steamDissector.getDetailsForGame(game['id'])
#            print json.dumps(g)

if __name__ == "__main__":
    unittest.main()
    
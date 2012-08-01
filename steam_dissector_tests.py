import unittest
from steam_dissector import SteamDissector

class Test(unittest.TestCase):
    
    def setUp(self):
        self.steamDissector = SteamDissector()

    def testGetUser(self):
        user = self.steamDissector.getUser('76561197972272127')

        self.assertEqual(user.id, '76561197972272127')
        self.assertEqual(user.name, 'murgo')
        self.assertEqual(user.avatarIcon, 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2.jpg')
        self.assertEqual(user.avatarMedium, 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_medium.jpg')
        self.assertEqual(user.avatarFull, 'http://media.steampowered.com/steamcommunity/public/images/avatars/54/54b97d0998d152f01d876d03dad1fdd2fb642dd2_full.jpg')
        self.assertEqual(user.state, 'online')

if __name__ == "__main__":
    unittest.main()
    
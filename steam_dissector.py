import urllib2
from bs4 import BeautifulSoup
from user import User
from game import Game

class SteamDissector(object):
    
    def __init__(self):
        pass
    
    def getUser(self, userId):
        response = urllib2.urlopen('http://steamcommunity.com/profiles/%s?xml=1' % userId)
        userXml = response.read()
        
        soup = BeautifulSoup(userXml)
        
        user = User()
        user.id = soup.steamid64.string
        user.name = soup.steamid.string
        user.onlineState = soup.onlinestate.string
        user.avatarIcon = soup.avataricon.string
        user.avatarMedium = soup.avatarmedium.string
        user.avatarFull = soup.avatarfull.string
        
        return user

    def getGamesForUser(self, userId):
        response = urllib2.urlopen('http://steamcommunity.com/profiles/%s/games?xml=1' % userId)
        userXml = response.read()
        
        soup = BeautifulSoup(userXml)
        
        xmlgames = soup.find_all('game')
        
        games = []
        for xmlGame in xmlgames:
            game = Game()
            game.id = xmlGame.appid.string
            game.name = xmlGame.find('name').string
            game.logo = xmlGame.logo.string
            game.storeLink = xmlGame.storelink.string
            
            if xmlGame.hourslast2weeks is not None:
                game.hoursLast2Weeks = xmlGame.hourslast2weeks.string
            else:
                game.hoursLast2Weeks = '0'

            if xmlGame.hoursonrecord is not None:
                game.hoursOnRecord = xmlGame.hoursonrecord.string
            else:
                game.hoursOnRecord = '0'
            games.append(game)
            
        return games

from bs4 import BeautifulSoup
import urllib2
from user import User

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

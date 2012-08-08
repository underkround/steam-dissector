import urllib2
from bs4 import BeautifulSoup
import datetime
import calendar


def getString(soup, default=''):
    if soup is None or soup.string is None:
        return default
    return soup.string.strip()


class GameNotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class SteamDissector(object):
    
    def __init__(self, cache):
        self.cache = cache

    
    def getUser(self, userId):
        response = urllib2.urlopen('http://steamcommunity.com/profiles/%s?xml=1' % userId)
        xml = response.read()
        
        soup = BeautifulSoup(xml)
        
        if soup.response is not None and soup.response.error is not None:
            raise UserNotFoundException()
        
        user = {}
        user['id'] = getString(soup.steamid64)
        user['name'] = getString(soup.steamid)
        user['onlineState'] = getString(soup.onlinestate)
        user['avatarIcon'] = getString(soup.avataricon)
        user['avatarMedium'] = getString(soup.avatarmedium)
        user['avatarFull'] = getString(soup.avatarfull)
        
        return user


    def getGamesForUser(self, userId):
        response = urllib2.urlopen('http://steamcommunity.com/profiles/%s/games?xml=1' % userId)
        xml = response.read()
        
        soup = BeautifulSoup(xml)
        
        if soup.response is not None and soup.response.error is not None:
            raise UserNotFoundException()

        xmlgames = soup.find_all('game')
        
        games = []
        for xmlGame in xmlgames:
            game = {}
            game['id'] = getString(xmlGame.appid)
            game['name'] = getString(xmlGame.find('name'))
            game['logo'] = getString(xmlGame.logo)
            game['storeLink'] = getString(xmlGame.storelink)
            game['hoursLast2Weeks'] = getString(xmlGame.hourslast2weeks, '0')
            game['hoursOnRecord'] = getString(xmlGame.hoursonrecord, '0')

            games.append(game)
            
        return games
    
    
    def getDetailsForGame(self, gameId):
        dbgame = self.cache.getGame(gameId)
        if dbgame is not None:
            if 'notFound' in dbgame:
                raise GameNotFoundException()
            return dbgame
        
        opener = urllib2.build_opener()
        opener.addheaders.append(("Cookie", "birthtime=315561601"))
        response = opener.open('http://store.steampowered.com/app/%s/' % gameId)
        html = response.read()
        
        soup = BeautifulSoup(html, 'lxml')
        
        game = {'id': gameId}
        
        detailsBlock = soup.find('div', 'details_block')
        if detailsBlock is None:
            game['notFound'] = True
            self.cache.putGame(game)
            raise GameNotFoundException()
            
        nameHeader = detailsBlock.find('b', text='Title:')
        game['name'] = nameHeader.nextSibling.strip()

        game['logoSmall'] = 'http://cdn.steampowered.com/v/gfx/apps/%s/capsule_184x69.jpg' % gameId

        tmp = soup.find('img', 'game_header_image')
        game['logoBig'] = tmp.attrs['src'].split('?')[0] if tmp is not None else ''
                
        game['metascore'] = getString(soup.find(id='game_area_metascore'))

        genreHeader = detailsBlock.find('b', text='Genre:')
        if genreHeader is not None:
            genreAnchors = genreHeader.findNextSiblings('a')
            game['genres'] = []
            for genreAnchor in genreAnchors:
                game['genres'].append(getString(genreAnchor))
            
        developerHeader = detailsBlock.find('b', text='Developer:')
        if developerHeader is not None:
            developerAnchors = developerHeader.findNextSiblings('a')
            game['developers'] = []
            for developerAnchor in developerAnchors:
                game['developers'].append(getString(developerAnchor))
            
        publisherHeader = detailsBlock.find('b', text='Publisher:')
        if publisherHeader is not None:
            publisherAnchors = publisherHeader.findNextSiblings('a')
            game['publishers'] = []
            for publisherAnchor in publisherAnchors:
                game['publishers'].append(getString(publisherAnchor))
                
        releaseDateHeader = detailsBlock.find('b', text='Release Date:')
        if releaseDateHeader is not None and releaseDateHeader.nextSibling is not None:
            try:
                date = datetime.datetime.strptime(releaseDateHeader.nextSibling.strip(), '%d %b %Y')
                game['releaseDate'] = str(calendar.timegm(date.utctimetuple()))
            except:
                try:
                    date = datetime.datetime.strptime(releaseDateHeader.nextSibling.strip(), '%b %Y')
                    game['releaseDate'] = str(calendar.timegm(date.utctimetuple()))
                except:
                    pass
                    # shitty release date format

        features = soup.find_all('div', 'game_area_details_specs')
        if features is not None:
            game['features'] = []
            for feature in features:
                game['features'].append(getString(feature.find('div', 'name')))

        self.cache.putGame(game)
        dbgame = self.cache.getGame(gameId)
        return dbgame

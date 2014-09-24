import urllib2
from bs4 import BeautifulSoup
import datetime
import calendar
import re
from urllib2 import HTTPError
from lxml import etree

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    
    
titlere = re.compile("<b>Title:</b>(.*)<br>")
cdatare = re.compile("\[CDATA\[(.*)\]\]")

def getString(soup, default=''):
    if soup is None or soup.string is None:
        return default
    match = cdatare.search(soup.string)
    if match is None:
        return soup.string.strip()
    group = match.group(1)
    return group.strip()


def getText(soup, default=''):
    if soup is None or soup.text is None:
        return default
    return soup.text.strip()


class GameNotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class SteamUnavailableException(Exception):
    pass


class SteamDissector(object):
    
    def __init__(self, cache, statistics):
        self.cache = cache
        self.statistics = statistics

    
    def getUser(self, userId, isVanityUrl = False):
        url = 'http://steamcommunity.com/profiles/%s?xml=1' % userId
        if isVanityUrl:
            url = 'http://steamcommunity.com/id/%s?xml=1' % userId

        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(url, parser)
        except IOError as e:
            raise SteamUnavailableException()

        root = tree.getroot()

        if root[0].tag == 'error':
            raise UserNotFoundException()

        user = {}
        user['id'] = root.find('steamID64').text
        user['name'] = root.find('steamID').text
        user['onlineState'] = root.find('onlineState').text
        user['avatarIcon'] = root.find('avatarIcon').text
        user['avatarMedium'] = root.find('avatarMedium').text
        user['avatarFull'] = root.find('avatarFull').text
        
        self.statistics.putUser(user)
        return user


    def getGamesForUser(self, userId, isVanityUrl = False):
        url = 'http://steamcommunity.com/profiles/%s/games?xml=1' % userId
        if isVanityUrl:
            url = 'http://steamcommunity.com/id/%s/games?xml=1' % userId

        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(url, parser)
        except IOError as e:
            raise SteamUnavailableException()

        root = tree.getroot()

        if root[0].tag == 'error':
            raise UserNotFoundException()

        xmlgames = root[2]
        
        games = []
        for xmlGame in xmlgames:
            game = {}
            game['id'] = xmlGame.find("appID").text
            game['name'] = xmlGame.find('name').text
            game['logo'] = xmlGame.find('logo').text
            game['communityUrl'] = xmlGame.find('storeLink').text
            game['hoursLast2Weeks'] = xmlGame.find('hoursLast2Weeks')
            game['hoursOnRecord'] = xmlGame.find('hoursOnRecord')

            if game['hoursLast2Weeks'] is not None:
                game['hoursLast2Weeks'] = game['hoursLast2Weeks'].text
            else:
                game['hoursLast2Weeks'] = 0

            if game['hoursOnRecord'] is not None:
                game['hoursOnRecord'] = game['hoursOnRecord'].text
            else:
                game['hoursOnRecord'] = 0

            games.append(game)

        self.statistics.putGamesForUser(userId, games)
        return games


    def getDetailsForGame(self, gameId):
        self.statistics.detailsFetched(gameId)

        dbgame = self.cache.getGame(gameId)
        if dbgame is not None:
            if 'notFound' in dbgame:
                raise GameNotFoundException()
            return dbgame
        
        opener = urllib2.build_opener(NoRedirectHandler())
        opener.addheaders.append(("Cookie", "birthtime=315561601"))
        storeLink = 'http://store.steampowered.com/app/%s' % gameId

        try:
            response = opener.open(storeLink)
            html = response.read()
        except HTTPError as e:
            if (e.code == 503):
                raise SteamUnavailableException()
            raise e

        soup = BeautifulSoup(html, 'html5lib', from_encoding="utf-8")
        
        game = {'id': gameId}
        
        detailsBlock = soup.find('div', 'details_block')
        if detailsBlock is None:
            game['notFound'] = True
            self.cache.putGame(game)
            raise GameNotFoundException()
            
        match = titlere.search(html)
        if match is not None:
            game['name'] = BeautifulSoup(match.group(1).strip(), from_encoding="utf-8").text
        else:
            game['name'] = "Unknown"

        game['logoSmall'] = 'http://cdn.steampowered.com/v/gfx/apps/%s/capsule_184x69.jpg' % gameId
        game['storeLink'] = storeLink
        game['communityUrl'] = 'http://steamcommunity.com/app/%s' % gameId

        tmp = soup.find('img', 'game_header_image_full')
        game['logoBig'] = tmp.attrs['src'].split('?')[0] if tmp is not None else ''
        
        game['metascore'] = ''
        tmp = soup.find(id='game_area_metascore')
        if tmp != None:
            tmp = getText(tmp.find('span'))
            if tmp.isdigit(): game['metascore'] = tmp

        genreHeader = detailsBlock.find('b', text='Genre:')
        if genreHeader is not None:
            genreAnchors = genreHeader.findNextSiblings('a')
            game['genres'] = []
            for genreAnchor in genreAnchors:
                if genreAnchor.find_previous_sibling('b').text != "Genre:": break
                genre = getString(genreAnchor)
                if (genre != ""):
                    game['genres'].append(genre)
            
        developerHeader = detailsBlock.find('b', text='Developer:')
        if developerHeader is not None:
            developerAnchors = developerHeader.findNextSiblings('a')
            game['developers'] = []
            for developerAnchor in developerAnchors:
                if developerAnchor.find_previous_sibling('b').text != "Developer:": break
                developer = getString(developerAnchor)
                if (developer != ""):
                    game['developers'].append(developer)
            
        publisherHeader = detailsBlock.find('b', text='Publisher:')
        if publisherHeader is not None:
            publisherAnchors = publisherHeader.findNextSiblings('a')
            game['publishers'] = []
            for publisherAnchor in publisherAnchors:
                if publisherAnchor.find_previous_sibling('b').text != "Publisher:": break
                publisher = getString(publisherAnchor)
                if (publisher != ""):
                    game['publishers'].append(publisher)
                
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
        return game

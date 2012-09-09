from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from steam_dissector import SteamDissector, GameNotFoundException, UserNotFoundException,\
    SteamUnavailableException
from cache import Cache
import traceback
import json
import ConfigParser
from statistics import Statistics


class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        cache = Cache()
        statistics = Statistics()
        self.dissector = SteamDissector(cache, statistics)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        
        
    def do_GET(self):
        #hackiest of 'em all
        if self.path.startswith('/games/'): self.getGame(self.path[7:])
        elif self.path.startswith('/profiles/') and self.path.endswith('/games'): self.getProfileGames(self.path[10:self.path.find('/games')])
        elif self.path.startswith('/profiles/'): self.getProfile(self.path[10:])
        else:
            self.error(error = False)
            
            
    def printJson(self, js):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(js))
    
    
    def error(self, msg = '', code = 400, error = True):
        if error:
            self.log_error(msg)
            trace = traceback.format_exc()
            self.log_error(trace.replace('%', '%%'))
        self.send_error(code, msg)
    
    
    def isVanityUrl(self, profileId):
        import re
        if (re.match("\d{17}", profileId)):
            return False
        return True

    
    def getGame(self, gameId):
        try:
            json = self.dissector.getDetailsForGame(gameId)
            self.printJson(json)
        except GameNotFoundException:
            self.error('Game not found', 404)
        except SteamUnavailableException:
            self.error('Steam not available', 503)
        except:
            self.error('Error while getting game details for id: %s' % gameId)
        
        
    def getProfile(self, profileId):
        vanityUrl = self.isVanityUrl(profileId)
        try:
            json = self.dissector.getUser(profileId, vanityUrl)
            json['gamesUrl'] = '/profiles/%s/games' % profileId
            self.printJson(json)
        except UserNotFoundException:
            self.error('Profile not found', 404)
        except SteamUnavailableException:
            self.error('Steam not available', 503)
        except:
            self.error('Error while getting game details for id: %s' % profileId)
        
        
    def getProfileGames(self, profileId):
        vanityUrl = self.isVanityUrl(profileId)
        try:
            json = self.dissector.getGamesForUser(profileId, vanityUrl)
            for game in json:
                game['detailsUrl'] = '/games/%s' % game['id']
            self.printJson(json)
        except UserNotFoundException:
            self.error('Profile not found', 404)
        except SteamUnavailableException:
            self.error('Steam not available', 503)
        except:
            self.error('Error while getting games for profile id: %s' % profileId)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


if __name__ == '__main__':
    cfg = ConfigParser.RawConfigParser()
    cfg.read('config.cfg')
    port = cfg.getint('Server', 'port')

    server = ThreadedHTTPServer(('', port), Handler)
    print 'Starting server at port %s, use <Ctrl-C> to stop' % port

    server.serve_forever()

from steam_dissector import SteamDissector, GameNotFoundException, UserNotFoundException, SteamUnavailableException
from cache import Cache
import traceback
import ConfigParser
from statistics import Statistics
from flask import Flask, jsonify

cache = Cache()
statistics = Statistics()
dissector = SteamDissector(cache, statistics)
app = Flask(__name__)
app.debug = True
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('steam.log', maxBytes=1048576, backupCount=100)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

def error(msg = '', code = 400, err = True):
    if err:
        app.logger.error(msg)
        trace = traceback.format_exc()
        app.logger.error(trace.replace('%', '%%'))
    return msg, code

def is_vanity_url(profile_id):
    import re
    if re.match("\d{17}", profile_id):
        return False
    return True

@app.route("/games/<gameId>")
def get_game(game_id):
    try:
        json = dissector.getDetailsForGame(game_id)
        return jsonify(json)
    except GameNotFoundException:
        return error('Game not found', 404)
    except SteamUnavailableException:
        return error('Steam not available', 503)
    except:
        return error('Error while getting game details for id: %s' % game_id)

@app.route("/profiles/<profileId>")
def get_profile(profile_id):
    vanity_url = is_vanity_url(profile_id)
    try:
        json = dissector.getUser(profile_id, vanity_url)
        json['gamesUrl'] = '/profiles/%s/games' % profile_id
        return jsonify(json)
    except UserNotFoundException:
        return error('Profile not found', 404)
    except SteamUnavailableException:
        return error('Steam not available', 503)
    except:
        return error('Error while getting game details for id: %s' % profile_id)

@app.route("/profiles/<profileId>/games")
def get_profile_games(profile_id):
    vanity_url = is_vanity_url(profile_id)
    try:
        json = dissector.getGamesForUser(profile_id, vanity_url)
        for game in json:
            game['detailsUrl'] = '/games/%s' % game['id']
        return jsonify(json)
    except UserNotFoundException:
        return error('Profile not found', 404)
    except SteamUnavailableException:
        return error('Steam not available', 503)
    except:
        return error('Error while getting games for profile id: %s' % profile_id)

if __name__ == '__main__':
    cfg = ConfigParser.RawConfigParser()
    cfg.read('config.cfg')
    port = cfg.getint('Server', 'port')

    app.run(host='0.0.0.0', port=port, use_evalex=False)
    print('Starting server at port %s, use <Ctrl-C> to stop' % port)

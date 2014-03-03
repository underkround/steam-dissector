from steam_dissector import SteamDissector, GameNotFoundException, UserNotFoundException, SteamUnavailableException
from cache import Cache
import traceback
import ConfigParser
from statistics import Statistics
from flask import Flask, jsonify
import json

cache = Cache()
statistics = Statistics()
dissector = SteamDissector(cache, statistics)
app = Flask(__name__)
app.debug = False

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

@app.route("/")
def default():
  return "use /games/<id> and /profiles/<id> and /profiles/<id>/games"

@app.route("/games/<game_id>")
def get_game(game_id):
    try:
        js = dissector.getDetailsForGame(game_id)
        return jsonify(js)
    except GameNotFoundException:
        return error('Game not found', 404)
    except SteamUnavailableException:
        return error('Steam not available', 503)
    except:
        return error('Error while getting game details for id: %s' % game_id)

@app.route("/profiles/<profile_id>")
def get_profile(profile_id):
    vanity_url = is_vanity_url(profile_id)
    try:
        js = dissector.getUser(profile_id, vanity_url)
        js['gamesUrl'] = '/profiles/%s/games' % profile_id
        return jsonify(js)
    except UserNotFoundException:
        return error('Profile not found', 404)
    except SteamUnavailableException:
        return error('Steam not available', 503)
    except:
        return error('Error while getting game details for id: %s' % profile_id)

@app.route("/profiles/<profile_id>/games")
def get_profile_games(profile_id):
    vanity_url = is_vanity_url(profile_id)
    try:
        js = dissector.getGamesForUser(profile_id, vanity_url)
        for game in js:
            game['detailsUrl'] = '/games/%s' % game['id']
        return json.dumps(js)
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

    app.run(port=port)

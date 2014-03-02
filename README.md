# SteamDissector

SteamDissector is an library/service that can be used to fetch data from Steam, such as user info, user's games and game's details.

### Goals:

SteamDissector is primarily made for use in conjunction with [SteamDissector web gui](https://github.com/zemm/steam-dissector-gui).

Goal is to create a service that can be used to sort your Steam game library better, and answer questions such as:
* "What controller enabled games do I have?"
* "What multiplayer games my friend and I both own?"
* "Which game is the latest adventure game I have?"

### Dependencies:

Uses [MongoDB](http://www.mongodb.org/) as cache, since the Steam store is pretty slow.

#### Installing and running:

Requirements: `Python2.7, pip, virtualenv.`

1. Clone repository, chdir into it
2. Run command `virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r dependencies.txt`
3. Create config with `cp config.cfg.example config.cfg` and edit it for your pleasure
4. Run the flask app with your favourite web server, developement server can be run with `python main.py`
# SteamDissector

SteamDissector is an library/service that can be used to fetch data from Steam, such as user info, user's games and game's details.

### Goals:

SteamDissector is primarily made for use in conjunction with [SteamDissector web ui](https://github.com/zemm/steam-dissector-ui).

Goal is to create a service that can be used to sort your Steam game library better, and answer questions such as:
* "What controller enabled games do I have?"
* "What multiplayer games my friend and I both own?"
* "Which game is the latest adventure game I have?"

### Dependencies and libraries used:

* [MongoDB](http://www.mongodb.org/) for cache, since the Steam store is pretty slow.
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
* [lxml](http://lxml.de/)
* [PyMongo](https://github.com/mongodb/mongo-python-driver/)
* [Flask](http://flask.pocoo.org/)

#### Installing and running:

Requirements: `Python2.7, pip, virtualenv.`
Requirements for lxml: `python-dev, libxslt1-dev, zlib1g-dev`.

1. Install, configure and run MongoDB
2. Clone repository, chdir into it
3. Run command `virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt`
4. Create config with `cp config.cfg.example config.cfg` and edit it for your pleasure
5. Run the flask app with your favourite web server, developement server can be run with `python main.py`, gunicorn can be run with `gunicorn -b '127.0.0.1:8088' -w 3 -t 60 main:app`
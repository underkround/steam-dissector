class MockCache(object):
    
    def __init__(self):
        self.games = []
        self.putCount = 0
        self.getCount = 0


    def putGame(self, game):
        self.putCount += 1
        self.games.append(game)


    def getGame(self, gameId):
        self.getCount += 1
        matches = [x for x in self.games if x['id'] == gameId]
        if len(matches) == 0: return None
        return matches[0]  


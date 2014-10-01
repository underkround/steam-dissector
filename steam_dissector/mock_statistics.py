class MockStatistics(object):
    
    def __init__(self):
        self.userCount = 0
        self.gamesForUserCount = 0
        self.detailsFetchedCount = 0


    def putUser(self, user):
        self.userCount += 1


    def putGamesForUser(self, userId, games):
        self.gamesForUserCount += 1


    def detailsFetched(self, gameId):
        self.detailsFetchedCount += 1


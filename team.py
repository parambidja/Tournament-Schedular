class Team:
    def __init__(self, teamId, leagueType):
        self._teamId    = teamId
        self._leagueType = leagueType
        self._games     = list()
        self._opponents = set()

    def recordGame(self, game, opponentId):
        self._games.append(game)
        self._opponents.add(opponentId)

    def hasPlayed(self, teamId):
        return teamId in self._opponents

    def writeToCsv(self):
        # writes this Team's schedule to CSV
        filename = self._teamId + '_schedule.csv'

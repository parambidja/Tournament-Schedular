class Game                                          :
    def __init__(self, gameId, courtId, round, startTime, endTime, awayTeamId, homeTeamId, leagueType, eventId = 1):
        self._gameId     = gameId
        self._courtId    = courtId
        self._eventId    = eventId
        self._awayTeamId = awayTeamId
        self._homeTeamId = homeTeamId
        self._leagueType = leagueType
        self._round      = round
        self._startTime  = startTime
        self._endTime    = endTime

    def __str__(self):
        return "Game {}, Court: {}, Round: {}, Start time: {}, End time: {}, Home team: {}, Away team: {}".format(self._gameId, self._courtId, self._round, self._startTime, self._endTime, self._homeTeamId, self._awayTeamId)

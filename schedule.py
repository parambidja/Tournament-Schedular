from team import Team
from game import Game
import collections
import xlsxwriter
import os

class Schedule:
    def __init__(self, courtRangeK1, courtRangeK2, nTeamsK1, nTeamsK2, nGames, startTime, gameLength, gapStart=None, gapEnd=None):
        self._nCourtsK1    = len(courtRangeK1)
        self._nCourtsK2    = len(courtRangeK2)
        self._nTeamsK1     = nTeamsK1
        self._nTeamsK2     = nTeamsK2
        self._nGames       = nGames
        self._startTime    = startTime
        self._gameLength   = gameLength
        self._gapStart     = gapStart
        self._gapEnd       = gapEnd
        self._rounds       = list() # a single round is a list of Games played simultaneously
        self._numLeagues   = 1
        self._courtRangeK1 = courtRangeK1
        self._courtRangeK2 = courtRangeK2
        self._teamsK1      = {i: Team(i, 'K1') for i in range(1, nTeamsK1 + 1)}
        self._teamsK2      = {i: Team(i, 'K2') for i in range(1, nTeamsK2 + 1)}

    def generate(self):
        k1Matchups = self.generate_matchups(list(self._teamsK1.keys()))
        k2Matchups = self.generate_matchups(list(self._teamsK2.keys()))
        return self.make_schedule(k1Matchups, k2Matchups)

    def generate_matchups(self, teams):
        all_games = list()

        for round in range(self._nGames):
            matchups = self.make_pairs(teams)
            all_games += matchups
            teams = self.rotate_list(teams)

        return all_games

    def make_pairs(self, lst):
        tups = list()
        start = 0
        end = len(lst) - 1
        while(start < end):
            tups.append((lst[start], lst[end]))
            start += 1
            end -= 1
        return tups

    def rotate_list(self, lst):
        if len(lst) == 0: return lst
        to_rotate = lst[1:]
        rotated = collections.deque(to_rotate)
        rotated.rotate(1)
        return lst[:1] + list(rotated)

    # takes as input the list of tuples for all the games
    def make_schedule(self, k1Matchups, k2Matchups):
        currTime = self._startTime
        currRoundNum = 1
        currGameK1 = 0
        currGameK2 = 0
        currCourt = 1
        currGame = 1
        gapChanged = False
        while currGameK1 < len(k1Matchups) or currGameK2 < len(k2Matchups):
            currRound = list()
            for currCourt in range(1, self._nCourtsK1 + self._nCourtsK2 + 1):
                if self._gapStart and not gapChanged and currTime >= self._gapStart:
                    currTime = self._gapEnd
                    gapChanged = True

                currMatchup = None
                if currCourt in self._courtRangeK1:
                    if currGameK1 < len(k1Matchups):
                        # play K1 game
                        currMatchup = k1Matchups[currGameK1]
                        currLeague = 'K1'
                        teams = self._teamsK1
                        currGameK1 += 1
                    elif currGameK2 < len(k2Matchups):
                        # play K2 game
                        currMatchup = k2Matchups[currGameK2]
                        currLeague = 'K2'
                        teams = self._teamsK2
                        currGameK2 += 1
                else:
                    if currGameK2 < len(k2Matchups):
                        # play K2 games
                        currMatchup = k2Matchups[currGameK2]
                        currLeague = 'K2'
                        teams = self._teamsK2
                        currGameK2 += 1
                    elif currGameK1 < len(k1Matchups):
                        # play K1 game
                        currMatchup = k1Matchups[currGameK1]
                        currLeague = 'K1'
                        teams = self._teamsK1
                        currGameK1 += 1

                if currMatchup:
                    homeTeamId = currMatchup[0]
                    awayTeamId = currMatchup[1]
                    currGame = Game(currGameK1 + currGameK2, currCourt, currRoundNum, currTime, currTime + self._gameLength, awayTeamId, homeTeamId, currLeague)
                    currRound.append(currGame)
                    teams[homeTeamId].recordGame(currGame, awayTeamId)
                    teams[awayTeamId].recordGame(currGame, homeTeamId)

            self._rounds.append(currRound)
            currTime += self._gameLength
            currRoundNum += 1

        return self._rounds

    # writes the master schedule to csv
    # also creates a seperate schedule for each Team
    def writeToCsv(self, filename=None):
        if not filename:
            filename = 'output/master_schedule_{}.xlsx'.format(self._startTime.year)

        if not os.path.exists('output'):
            os.makedirs('output')

        output = xlsxwriter.Workbook(filename)
        worksheet = output.add_worksheet()

        #formats
        merge_format = output.add_format({'align': 'center'})
        fontColors = ['black', 'blue', 'red', 'cyan', 'magenta']

        totalCourts = self._nCourtsK1 + self._nCourtsK2
        worksheet.merge_range(0, 0, 0, totalCourts + 1, '|| Swami Shreeji ||', merge_format)
        worksheet.merge_range(1, 0, 1, totalCourts + 1, 'Yogi Cup {} Schedule'.format(self._startTime.year), merge_format)
        worksheet.write(2, 0, "Start Time")
        worksheet.write(2, 1, "End Time")

        for x in range(1, totalCourts + 1):
            worksheet.write(2, 1 + x, "COURT " + str(x))

        k1GameCounts = dict()
        k2GameCounts = dict()

        row = 3
        for round in self._rounds:
            for gameInd in range(len(round)):
                game = round[gameInd]
                if gameInd == 0:
                    worksheet.write(row, 0, game._startTime.strftime("%H:%M"))
                    worksheet.write(row, 1, game._endTime.strftime("%H:%M"))
                toWrite = "{}: {} vs {}".format(game._leagueType, game._homeTeamId, game._awayTeamId)
                format = output.add_format({'align': 'left'})
                if game._leagueType == 'K1':
                    if game._homeTeamId not in k1GameCounts:
                        k1GameCounts[game._homeTeamId] = 0
                    if game._awayTeamId not in k1GameCounts:
                        k1GameCounts[game._awayTeamId] = 0

                    k1GameCounts[game._homeTeamId] += 1
                    k1GameCounts[game._awayTeamId] += 1

                    fontInd = k1GameCounts[game._homeTeamId] % len(fontColors)
                    format.set_font_color(fontColors[fontInd])
                    format.set_bg_color('gray')
                else:
                    if game._homeTeamId not in k2GameCounts:
                        k2GameCounts[game._homeTeamId] = 0
                    if game._awayTeamId not in k2GameCounts:
                        k2GameCounts[game._awayTeamId] = 0

                    k2GameCounts[game._homeTeamId] += 1
                    k2GameCounts[game._awayTeamId] += 1

                    fontInd = k2GameCounts[game._homeTeamId] % len(fontColors)
                    format.set_font_color(fontColors[fontInd])
                    format.set_bg_color('white')

                worksheet.write(row, 1 + game._courtId, toWrite, format)
            row += 1

        output.close();

        teamWiseOutput = xlsxwriter.Workbook('output/team_wise_schedule_{}.xlsx'.format(self._startTime.year))
        for team in self._teamsK1.values():
            team.writeToCsv(teamWiseOutput)
        for team in self._teamsK2.values():
            team.writeToCsv(teamWiseOutput)

        teamWiseOutput.close()

    def writeToDBSchema(self, filename=None):
        if not filename:
            filename = 'output/database_schedule_{}.xlsx'.format(self._startTime.year)

        if not os.path.exists('output'):
            os.makedirs('output')

        output = xlsxwriter.Workbook(filename)
        worksheet = output.add_worksheet()

        headers = ['Game ID', 'League Type', 'Court', 'Home Team', 'Away Team', 'Start Time', 'End Time']
        for n in range(len(headers)):
            worksheet.write(0, n, headers[n])

        row = 0
        for round in self._rounds:
            for game in round:
                row += 1
                fields = [game._gameId, game._leagueType, game._courtId, game._homeTeamId, game._awayTeamId, game._startTime.strftime("%Y-%m-%d %H:%M:%S"), game._endTime.strftime("%Y-%m-%d %H:%M:%S")]
                for n in range(len(fields)):
                    worksheet.write(row, n, fields[n])
        output.close();

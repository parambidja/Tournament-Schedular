import xlsxwriter
import os

class Team:
    def __init__(self, teamId, leagueType):
        self._teamId    = teamId
        self._leagueType = leagueType
        self._games     = list()
        self._opponents = set()

    def recordGame(self, game, opponentId):
        if opponentId in self._opponents:
            raise ValueError('a team cannot play the same team twice')

        self._games.append(game)
        self._opponents.add(opponentId)

    def writeToCsv(self, output):
        team_name = "{} team {}".format(self._leagueType, self._teamId)

        worksheet = output.add_worksheet(team_name)

        col_width = 12
        worksheet.set_column('A:C', col_width)
        worksheet.set_column('E:F', col_width)

        top_format = output.add_format({'align': 'center', 'bold': True, 'font_color': 'black', 'font_name':'Arial', 'font_size': 24})
        header_format = output.add_format({'align': 'center', 'bold': True, 'font_color': 'white', 'font_name':'Arial', 'bg_color':'black', 'font_size': 11})
        games_format = output.add_format({'align': 'center', 'bold': False, 'font_color': 'black', 'font_name':'Arial', 'border':1, 'bottom_color': 'black', 'font_size': 11})

        top_format.set_align('vcenter')
        header_format.set_align('vcenter')
        games_format.set_align('vcenter')

        toWrite = "{} Team {} Schedule".format(self._leagueType, self._teamId)
        worksheet.merge_range(0, 0, 0, 5, toWrite, top_format)
        worksheet.set_row(0, 30)

        worksheet.set_row(1, 22)
        worksheet.write(1, 0, "Start Time", header_format)
        worksheet.write(1, 1, "End Time", header_format)
        worksheet.write(1, 2, "Game", header_format)
        worksheet.write(1, 3, "Court", header_format)
        worksheet.write(1, 4, "Home Team", header_format)
        worksheet.write(1, 5, "Away Team", header_format)
        row = 2
        gameCount = 1
        for game in self._games:
            worksheet.set_row(row, 22)
            worksheet.write(row, 0, game._startTime.strftime("%I:%M %p"), games_format)
            worksheet.write(row, 1, game._endTime.strftime("%I:%M %p"), games_format)
            worksheet.write(row, 2, "Game {}".format(gameCount), games_format)
            worksheet.write(row, 3, game._courtId, games_format)
            worksheet.write(row, 4, game._homeTeamId, games_format)
            worksheet.write(row, 5, game._awayTeamId, games_format)
            row += 1
            gameCount += 1

from team import Team
from game import Game
import collections

class Schedule:
    def __init__(self, nCourts, nTeams, nGames, startTime, gameLength, leagueType):
        self._nCourts    = nCourts
        self._nTeams     = nTeams
        self._nGames     = nGames
        self._startTime  = startTime
        self._gameLength = gameLength
        self._leagueType = leagueType
        self._rounds     = list() # a single round is a list of Games played simultaneously
        self._teams      = {i: Team(i, leagueType) for i in range(1, nTeams + 1)}

    def generate(self):
        matchups = self.generate_matchups()
        return self.make_schedule(matchups)

    def generate_matchups(self):
        teams = list(self._teams.keys())
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
    def make_schedule(self, games):
        curr_time = self._startTime
        curr_round = list()
        curr_round_n = 1
        curr_game_i = 0
        curr_court = 1

        while(curr_game_i < len(games)):
            curr_matchup_tup = games[curr_game_i]

            if(len(curr_round) == self._nCourts):
                self._rounds.append(curr_round)
                curr_round_n += 1
                curr_round = list()
                curr_court = 1
                curr_time += self._gameLength

            if curr_round_n % 2 != 0:
                home_team = curr_matchup_tup[0]
                away_team = curr_matchup_tup[1]
            else:
                away_team = curr_matchup_tup[0]
                home_team = curr_matchup_tup[1]

            curr_game = Game(curr_game_i, curr_court, curr_round_n, curr_time, curr_time + self._gameLength, away_team, home_team, self._leagueType)
            curr_round.append(curr_game)

            curr_game_i += 1
            curr_court += 1

        if(curr_round):
            self._rounds.append(curr_round)

        return self._rounds

    # writes the master schedule to csv
    # also creates a seperate schedule for each Team
    def writeToCsv(self, filename = 'final_schedule.csv'):
        pass

    def writeToDatabase(self):
        pass

    # for merging k1 and k2
    def merge_schedules(self, schedule2):
        pass

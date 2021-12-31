import unittest
from datetime import datetime
from datetime import timedelta
from schedule import Schedule

class ScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_schedule = Schedule(range(1,3), range(3,6), 8, 12, 3, datetime.strptime("10:00", '%H:%M'), timedelta(minutes=15))

    def test_rotate_list(self):
        self.assertTrue(self.mock_schedule.rotate_list([1,2,3]) == [1,3,2])
        self.assertTrue(self.mock_schedule.rotate_list([1,2,3,4]) == [1,4,2,3])

    def test_rotate_list_empty(self):
        self.assertTrue(self.mock_schedule.rotate_list([]) == [])

    def test_rotate_list_one_element(self):
        self.assertTrue(self.mock_schedule.rotate_list([1]) == [1])

    def test_make_pairs(self):
        result = self.mock_schedule.make_pairs([1,2,3,4])
        self.assertTrue(len(result) == 2)
        self.assertTrue((1,4) in result)
        self.assertTrue((2,3) in result)

    def test_generate_matchups(self):
        result = self.mock_schedule.generate_matchups([i for i in range(1, 9)])
        expected = [(1, 8), (2, 7), (3, 6), (4, 5), (1, 7), (8, 6), (2, 5), (3, 4), (1, 6), (7, 5), (8, 4), (2, 3)]
        self.assertTrue(result == expected)

    def test_generate(self):
        result = self.mock_schedule.generate()
        self.assertTrue(len(result) == 6)
        for round in result:
            self.assertTrue(len(round) == 5)

    def test_generate_edge_case(self):
        mock_schedule = Schedule(range(1,8), range(8,14), 62, 34, 4, datetime.strptime("2/8/2020 10:00", '%m/%d/%Y %H:%M'), timedelta(minutes=15))
        result = mock_schedule.generate()
        self.assert_no_dup_teams_in_round(result)
        gameCount = 0
        for round in result:
            gameCount += len(round)
            self.assertTrue(len(round) <= 13)
        self.assertTrue(gameCount == 192)

    def test_final_schedule(self):
        mock_schedule = Schedule(range(7,15), range(1,7), 76, 34, 5, datetime.strptime("2/8/2020 10:00", '%m/%d/%Y %H:%M'), timedelta(minutes=25), datetime.strptime("2/8/2020 14:10", '%m/%d/%Y %H:%M'), datetime.strptime("2/8/2020 15:35", '%m/%d/%Y %H:%M'))
        result = mock_schedule.generate()
        self.assert_no_dup_teams_in_round(result)
        mock_schedule.writeToCsv()
        mock_schedule.writeToDBSchema()

    def test_final_schedule_2022(self):
        mock_schedule = Schedule(range(7,15), range(1,7), 72, 40, 5, datetime.strptime("1/8/2022 10:00", '%m/%d/%Y %H:%M'), timedelta(minutes=25), datetime.strptime("1/8/2022 14:10", '%m/%d/%Y %H:%M'), datetime.strptime("1/8/2022 15:30", '%m/%d/%Y %H:%M'))
        result = mock_schedule.generate()
        self.assert_no_dup_teams_in_round(result)
        mock_schedule.writeToCsv()
        mock_schedule.writeToDBSchema()

    def assert_no_dup_teams_in_round(self, rounds):
        for round in rounds:
            k1Teams = set()
            k2Teams = set()
            for game in round:
                league = game._leagueType
                awayTeam = game._awayTeamId
                homeTeam = game._homeTeamId
                if league == 'K1':
                    self.assertFalse(game._awayTeamId in k1Teams)
                    self.assertFalse(game._homeTeamId in k1Teams)
                    k1Teams.add(game._awayTeamId)
                    k1Teams.add(game._homeTeamId)
                elif league == 'K2':
                    self.assertFalse(game._awayTeamId in k2Teams)
                    self.assertFalse(game._homeTeamId in k2Teams)
                    k2Teams.add(game._awayTeamId)
                    k2Teams.add(game._homeTeamId)

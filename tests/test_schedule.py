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
        gameCount = 0
        for round in result:
            gameCount += len(round)
            self.assertTrue(len(round) <= 13)
        self.assertTrue(gameCount == 192)

    def test_write_to_excel(self):
        mock_schedule = Schedule(range(7,15), range(1,7), 76, 36, 5, datetime.strptime("2/8/2020 10:00", '%m/%d/%Y %H:%M'), timedelta(minutes=25))
        mock_schedule.generate()
        mock_schedule.writeToCsv()
        mock_schedule.writeToDBSchema()

import unittest
from datetime import datetime
from datetime import timedelta
from schedule import Schedule

class ScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_schedule = Schedule(2, 8, 3, datetime.strptime("10:00", '%H:%M'), timedelta(minutes=15), "K1")

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
        result = self.mock_schedule.generate_matchups()
        expected = [(1, 8), (2, 7), (3, 6), (4, 5), (1, 7), (8, 6), (2, 5), (3, 4), (1, 6), (7, 5), (8, 4), (2, 3)]
        self.assertTrue(result == expected)

    def test_generate(self):
        result = self.mock_schedule.generate()
        self.assertTrue(len(result) == 6)
        for round in result:
            self.assertTrue(len(round) == 2)

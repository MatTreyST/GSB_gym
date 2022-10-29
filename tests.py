import unittest
from main import *
from pseudo_db import *


class TestUserAndDayInsert(unittest.TestCase):
    def test_user_and_day_insert(self):
        reset_data()
        user_and_day_insert('123', '12')
        user_and_day_insert('321', '21')
        res = user_and_day_insert('321', '31')
        self.assertTrue(res == {'123': ['12'], '321': ['31']})


class TestDayAndTimeListInsert(unittest.TestCase):
    def test_day_and_time_list_insert(self):
        reset_data()
        user_and_day_insert('123', '12')
        user_and_day_insert('321', '21')
        day_and_time_list_insert('123', '08:00')
        res = day_and_time_list_insert('321', '12:56')
        self.assertTrue(res == {'123': ['12', '08:00'], '321': ['21', '12:56']})


class TestGetInfo(unittest.TestCase):
    def test_get_info(self):
        reset_data()
        user_and_day_insert('7890', '12')
        user_and_day_insert('1234', '21')
        day_and_time_list_insert('1234', '08:00')
        day_and_time_list_insert('7890', '12:46')
        self.assertTrue(get_reservation_data(7890) == ['12', '12:46'])
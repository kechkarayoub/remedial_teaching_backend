from django.test import TestCase
from .utils import date_from_string
import datetime


class UtilsTest(TestCase):

    def setUp(self):
        pass

    def test_date_from_string(self):
        date_obj = date_from_string('01/01/2021')
        self.assertEqual(date_obj, datetime.datetime(2021, 1, 1, 0, 0))
        date_obj = date_from_string('25/01/2021')
        self.assertEqual(date_obj, datetime.datetime(2021, 1, 25, 0, 0))
        date_obj = date_from_string('25/001/2021')
        self.assertEqual(date_obj, None)
        date_obj = date_from_string('2021/01/21')
        self.assertEqual(date_obj, None)


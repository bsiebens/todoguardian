from django.test import TestCase
from datetime import date

from ...functions.date import to_date
from freezegun import freeze_time


@freeze_time("2024-06-07")
class ToDateTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.yesterday = date(2024, 6, 6)
        self.today = date(2024, 6, 7)
        self.tomorrow = date(2024, 6, 8)
        self.monday = date(2024, 6, 10)
        self.friday = date(2024, 6, 14)

    def testZeroDay(self):
        self.assertEqual(to_date("0d"), self.today)

    def testOneDay(self):
        self.assertEqual(to_date("1d"), self.tomorrow)

    def testZeroBDay(self):
        self.assertEqual(to_date("0b"), self.today)

    def testOneBDay(self):
        self.assertEqual(to_date("1b"), self.monday)

    def testOneBWeek(self):
        self.assertEqual(to_date("5b"), self.friday)

    def testZeroWeek(self):
        self.assertEqual(to_date("0w"), self.today)

    def testOneWeek(self):
        self.assertEqual(to_date("1w"), self.friday)

    def testZeroMonth(self):
        self.assertEqual(to_date("0m"), self.today)

    def testOneMonth(self):
        self.assertEqual(to_date("1m"), date(2024, 7, 7))

    def testOneMonthEdgeCases(self):
        self.assertEqual(to_date("1m", date(2015, 1, 29)), date(2015, 2, 28))
        self.assertEqual(to_date("1m", date(2016, 1, 31)), date(2016, 2, 29))
        self.assertEqual(to_date("1m", date(2015, 12, 31)), date(2016, 1, 31))
        self.assertEqual(to_date("1m", date(2015, 7, 31)), date(2015, 8, 31))
        self.assertEqual(to_date("1m", date(2015, 10, 31)), date(2015, 11, 30))

    def testZeroYear(self):
        self.assertEqual(to_date("0y"), self.today)

    def testOneYear(self):
        self.assertEqual(to_date("1y"), date(2025, 6, 7))

    def testLeapYear(self):
        self.assertEqual(to_date("1y", date(2016, 2, 29)), date(2017, 2, 28))
        self.assertEqual(to_date("4y", date(2016, 2, 29)), date(2020, 2, 29))

    def test_garbage(self):
        self.assertIsNone(to_date("1f"))

    def testToday(self):
        self.assertEqual(to_date("today"), self.today)
        self.assertEqual(to_date("tod"), self.today)
        self.assertEqual(to_date("today", self.tomorrow), self.today)

    def testTomorrow(self):
        self.assertEqual(to_date("tomorrow"), self.tomorrow)
        self.assertEqual(to_date("tom"), self.tomorrow)

    def testYesterday(self):
        self.assertEqual(to_date("yesterday"), self.yesterday)
        self.assertEqual(to_date("yes"), self.yesterday)

    def testMonday(self):
        self.assertEqual(to_date("monday"), self.monday)
        self.assertEqual(to_date("mo"), self.monday)

    def testFriday(self):
        self.assertEqual(to_date("friday"), self.friday)
        self.assertEqual(to_date("fri"), self.friday)

    def testOffset(self):
        self.assertEqual(to_date("1d", self.yesterday), self.today)

    def testNegativePattern(self):
        self.assertEqual(to_date("-1d"), self.yesterday)
        self.assertEqual(to_date("-0d"), self.today)

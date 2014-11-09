from nose.tools import istest

from unittest import TestCase

from libs.averagers import ReadingsAverager


class AveragerTests(TestCase):
    @istest
    def averaging_no_readings_returns_none(self):
        averager = ReadingsAverager()

        self.assertIsNone(averager.average_readings('0'))

    @istest
    def can_average_a_series_of_readings(self):
        averager = ReadingsAverager()
        averager.keep_readings('0','10')
        averager.keep_readings('0','20')
        averager.keep_readings('0','30')

        average = averager.average_readings('0')

        self.assertEqual(20.0, average)

    @istest
    def can_reset_a_series_of_readings(self):
        averager = ReadingsAverager()
        averager.keep_readings('0','10')

        averager.reset_readings('0')

        self.assertIsNone(averager.average_readings('0'))
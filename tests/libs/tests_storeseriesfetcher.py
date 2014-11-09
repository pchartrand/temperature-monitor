import datetime

from nose.tools import istest

from unittest import TestCase

from libs.storeseriesfetcher import StoreSeriesFetcher


class FakedStore(object):
    depth = 4
    def fetch(self):
        pass

    def last(self):
        return 3

    def get_one(self, i):
        serie = {
            3: ('1', 1.2, '2013-11-09 12:12:13'),
            2: ('0', 0.2, '2013-11-09 12:12:12'),
            1: ('1', 1.1, '2013-11-09 12:12:11'),
            0: ('0', 0.1, '2013-11-09 12:12:10')
        }
        return serie[i]


class StoreSeriesFetcherTests(TestCase):
    @istest
    def can_fetch_series_from_store(self):
        fetcher = StoreSeriesFetcher(FakedStore())

        s0, s1 = fetcher.fetch()

        self.assertEqual(
            [
                (datetime.datetime(2013, 11, 9, 12, 12, 12), 0.2),
                (datetime.datetime(2013, 11, 9, 12, 12, 10), 0.1),
            ],
            s0
        )
        self.assertEqual(
            [
                (datetime.datetime(2013, 11, 9, 12, 12, 13), 1.2),
                (datetime.datetime(2013, 11, 9, 12, 12, 11), 1.1),
            ],
            s1
        )
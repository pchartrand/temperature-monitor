from nose.tools import istest

from unittest import TestCase

from libs.store import Store


class StoreTests(TestCase):
    def setUp(self):
        self.store = Store()

    def tearDown(self):
        self.store.cleanup()

    @istest
    def can_store_and_recall_values(self):
        self.store.push('1',2.3, 3)

        self.assertEqual(['1', 2.3, 3], self.store.get_last())

    @istest
    def can_store_values_and_recall_them(self):
        self.store.push('1', 2.1, 1)
        self.store.push('1', 2.2, 2)
        self.store.push('1', 2.3, 3)

        self.assertEqual(['1', 2.3, 3], self.store.get_one(2))
        self.assertEqual(['1', 2.2, 2], self.store.get_one(1))
        self.assertEqual(['1', 2.1, 1], self.store.get_one(0))

    @istest
    def can_store_values_at_arbitrary_positions(self):
        self.store.store_one(1, '1', 5.5, 2)

        self.assertEqual(['1', 5.5, 2], self.store.get_one(1))

    @istest
    def missing_values_are_returned_as_nones(self):
        self.assertEqual([None, None, None], self.store.get_one(0))

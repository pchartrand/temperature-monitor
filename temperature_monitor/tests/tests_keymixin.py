from nose.tools import istest

from unittest import TestCase

from temperature_monitor.lib.storekeys import KeyMixin


class KeyMixinTests(TestCase):
    def setUp(self):
        self.key_mixin =  KeyMixin()
        self.key_mixin.make_keys(1)

    @istest
    def can_get_current_keys(self):
        keys = self.key_mixin.get_keys()

        self.assertEqual(['line_1', 'temp_1', 'time_1'], keys)

    @istest
    def can_get_a_specific_key_by_name(self):
        key = self.key_mixin.get_key('line')

        self.assertEqual('line_1', key)

    @istest
    def can_extract_data_by_name(self):
        stored_value = self.key_mixin.get_value({'line_1': 'toto'}, 'line')

        self.assertEqual('toto', stored_value)
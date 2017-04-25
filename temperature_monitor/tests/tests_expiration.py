from nose.tools import istest

from unittest import TestCase

from temperature_monitor.lib.expiration import Expiration


class ExpirationTests(TestCase):
    def setUp(self):
        self.expirer = Expiration()
        self.expected = [
            32, 1, 2, 1, 4, 1, 2, 1,
            8, 1, 2, 1, 4, 1, 2, 1,
            16, 1, 2, 1, 4, 1, 2, 1,
            8, 1, 2, 1, 4, 1, 2, 1,
        ]

    @istest
    def can_get_an_expiration_time(self):
        from temperature_monitor.lib.constants import HOURS, MINUTES, SECONDS
        time = self.expirer.get_expiration_time()
        self.assertEqual(time, HOURS * MINUTES * SECONDS)

    @istest
    def can_get_a_variable_expiration_time(self):
        from temperature_monitor.lib.constants import HOURS, MINUTES, SECONDS
        time = self.expirer.get_expiration_time(2)
        self.assertEqual(time, 2 * HOURS * MINUTES * SECONDS)

    @istest
    def can_get_a_range_of_expiration_times(self):

        expirations = [self.expirer.get_variable_multiplier(v) for v in range(32)]

        for i in range(32):
            self.assertEqual(self.expected[i], expirations[i])

    @istest
    def can_get_a_range_of_expiration_times(self):
        from temperature_monitor.lib.constants import HOURS, MINUTES, SECONDS

        expirations = [self.expirer.get_variable_expiration_time(v) for v in range(32)]

        for i in range(32):
            self.assertEqual(self.expected[i] * HOURS * MINUTES * SECONDS, expirations[i])

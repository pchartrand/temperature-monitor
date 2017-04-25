#- coding: utf-8 -#

import memcache

from temperature_monitor.lib.constants import MEMCACHED_HOST, SAMPLE_WINDOW
from temperature_monitor.lib.expiration import Expiration
from temperature_monitor.lib.storekeys import KeyMixin


class Store(KeyMixin):
    """Storage interface to memcache.
    Saves and fetches three values sequentially
    line_0:line number
    temp_0:a temperature
    time_0:timestamp
    line_1:...
    counter: last value of integer included in the keys.
    """

    def __init__(self, host=MEMCACHED_HOST, depth=SAMPLE_WINDOW):
        self.store = memcache.Client([host], debug=True)
        self.depth = depth
        self.counter = 0
        self.expirator = Expiration()

    def get_one(self, i):
        """get data from a precise position"""
        self.make_keys(i)
        data = self.store.get_multi(self.get_keys())
        return [self.get_value(data, key) for key in self.KEY_TEMPLATES]

    def _adjust_counter(self, i):
        if i > self.counter:
            self.counter = i-1
            self.store.set('counter', self.counter - 1)

    def store_one(self, i, line, temp, time):
        """store data at a precise position"""
        if i<0:
            raise ValueError("Cannot insert at negative position %s" % i)
        self.make_keys(i)
        self.store.set_multi(
            {
                self.get_key('line'): line,
                self.get_key('temp'): temp,
                self.get_key('time'): time
            },
            time=self.expirator.get_expiration_time()
        )
        self._adjust_counter(i)

    def push(self, line, temp, time):
        """add data at the end of the stack"""
        self.store_one(self.counter, line, temp, time)
        self.store.set('counter', self.counter)
        self.counter += 1

    def last(self):
        """index of last inserted data"""
        return self.store.get('counter')

    def get_last(self):
        """last inserted data"""
        return self.get_one(self.last())

    def cleanup(self):
        """wipes out data known to be saved by this instance"""
        for i in range(self.counter, 0, -1):
            self.make_keys(i - 1)
            self.store.delete_multi(self.get_keys())
        self.counter = 0

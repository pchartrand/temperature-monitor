#- coding: utf-8 -#

from constants import MEMCACHE_EXPIRATION_TIME, MEMCACHED_HOST, SAMPLE_WINDOW
import memcache


class KeyMixin(object):
    """Utility class to generate and maintain keys used to get/set values in the store
    """
    KEY_TEMPLATES = ['line', 'temp', 'time']
    keys = {}

    @staticmethod
    def _make_key(key, i):
        return '%s_%i' % (key, i)

    def make_keys(self, i):
        for key in self.KEY_TEMPLATES:
            self.keys[key] = self._make_key(key, i)

    def get_key(self, key):
        return self.keys.get(key)

    def get_keys(self):
        return [self.get_key(key) for key in self.KEY_TEMPLATES]

    def get_value(self, data, key):
        return data.get(self.get_key(key))


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

    def get_one(self, i):
        """get data from a precise position"""
        self.make_keys(i)
        data = self.store.get_multi(self.get_keys())
        return [self.get_value(data, key) for key in self.KEY_TEMPLATES]

    def store_one(self, i, line, temp, time):
        """store data at a precise position"""
        self.make_keys(i)
        self.store.set_multi(
            {
                self.get_key('line'): line,
                self.get_key('temp'): temp,
                self.get_key('time'): time
            },
            time=MEMCACHE_EXPIRATION_TIME
        )

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

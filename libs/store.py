#- coding: utf-8 -#

from constants import MEMCACHE_EXPIRATION_TIME, MEMCACHED_HOST, SAMPLE_WINDOW
import memcache


class Store(object):
    KEYS = ['line', 'temp', 'time']
    def __init__(self, host=MEMCACHED_HOST, depth=SAMPLE_WINDOW):
        self.store = memcache.Client([host], debug=True)
        self.depth = depth
        self.counter = 0
        self.keys = {}

    @staticmethod
    def _make_key(key, i):
        return '%s_%i' % (key, i)

    def make_keys(self, i):
        for key in self.KEYS:
            self.keys[key] = self._make_key(key, i)

    def get_key(self, key):
        return self.keys.get(key)

    def get_keys(self):
        return [self.get_key(key) for key in self.KEYS]

    def get_value(self, data, key):
        return data.get(self.get_key(key))

    def get_one(self, i):
        self.make_keys(i)
        data = self.store.get_multi(self.get_keys())
        return [self.get_value(data, key) for key in self.KEYS]

    def store_one(self, i, line, temp, time):
        self.make_keys(i)
        self.store.set_multi(
            {
                self.get_key('line'): line,
                self.get_key('temp'): temp,
                self.get_key('time'): time
            },
            time=MEMCACHE_EXPIRATION_TIME
        )

    def last(self):
        return self.store.get('counter')

    def push(self, line, temp, time):
        self.store_one(self.counter, line, temp, time)
        self.store.set('counter', self.counter)
        self.counter += 1

    def get_last(self):
        return self.get_one(self.last())

from os import environ
from constants import  HOURS, MINUTES, SECONDS


class Expiration(object):
    MEMCACHE_EXPIRATION_TIME = int(environ.get('MEMCACHE_EXPIRATION_TIME', HOURS * MINUTES * SECONDS))

    def get_expiration_time(self, multiplier=1):
        return self.MEMCACHE_EXPIRATION_TIME * multiplier

    @staticmethod
    def get_variable_multiplier(timestamp):
        if not (timestamp % 32):
            return 32
        elif not(timestamp % 16):
            return 16
        elif not(timestamp % 8):
            return 8
        elif not(timestamp % 4):
            return 4
        elif not (timestamp % 2):
            return 2
        else:
            return 1

    def get_variable_expiration_time(self, timestamp):
        return self.get_expiration_time(self.get_variable_multiplier(timestamp))
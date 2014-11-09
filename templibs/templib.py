#- coding: utf-8 -#

import datetime
import time


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_timestamp():
    return int(datetime.datetime.now().strftime('%s'))

def sleep(interval):
    time.sleep(interval)

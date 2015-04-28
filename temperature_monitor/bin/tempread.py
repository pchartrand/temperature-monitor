#!/usr/bin/env python
from temperature_monitor.lib.store import Store
from temperature_monitor.lib.constants import ARDUINO_NUMBER_OF_INPUTS

def main_func():
    store = Store()
    for i in range(ARDUINO_NUMBER_OF_INPUTS):
        (line, temp, timestamp) = store.get_one(store.last() - i)
        if temp is None:
            print("Memcached seems to be down.")
        else:
            print("%s %s %.1f" % (timestamp, line, float(temp)))


if __name__ == '__main__':
    main_func()

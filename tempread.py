#!/usr/bin/env python
from templibs.store import Store


if __name__ == '__main__':
    store = Store()
    for i in range(2):
        (line, temp, timestamp) = store.get_one(store.last() - i)
        if temp is None:
            print("Memcached seems to be down.")
        else:
            print("%s %s %.1f" % (timestamp, line, float(temp)))

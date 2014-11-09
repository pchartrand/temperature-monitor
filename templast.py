#!/usr/bin/env python
from templibs.store import Store


if __name__ == '__main__':
    store = Store()
    last = store.last()
    for i in range(store.depth):
        (line, temp, timestamp) = store.get_one(last - i)
        if line is None:
            continue
        print("%i %s %s %.1f" % (i, timestamp, line, float(temp)))


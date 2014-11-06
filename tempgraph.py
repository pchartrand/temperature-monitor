#!/usr/bin/env python
#- coding: utf-8 -#
from datetime import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from libs.store import Store
from libs.templib import get_time


def fetch():
    store = Store()
    last = store.last()
    d0 = []
    d1 = []
    t0 = []
    t1 = []
    for i in range(store.depth):
        (line, temp, timestamp) = store.get_one(last - i)
        if line is None:
            continue
        elif line == '0':
            d0.append(float(temp))
            t0.append(dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'))
        else:
            d1.append(float(temp))
            t1.append(dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'))
    return t0, d0, t1, d1


if __name__ == '__main__':
    t0, d0, t1, d1 = fetch()
    for s in (t0, d0, t1, d1):
        s.reverse()
    a0 = np.average(d0)
    a1 = np.average(d1)
    plt.plot(t0, d0)
    plt.plot(t0, [a0 for x in range(len(d0))])
    plt.plot(t1, d1)
    plt.plot(t1, [a1 for x in range(len(d1))])
    
    plt.legend((u'Extérieur', u'Moy. extérieur', u'Intérieur',u'Moy. intérieur'), loc='center right', shadow=True)
    plt.xlabel(u'Période')
    plt.ylabel(u'Température (C)')
    plt.title(u'Températures intérieures et extérieures\n%s' % get_time())

    plt.show()

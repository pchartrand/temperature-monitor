#!/usr/bin/env python
#- coding: utf-8 -#
import matplotlib.pyplot as plt

from templibs.store import Store
from templibs.storeseriesfetcher import StoreSeriesFetcher
from templibs.tempseriesplot import plot_temperatures


if __name__ == '__main__':
    fetcher = StoreSeriesFetcher(Store())
    s0, s1 = fetcher.fetch()
    for s in (s0, s1):
        s.reverse()
    plot_temperatures(plt, s0, s1)
    plt.show()

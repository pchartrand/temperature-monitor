#!/usr/bin/env python
#- coding: utf-8 -#
import matplotlib.pyplot as plt

from temperature_monitor.lib.store import Store
from temperature_monitor.lib.storeseriesfetcher import StoreSeriesFetcher
from temperature_monitor.lib.tempseriesplot import plot_temperatures


def main_func():
    fetcher = StoreSeriesFetcher(Store())
    series = fetcher.fetch()
    for s in (series):
        s.reverse()
    plot_temperatures(plt, series)
    plt.show()


if __name__ == '__main__':
    main_func()
#!/usr/bin/env python
#- coding: utf-8 -#
"""
Saves a drawing of last day of temperature readings.
"""
import logging
import os

import matplotlib
matplotlib.use('Agg')  #graphical backend not requiring X11
import matplotlib.pyplot as plt
from pylab import savefig, setp

from temperature_monitor.lib.constants import GRAPHS_OUTPUT_DIRECTORY
from temperature_monitor.lib.store import Store
from temperature_monitor.lib.storeseriesfetcher import StoreSeriesFetcher
from temperature_monitor.lib.tempseriesplot import plot_temperatures
from temperature_monitor.lib.templib import get_time

logging.basicConfig(level=logging.INFO)


def resize_xticklabels(plt, fontsize=10):
    setp(plt.axes().get_xticklabels(), fontsize=fontsize)


def main_func():
    fetcher = StoreSeriesFetcher(Store())
    s0, s1 = fetcher.fetch()
    for s in (s0, s1):
        s.reverse()
    plot_temperatures(plt, s0, s1)
    resize_xticklabels(plt, fontsize=8)
    filename = 'temperatures_%s.png' % get_time()
    filename = filename.replace(' ', '_')
    filename = os.path.join(GRAPHS_OUTPUT_DIRECTORY, filename)
    logging.info("Saving to file %s", filename)
    savefig(filename, dpi=300)


if __name__ == '__main__':
    main_func()
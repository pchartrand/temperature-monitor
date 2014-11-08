#!/usr/bin/env python
#- coding: utf-8 -#
import matplotlib.pyplot as plt
import numpy as np

from libs.store import Store
from libs.storeseriesfetcher import StoreSeriesFetcher
from libs.templib import get_time
from libs.tempseries import TempDataset


def plot_temperature_variations(time, temp):
    plt.plot(time, temp)


def plot_mean_temperature(x, avg):
    plt.plot(x, [avg for i in range(len(x))])


def decorate_plot():
    plt.legend((u'Extérieur', u'Moy. extérieur', u'Intérieur',u'Moy. intérieur'), loc='center right', shadow=True)
    plt.xlabel(u'Période')
    plt.ylabel(u'Température (C)')
    plt.title(u'Températures intérieures et extérieures\n%s' % get_time())


def plot_temperatures(s0, s1):
    external_temp = TempDataset(s0)
    internal_temp = TempDataset(s1)

    plot_temperature_variations(external_temp.timestamps, external_temp.temperatures)
    plot_mean_temperature(external_temp.timestamps, external_temp.average_temperature)

    plot_temperature_variations(internal_temp.timestamps, internal_temp.temperatures)
    plot_mean_temperature(internal_temp.timestamps, internal_temp.average_temperature)

    decorate_plot()


if __name__ == '__main__':
    fetcher = StoreSeriesFetcher(Store())

    s0, s1 = fetcher.fetch()
    for s in (s0, s1):
        s.reverse()
    plot_temperatures(s0, s1)
    plt.show()

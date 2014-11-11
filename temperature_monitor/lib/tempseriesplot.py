#- coding: utf-8 -#

from temperature_monitor.lib.templib import get_time
from temperature_monitor.lib.tempseries import TempDataset


class TempPlotter(object):
    """
    Given an instance of mathplotlib, generates a graph for temperature readings.
    """
    def __init__(self, plotter):
        self.plotter = plotter

    def plot_temperature_variations(self, time, temp):
        self.plotter.plot(time, temp)

    def plot_mean_temperature(self, x, avg):
        self.plotter.plot(x, [avg for i in range(len(x))])

    def decorate_plot(self):
        self.plotter.legend(
            (u'Extérieur', u'Moy. extérieure', u'Intérieur',u'Moy. intérieure'),
            loc='center right',
            shadow=True
        )
        self.plotter.xlabel(u'Période')
        self.plotter.ylabel(u'Température (C)')
        self.plotter.suptitle(u'Températures intérieures et extérieures')
        self.plotter.title(get_time())



def plot_temperatures(plt, s0, s1):
    """
    Generates a graph for two temperature readings.
    """
    external_temp = TempDataset(s0)
    internal_temp = TempDataset(s1)
    plotter = TempPlotter(plt)

    plotter.plot_temperature_variations(external_temp.timestamps, external_temp.temperatures)
    plotter.plot_mean_temperature(external_temp.timestamps, external_temp.average_temperature)

    plotter.plot_temperature_variations(internal_temp.timestamps, internal_temp.temperatures)
    plotter.plot_mean_temperature(internal_temp.timestamps, internal_temp.average_temperature)

    plotter.decorate_plot()
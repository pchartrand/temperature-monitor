#- coding: utf-8 -#

from temperature_monitor.lib.templib import get_time
from temperature_monitor.lib.tempseries import TempDataset
import matplotlib.lines as mlines


class TempPlotter(object):
    """
    Given an instance of mathplotlib, generates a graph for temperature readings.
    """
    def __init__(self, plotter, labels):
        self.plotter = plotter
        self.colors = self.define_colors()
        self.labels = labels

    def plot_temperature_variations(self, time, temp):
        self.plotter.plot(time, temp)

    def plot_mean_temperature(self, x, avg):
        self.plotter.plot(x, [avg for _ in range(len(x))])

    def define_colors(self):
        return ['blue', 'red', 'magenta', 'black', 'green']

    def _define_handles(self):
        lw=3
        handles = []
        dummy = mlines.Line2D([], [], color='white', label=u'', linewidth=lw)

        for color, label in zip(self.colors, self.labels):
            h = mlines.Line2D([], [], color=color, label=label, linewidth=lw)
            handles.append(h)
            handles.append(dummy)
        return handles

    def add_titles(self, xlabel, ylabel, suptitle, title):
        self.plotter.xlabel(xlabel)
        self.plotter.ylabel(ylabel)
        self.plotter.suptitle(suptitle)
        self.plotter.title(title)

    def add_legend(self):
        self.plotter.legend(
            handles = self._define_handles(),
            loc=3,
            ncol=5,
            bbox_to_anchor=(0.05, 0.0),
            prop={'size': 8}
        )


def report_on_temperature(temp, label):
    print("%s temperature:%s" % (label, round(temp.current_temperature, 1)))
    print(
        "average %s temperature over the last %s hours (%s seconds):%s" %
        (
            label,
            round(temp.time_variation_in_seconds/3600.0, 0),
            temp.time_variation_in_seconds,
            round(temp.average_temperature, 1)
        )
    )
    print(
        "%s temperature variation in the last hour:%s" %
        (
            label,
            temp.temperature_variation_for_last_hour
        )
    )
    print(u"")


def plot_temperatures(plt, series, labels):
    """
    Generates a graph for n temperature readings.
    """
    plotter = TempPlotter(plt, labels)

    for i, serie in enumerate(series):
        temperatures = TempDataset(serie)

        report_on_temperature(temperatures, i)

        plotter.plot_temperature_variations(temperatures.timestamps, temperatures.temperatures)
        plotter.plot_mean_temperature(temperatures.timestamps, temperatures.average_temperature)

    plotter.add_titles(
        xlabel=u'Période',
        ylabel=u'Température (C)',
        suptitle=u'Températures intérieures et extérieures',
        title=get_time()
    )

    if labels:
        plotter.add_legend()

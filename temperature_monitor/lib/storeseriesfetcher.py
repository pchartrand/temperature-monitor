from datetime import datetime as dt
from temperature_monitor.lib.constants import ARDUINO_NUMBER_OF_INPUTS


class StoreSeriesFetcher(object):
    """
    Responsible to fetch time series from store as distinct (timestamp, temperature) series
    """
    def __init__(self, store):
        self.store = store

    @staticmethod
    def _format(timestamp, temperature):
            return dt.strptime(timestamp, '%Y-%m-%d %H:%M:%S'), float(temperature)

    def fetch(self, samples=None):
        series_lists = []
        for i in range(ARDUINO_NUMBER_OF_INPUTS):
            series_lists.append([])

        if samples is None:
            samples = self.store.depth

        last = self.store.last()
        for i in range(samples):
            (line, temp, timestamp) = self.store.get_one(last - i)
            if line is None:
                continue
            elif int(line) < ARDUINO_NUMBER_OF_INPUTS:
                series_lists[int(line)].append(self._format(timestamp, temp))
            else:
                raise Exception("Unknown line %s" % line)
        return series_lists

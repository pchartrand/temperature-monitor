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

    def sample(self, sampling=60):
        series_lists = self.fetch()
        sampled_series = []
        for i in range(ARDUINO_NUMBER_OF_INPUTS):
            sampled_series.append([])
            for count, sample in enumerate(series_lists[i]):
                if not (count % sampling):
                    sampled_series[i].append(sample)
        return sampled_series

    def smooth(self, sampling=60):
        series_lists = self.fetch()
        smoothed_series = []
        for i in range(ARDUINO_NUMBER_OF_INPUTS):
            smoothed_series.append([])
            value = 0
            timestamp = None
            for count, sample in enumerate(series_lists[i]):  # going backwards in time
                if count == 0:
                    smoothed_series[i].append(sample)  # most recent sample
                    continue
                if count % sampling:
                    value = value + sample[1]
                    if count % sampling == 1:
                        timestamp = sample[0]
                else:
                    smoothed_series[i].append([timestamp, value / sampling])
                    value = 0
        return smoothed_series

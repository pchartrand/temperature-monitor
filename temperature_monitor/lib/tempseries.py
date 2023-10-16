import datetime
from functools import reduce

class TempDataset(object):
    """
    Convert (timestamp, temperature) series as distinct timestamp and temperature series.
    Calculates average temperature.
    """
    def __init__(self, temperature_time_series):
        self.timestamps, self.temperatures = self.split_coordinates_to_distinct_series(temperature_time_series)
        self.len = len(self.temperatures)
        self.current_temperature = self._get_current_temperature()
        self.average_temperature = self._get_average_temperature()
        self.temperature_variation = self._get_total_temperature_variation()
        self.temperature_variation_for_last_hour = self._get_temperature_variation_for_last_hour()
        self.time_variation = self._get_time_variation()
        self.time_variation_in_seconds = self._get_time_variation_in_seconds()

    def _get_average_temperature(self):
        if self.len > 0:
            return reduce(lambda x, y: x + y, self.temperatures) / self.len
        else:
            return None

    def _get_total_temperature_variation(self):
        if self.len > 0:
            return round(self.temperatures[-1] - self.temperatures[0], 1)

    def _get_temperature_variation_for_last_hour(self):
        if self.len >= 60:
            return round(self.temperatures[-1] - self.temperatures[-60], 1)

    def _get_time_variation_in_seconds(self):
        if self.len > 0:
            t0 = int(self._convert_datetime_to_seconds(self.timestamps[0]))
            t1 = int(self._convert_datetime_to_seconds(self.timestamps[-1]))
            return t1 - t0

    def _get_time_variation(self):
        if self.len > 0:
            return self.timestamps[-1] - self.timestamps[0]

    def _get_current_temperature(self):
        if self.len > 0:
            return self.temperatures[-1]

    @staticmethod
    def _convert_datetime_to_seconds(value):
        return value.strftime('%s') if isinstance(value, datetime.datetime) else value

    @staticmethod
    def split_coordinates_to_distinct_series(s):
        x = []
        y = []
        for xy in s:
            assert isinstance(xy[1], float)
            x.append(xy[0]), y.append(xy[1])
        return x, y

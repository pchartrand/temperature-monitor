import numpy as np


class TempDataset(object):
    def __init__(self, temperature_time_series):
        self.temperature_time_series = temperature_time_series
        self.timestamps, self.temperatures = self.split_coordinates_to_distinct_series(temperature_time_series)
        self.average_temperature = np.average(self.temperatures)

    @staticmethod
    def split_coordinates_to_distinct_series(s):
        x = []
        y = []
        for xy in s:
            x.append(xy[0]), y.append(xy[1])
        return x, y
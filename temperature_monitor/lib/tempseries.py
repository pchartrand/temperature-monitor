class TempDataset(object):
    """
    Convert (timestamp, temperature) series as distinct timestamp and temperature series.
    Calculates average temperature.
    """
    def __init__(self, temperature_time_series):
        self.timestamps, self.temperatures = self.split_coordinates_to_distinct_series(temperature_time_series)
        self.average_temperature = self.get_average_temperature()

    def get_average_temperature(self):
        if len(self.temperatures):
            return reduce(lambda x,y: x + y, self.temperatures) / len(self.temperatures)
        else:
            return None
    @staticmethod
    def split_coordinates_to_distinct_series(s):
        x = []
        y = []
        for xy in s:
            assert isinstance(xy[1], float)
            x.append(xy[0]), y.append(xy[1])
        return x, y
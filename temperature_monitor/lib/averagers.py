#- coding: utf-8 -#
from temperature_monitor.lib.constants import ARDUINO_NUMBER_OF_INPUTS

class ReadingsAverager(object):
    """
    Keeps most recent readings for distinct lines and returns average value.
    """
    def __init__(self):
        self.readings = {}
        for i in range(ARDUINO_NUMBER_OF_INPUTS):
            self.readings[str(i)] = []

    def keep_readings(self, line, temp):
        self.readings[line].append(temp)

    def average_readings(self, line):
        if len(self.readings[line]) == 0:
            return None

        sum_of_readings = float(reduce(lambda x,y: float(x)+float(y), self.readings[line]))
        return sum_of_readings / len(self.readings[line])

    def reset_readings(self, line):
        self.readings[line] = []


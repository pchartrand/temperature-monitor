#- coding: utf-8 -#


class ReadingsAverager(object):
    """
    Keeps most recent readings for distinct lines and returns average value.
    """
    LINE0 = '0'
    LINE1 = '1'
    readings = {LINE0: [], LINE1: []}
    def keep_readings(self, line, temp):
        self.readings[line].append(temp)

    def average_readings(self, line):
        sum_of_readings = float(reduce(lambda x,y: float(x)+float(y), self.readings[line]))
        return sum_of_readings / len(self.readings[line])

    def reset_readings(self, line):
        self.readings[line] = []


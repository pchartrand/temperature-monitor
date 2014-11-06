#- coding: utf-8 -#


class ReadingsAverager(object):
    LINE0 = '0'
    LINE1 = '1'
    readings = {LINE0: [], LINE1: []}
    def keep_readings(self, line, temp):
        self.readings[line].append(temp)

    def reset_readings(self, line):
        self.readings[line] = []

    def average_readings(self, line):
        sum_of_readings = float(reduce(lambda x,y: float(x)+float(y), self.readings[line]))
        return sum_of_readings / len(self.readings[line])

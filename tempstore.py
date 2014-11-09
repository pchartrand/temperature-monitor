#!/usr/bin/env python
from sys import argv
import logging

from templibs.arduinousb import ArduinoUSB
from templibs.averagers import ReadingsAverager
from templibs.constants import SAMPLE_PERIOD
from templibs.store import Store
from templibs.templib import get_time


class Reader(object):
    """Reads from arduino and saves samples of values to store.
    If averager is provided, will store average of samples collected during sampling period.
    """
    i = 0
    def __init__(self, arduino, store, averager=None):
        self.arduino = arduino
        self.store = store
        self.averager = averager

    def read(self):
        (line, temp) = self.arduino.read_temperatures()
        time = get_time()
        if self.averager is not None:
            self.averager.keep_readings(line, temp)
        return line, temp, time
    
    def sample(self):
        (line, temp, time) = self.read()
        logging.debug(u"%s [read] %s %.1f", time, line, float(temp))

        if self.i % SAMPLE_PERIOD in [0, 1]:
            if self.averager is not None:
                saved_temp = self.averager.average_readings(line)
            else:
                saved_temp = temp
            self.save(line, saved_temp, time)
            logging.info(u"%s [store] %s %.2f", time, line, saved_temp)
        self.i += 1

    def save(self, line, temp, time):
        self.store.push(line, temp, time)
        if self.averager is not None:
            self.averager.reset_readings(line)


if __name__ == '__main__':
    if '-v' in argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    averager = ReadingsAverager()
    reader = Reader(ArduinoUSB(), Store(), averager)
    while True:
        reader.sample()


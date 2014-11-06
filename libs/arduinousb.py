# -*- coding: UTF-8 -*-.
from constants import BAUD_RATE, PORT
import serial


class ArduinoUSB(object):
    def __init__(self, port=PORT, baud_rate=BAUD_RATE):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = serial.Serial(self.port, self.baud_rate)

    def read_line(self):
        return self.serial.readline()

    def read_line_stripped(self):
        return self.read_line().strip()

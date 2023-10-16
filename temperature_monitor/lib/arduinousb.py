# -*- coding: UTF-8 -*-.
from temperature_monitor.lib.constants import ARDUINO_BAUD_RATE, ARDUINO_USB_PORT
import serial


class ArduinoUSB(object):
    """Returns values from arduino via USB port.
    Assumes arduino returns an array of column delimited values such as 0:20.1, 1:7.2,
    where first item is the analog input, and second item is a temperature in celsius
    """
    def __init__(self, port=ARDUINO_USB_PORT, baud_rate=ARDUINO_BAUD_RATE):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = serial.Serial(self.port, self.baud_rate)

    def read_line(self):
        return self.serial.readline().decode('ASCII')

    def read_line_stripped(self):
        return self.read_line().strip()

    def read_temperatures(self):
        return self.read_line_stripped().split(':')

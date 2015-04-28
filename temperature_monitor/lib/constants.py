#- coding: utf-8 -#
from os import environ

ARDUINO_USB_PORT = environ.get('ARDUINO_USB_PORT', '/dev/ttyUSB0')
ARDUINO_BAUD_RATE = environ.get('ARDUINO_BAUD_RATE', 9600)
GRAPHS_OUTPUT_DIRECTORY = environ.get('GRAPHS_OUTPUT_DIRECTORY', './')
MEMCACHED_HOST = environ.get('MEMCACHED_HOST','127.0.0.1:11211')
MEMCACHE_EXPIRATION_TIME =  environ.get('MEMCACHE_EXPIRATION_TIME', 24 * 60  * 60)
SAMPLE_PERIOD = environ.get('SAMPLE_PERIOD', 60)
SAMPLE_WINDOW = environ.get('SAMPLE_WINDOW', 2880)

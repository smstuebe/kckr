import threading
from time import sleep
import math
import sys
import grovepi


class Air:
    def __init__(self, tempSensorDigitalPort, debugging=False):
        self.msPerRead = 15000
        self.temperature = None
        self.humidity = None
        self.tempSensorDigitalPort = tempSensorDigitalPort

    def update(self, milliseconds):
        if milliseconds % self.msPerRead > 0:
            return

        try:
            [temp, humidity] = grovepi.dht(self.tempSensorDigitalPort, 1)

            if math.isnan(temp) is False and math.isnan(humidity) is False:
                self.temperature = temp
                self.humidity = humidity

        except BaseException as ex:
            print("[air] " + str(ex), file=sys.stderr)

    def hasValues(self):
        return isinstance(self.temperature, float) and isinstance(self.humidity, float)

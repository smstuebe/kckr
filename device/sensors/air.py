import threading
from time import sleep
import math
import sys
import grovepi

class Air(threading.Thread):
    def __init__(self, tempSensorDigitalPort, lock, debugging=False):
        super(Air, self).__init__(name="Temperature and Humidity sensor")
        self.pollingDelay = 15
        self.temperature = None
        self.humidity = None
        self.tempSensorDigitalPort = tempSensorDigitalPort
        self.lock = lock
        self.event_stopper = threading.Event()

    def stop(self):
        self.event_stopper.set()
        self.join()

    def run(self):
        sleep(2)
        while not self.event_stopper.is_set():
            try:
                with self.lock:
                    [temp, humidity] = grovepi.dht(self.tempSensorDigitalPort, 1)

                if math.isnan(temp) is False and math.isnan(humidity) is False:
                    self.temperature = temp
                    self.humidity = humidity

            except BaseException as ex:
                print("[air] " + str(ex), file=sys.stderr)
            finally:
                sleep(self.pollingDelay)

    def hasValues(self):
        return isinstance(self.temperature, float) and isinstance(self.humidity, float)
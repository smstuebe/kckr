import threading
from time import sleep
import collections
import math
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
        while not self.event_stopper.is_set():
            try:
                with self.lock:
                    [temp,humidity] = grovepi.dht(self.tempSensorDigitalPort, 1)
                  
                if math.isnan(temp) == False and math.isnan(humidity) == False:
                    self.temperature = temp
                    self.humidity = humidity

            # in case we have an IO error
            except IOError:
                print("[dht sensor][we've got an IO error]")

            # intented to catch NaN errors
            except RuntimeWarning as error:
                print(str(error))
            except:
                print("some exception, ignored it :P")

            finally:
                sleep(self.pollingDelay)

    def hasValues(self):
        return isinstance(self.temperature, float) and isinstance(self.humidity, float)
import threading
from time import sleep
from datetime import datetime, timedelta
import numpy
import grovepi
import sys

class Loudness(threading.Thread):
    def __init__(self, loudnessSensorAnalogPort, sensorLock, debugging=False):
        super(Loudness, self).__init__(name="Loudness sensor")
        self.pollingDelay = 0.2
        self.loudnessSensorAnalogPort = loudnessSensorAnalogPort
        self.sensorLock = sensorLock
        self.stoppedEvent = threading.Event()
        self.history = []

    def stop(self):
        self.stoppedEvent.set()
        self.join()

    def run(self): 
        startTime = datetime.now()
        self.history = []
        while not self.stoppedEvent.is_set():
            try:
                with self.sensorLock:
                    loudness = grovepi.analogRead(self.loudnessSensorAnalogPort)

                timeStamp = int((datetime.now() - startTime).total_seconds() * 1000)
                self.history.append((timeStamp, loudness))

            except IOError:
                print("[loudness sensor]: IO error")
            except RuntimeWarning as error:
                print("[loudness sensor]: ", str(error))
            except BaseException as ex:
                print("[loudness sensor]: ", str(ex))

            finally:
                sleep(self.pollingDelay)
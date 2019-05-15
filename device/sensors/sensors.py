import threading
from time import sleep
import collections
import numpy
import sys
import grovepi
import rx
from sensors.occupation import Occupation
from sensors.air import Air
from sensors.loudness import Loudness


class Sensors(threading.Thread):
    def __init__(self, debugging=False):
        super(Sensors, self).__init__(name="Sensor reader")
        self.event_stopper = threading.Event()
        self.occupation = Occupation(6)
        self.air = Air(7)
        self.loudness = Loudness(1)

    def stop(self):
        self.event_stopper.set()
        self.join()

    def run(self):
        # tick milliseconds (not real milliseconds due to read delays)
        milliseconds = 0

        while not self.event_stopper.is_set():
            try:
                self.occupation.update(milliseconds)
                self.air.update(milliseconds)
                self.loudness.update(milliseconds)

            except BaseException as ex:
                print("[sensors] " + str(ex), file=sys.stderr)

            finally:
                sleep(0.1)
                milliseconds += 100
                milliseconds %= 10000000  # overflow prevention

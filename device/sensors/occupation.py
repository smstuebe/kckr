import threading
from time import sleep
import collections
import numpy
import sys
import grovepi

class Occupation(threading.Thread):
    def __init__(self, motionSensorDigitalPort, lock, debugging=False):
        super(Occupation, self).__init__(name="Occupation detection")
        self.pollingDelay = 0.5
        self.isOccupied = False
        self.motionSensorDigitalPort = motionSensorDigitalPort
        self.lock = lock
        self.event_stopper = threading.Event()

        bufferSize = int(15 / self.pollingDelay)
        self.buffer = collections.deque(numpy.zeros(
            bufferSize, dtype=numpy.int), bufferSize)

    def stop(self):
        self.event_stopper.set()
        self.join()

    def run(self):
        grovepi.pinMode(self.motionSensorDigitalPort, "INPUT")

        while not self.event_stopper.is_set():
            try:
                with self.lock:
                    motion = grovepi.digitalRead(self.motionSensorDigitalPort)

                if motion == 0 or motion == 1:
                    self.buffer.append(motion)

                mean = numpy.average(self.buffer)
                if self.isOccupied and mean <= 1 / len(self.buffer):
                    self.isOccupied = False
                elif not self.isOccupied:
                    self.isOccupied = bool(mean >= 0.3)

            except BaseException as ex:
                print("[occupation] " + str(ex), file=sys.stderr)

            finally:
                sleep(self.pollingDelay)

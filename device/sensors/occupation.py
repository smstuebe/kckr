import threading
from time import sleep
import collections
import numpy
import sys
import grovepi
import rx


class Occupation:
    def __init__(self, motionSensorDigitalPort, debugging=False):
        self.msPerRead = 500  # every 0.5 sec
        self.isOccupied = False
        self.motionSensorDigitalPort = motionSensorDigitalPort

        bufferSize = int(15000 / self.msPerRead)  # 15 sec
        self.buffer = collections.deque(numpy.zeros(
            bufferSize, dtype=numpy.int), bufferSize)
        grovepi.pinMode(self.motionSensorDigitalPort, "INPUT")

    def update(self, milliseconds):
        if milliseconds % self.msPerRead > 0:
            return

        try:
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

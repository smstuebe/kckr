import threading
from time import sleep
import collections
import numpy

class Occupation(threading.Thread):
    def __init__(self, motionSensorDigitalPort, debugging=False):
        super(Occupation, self).__init__(name="Occupation detection")
        self.pollingDelay = 0.5
        self.isOccupied = False
        self.motionSensorDigitalPort = motionSensorDigitalPort
        self.event_stopper = threading.Event()

        bufferSize = 5 / self.pollingDelay
        self.buffer = collections.deque(numpy.zeros(
            bufferSize, dtype=numpy.int), bufferSize)

    def stop(self):
        self.event_stopper.set()
        self.join()

    def run(self):
        grovepi.pinMode(self.motionSensorDigitalPort, "INPUT")

        while not self.event_stopper.is_set():
            try:
                motion = grovepi.digitalRead(self.motionSensorDigitalPort)
                if motion == 0 or motion == 1:
                    self.buffer.append(motion)

                mean = numpy.average(self.buffer)
                if self.isOccupied and mean <= 1 / len(self.buffer):
                    self.isOccupied = False
                elif not self.isOccupied:
                    self.isOccupied = mean >= 0.5

            # in case we have an IO error
            except IOError:
                print("[occupation sensor][we've got an IO error]")

            # intented to catch NaN errors
            except RuntimeWarning as error:
                print(str(error))

            finally:
                sleep(self.pollingDelay)
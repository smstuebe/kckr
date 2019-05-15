import threading
from time import sleep
from datetime import datetime, timedelta
import numpy
import grovepi
import sys


class Loudness:
    def __init__(self, loudnessSensorAnalogPort, debugging=False):
        self.msPerRead = 200
        self.loudnessSensorAnalogPort = loudnessSensorAnalogPort
        self.isActive = False
        self.history = []
        self.startTime = None

    def reset(self):
        self.history = []
        self.startTime = datetime.now()

    def setActive(self, active):
        if active:
            self.reset()

        self.isActive = active

    def update(self, milliseconds):
        if not self.isActive or milliseconds % self.msPerRead > 0:
            return

        try:
            loudness = grovepi.analogRead(self.loudnessSensorAnalogPort)

            #timeStamp = int((datetime.now() - startTime).total_seconds() * 1000)
            self.history.append((datetime.now(), loudness))

        except BaseException as ex:
            print("[loudness] " + str(ex), file=sys.stderr)

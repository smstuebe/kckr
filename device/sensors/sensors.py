import threading
from time import sleep
import collections
from occupation import Occupation
from air import Air
from loudness import LoudnessValue

# argparse

class SensorValues:
    def __init__(self):
        self.timestamp = 0
        self.temperature = 0
        self.humidity = 0
        self.light = 0
        self.occupied = False
        self.loudness = LoudnessValue()

occupation = Occupation(6)
air = Air(7)

try:
    occupation.run()
    air.run()

    while True:

        sleep(1) 

# when pressing CTRL-C
except KeyboardInterrupt:
    # stop gathering data
    occupation.stop()
    air.stop()
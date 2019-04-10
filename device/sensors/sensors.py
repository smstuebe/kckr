import threading
from time import sleep
import collections
from occupation import Occupation
from air import Air
from loudness import Loudness

# argparse


import ptvsd
ptvsd.enable_attach(address=('192.168.178.27', 1337), redirect_output=True)
ptvsd.wait_for_attach()

class SensorValues:
    def __init__(self):
        self.timestamp = 0
        self.temperature = 0
        self.humidity = 0
        self.light = 0
        self.occupied = False

lock = threading.Lock()
occupation = Occupation(6, lock)
air = Air(7, lock)
loudness = Loudness(1, lock)

try:
    occupation.start()
    air.start()
    loudness.start()

    while True:

        print("Occupied     %s" % (occupation.isOccupied))
        if(air.hasValues()):
            print("Temperature  %.02f°C" % (air.temperature))
            print("Humidity     %.02f%%" % (air.humidity))

        sleep(1)

except KeyboardInterrupt:
    occupation.stop()
    air.stop()
    loudness.stop()

for entry in loudness.history:
    print("{time:07}: {value: >3}".format(time=entry[0], value=entry[1]))

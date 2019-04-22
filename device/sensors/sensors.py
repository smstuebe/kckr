import threading
from time import sleep
import collections
import requests
import json
from occupation import Occupation
from air import Air
from loudness import Loudness
import argparse

parser = argparse.ArgumentParser(description="Kicker activity indicator.")
parser.add_argument('--debug', action='store_const',
                    const=True, default=False,
                    help='Listen to the debugger.')

args = parser.parse_args()

if args.debug:
    import ptvsd
    ptvsd.enable_attach(address=('192.168.178.27', 1337), redirect_output=True)
    ptvsd.wait_for_attach()


# class Game:
#    def __init__(self):

lock = threading.Lock()
occupation = Occupation(6, lock)
air = Air(7, lock)
loudness = Loudness(1, lock)

try:
    occupation.start()
    air.start()
    # loudness.start()
    num = 0
    while True:
        print("Occupied     %s" % (occupation.isOccupied))
        if air.hasValues():
            print("Temperature  %.02f°C" % (air.temperature))
            print("Humidity     %.02f%%" % (air.humidity))

        num += 1
        sleep(1)
        if num == 15 and air.hasValues():
            print("sending data")
            requests.post("", json={
                "Occupied": occupation.isOccupied,
                "Temperature": air.temperature,
                "Humidity": air.humidity
            })
            num = 0

except KeyboardInterrupt:
    occupation.stop()
    air.stop()
    loudness.stop()

# for entry in loudness.history:
#    print("{time:07}: {value: >3}".format(time=entry[0], value=entry[1]))

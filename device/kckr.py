import threading
from time import sleep
import collections
import requests
import json
from sensors.occupation import Occupation
from sensors.air import Air
from sensors.loudness import Loudness
import argparse
import configparser
from backend.backend import Backend

parser = argparse.ArgumentParser(description="Kicker activity indicator.")
parser.add_argument('--debug', action='store_const',
                    const=True, default=False,
                    help='Listen to the debugger.')
parser.add_argument('--verbose', action='store_const',
                    const=True, default=False,
                    help='Verbose output mode.')

args = parser.parse_args()

if args.debug:
    import ptvsd
    ptvsd.enable_attach(address=('192.168.178.27', 1337), redirect_output=True)
    ptvsd.wait_for_attach()

config = configparser.ConfigParser()
config.read("/mnt/device/config.ini")
# TODO: make dynamic
# TODO: validate
# TODO: make sensor ports configurable

print("Started kckr for location: %s" % (config["device"]["location"]))

lock = threading.Lock()
occupation = Occupation(6, lock)
air = Air(7, lock)
loudness = Loudness(1, lock)
backend = Backend(config)

try:
    occupation.start()
    air.start()
    # loudness.start()
    num = 0
    occupied = None
    while True:
        print("Occupied     %s" % (occupation.isOccupied))
        if air.hasValues():
            print("Temperature  %.02f°C" % (air.temperature))
            print("Humidity     %.02f%%" % (air.humidity))
        num += 1

        if occupied != occupation.isOccupied:
            occupied = occupation.isOccupied
            backend.updateOccupation(occupied) 

        if num == 15 and air.hasValues():
            backend.updateEnvironmentData(occupied, air.temperature, air.humidity)
            num = 0

        sleep(1)

except KeyboardInterrupt:
    occupation.stop()
    air.stop()
    loudness.stop()

# for entry in loudness.history:
#    print("{time:07}: {value: >3}".format(time=entry[0], value=entry[1]))

import threading
from time import sleep
import collections
import requests
import json
import argparse
import configparser
from sensors.sensors import Sensors
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
config.read("config.ini")
# TODO: make dynamic
# TODO: validate
# TODO: make sensor ports configurable

print("Started kckr for location: %s" % (config["device"]["location"]))

sensors = Sensors()
backend = Backend(config)

try:
    num = 0
    occupied = None
    sensors.start()

    while True:
        print("Occupied     %s" % (sensors.occupation.isOccupied))
        if sensors.air.hasValues():
            print("Temperature  %.02f°C" % (sensors.air.temperature))
            print("Humidity     %.02f%%" % (sensors.air.humidity))
        num += 1

        if occupied != sensors.occupation.isOccupied:
            occupied = sensors.occupation.isOccupied
            backend.updateOccupation(occupied)

        if num == 15 and sensors.air.hasValues():
            backend.updateEnvironmentData(
                occupied, sensors.air.temperature, sensors.air.humidity)
            num = 0

        sleep(1)

except KeyboardInterrupt:
    sensors.stop()

# for entry in loudness.history:
#    print("{time:07}: {value: >3}".format(time=entry[0], value=entry[1]))

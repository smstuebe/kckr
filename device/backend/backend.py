import requests
import sys

class Backend:
    def __init__(self, config):
        self.config = config

    def updateOccupation(self, occupied):
        print("Occupation changed: %s" % (occupied))
        try:
            url = "https://%s/api/InsertOccupation?code=%s" % (self.config["backend"]["fn-base-url"], self.config["backend"]["occupation-fn-key"])
            requests.post(url, json={
                "Location": self.config["device"]["location"],
                "Occupied": occupied
            })
        except BaseException as ex:
            print("[backend] " + str(ex), file=sys.stderr)

    def updateEnvironmentData(self, occupied, temp, humidity):
        print("Sending environment data: %s %.02f°C %.02f%%" % (occupied, temp, humidity))
        try:
            url = "https://%s/api/InsertEnvironmentData?code=%s" % (self.config["backend"]["fn-base-url"], self.config["backend"]["environment-fn-key"])
            requests.post(url, json={
                "Location": self.config["device"]["location"],
                "Occupied": occupied,
                "Temperature": temp,
                "Humidity": humidity
            })
        except BaseException as ex:
            print("[backend] " + str(ex), file=sys.stderr)
                


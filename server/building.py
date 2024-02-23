from time import time

from flask import request


def buildingSync():

    data = request.data
    data = {
        "ts": round(time()),
        "playerDataDelta": {
            "modified": {
                "building": {},
                "event": {
                    "building": round(time()) + 3000
                }
            },
            "deleted": {}
        }
    }
    return data


from flask import request

from constants import USER_JSON_PATH
from utils import read_json, write_json


def deepSeaBranch():

    data = request.data
    request_data = request.get_json()["branches"]
    techTrees = {branch["techTreeId"]: {"branch": branch["branchId"], "state": 2} for branch in request_data}

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["deepSea"]["techTrees"] = techTrees
    write_json(saved_data, USER_JSON_PATH)

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "deepSea": {
                    "techTrees": techTrees
                }
            }
        }
    }

    return data


def deepSeaEvent():

    data = request.data
    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

    return data

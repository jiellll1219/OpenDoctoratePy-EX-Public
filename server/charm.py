from flask import request

from constants import USER_JSON_PATH
from utils import read_json, write_json, run_after_response


def charmSetSquad():

    data = request.data
    charm_squad = request.get_json()["squad"]

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["charm"]["squad"] = charm_squad
    run_after_response(write_json ,saved_data, USER_JSON_PATH)

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "charm": {
                    "squad": charm_squad
                }
            }
        }
    }

    return data


from flask import request
from utils import read_json, write_json 
from constants import USER_JSON_PATH, SYNC_DATA_TEMPLATE_PATH


def backgroundSetBackground():

    data = request.data
    request_data = request.get_json()
    player_data = read_json(USER_JSON_PATH, encoding="utf-8")
    player_data["user"]["background"]["selected"] = request_data["bgID"]
    write_json(player_data, SYNC_DATA_TEMPLATE_PATH)

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "background": {
                    "selected": request_data["bgID"]
                }
            }
        }
    }
    return data


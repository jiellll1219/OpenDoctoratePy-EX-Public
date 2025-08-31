from flask import request
from utils import read_json, write_json 
from constants import USER_JSON_PATH, SYNC_DATA_TEMPLATE_PATH, CONFIG_PATH


def SetBackground():

    data = request.data
    request_data = request.get_json()
    player_data = read_json(USER_JSON_PATH)
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

def homeThemeChange():
    request_data = request.get_json()

    themeId = request_data["themeId"]

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {"homeTheme": {"selected": themeId}},
        }
    }

    config = read_json(CONFIG_PATH)
    config["userConfig"]["theme"] = themeId

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["homeTheme"]["selected"] = themeId
    write_json(saved_data, USER_JSON_PATH)
    write_json(config, CONFIG_PATH)

    return data

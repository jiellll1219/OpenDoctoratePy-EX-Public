import json
from flask import request
from constants import USER_JSON_PATH, CONFIG_PATH
from utils import read_json, write_json


def setAssistCharList():
    try:
        request_data = request.get_json()
        charInstId = request_data.get("assistCharList")[-1].get("charInstId")
        user_data = read_json(USER_JSON_PATH)
        config = read_json(CONFIG_PATH)
        config["charConfig"]["assistUnit"] = {
            "charId": user_data["user"]["troop"]["chars"].get(str(charInstId), {}).get("charId"),
            "skinId": user_data["user"]["troop"]["chars"].get(str(charInstId), {}).get("skin"),
            "skillIndex": request_data.get("assistCharList")[-1].get("skillIndex"),
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        data = {"playerDataDelta":{"modified":{"social":{"assistCharList":request_data.get("assistCharList")}},"deleted":{}}}
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def getSortListInfo():

    data = {"playerDataDelta":{"deleted":{},"modified":{}},"result":[]}

    return data

def getFriendList():
    
    data = request.data

    return {}

def searchPlayer():

    data = {"list": [], "request": []}

    return data

def getFriendRequestList():

    data = request.data

    return data

def processFriendRequest():

    data = request.data

    return data

def sendFriendRequest():

    data = request.data

    return data

def setFriendAlias():

    data = request.data

    return data

def deleteFriend():
    
    data = request.data

    return data

def setCardShowMedal():
    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH)
    if "medalBoard" not in user_data["user"]["social"]:
        user_data["user"]["social"]["medalBoard"] = {}
    user_data["user"]["social"]["medalBoard"]["type"] = json_body["type"]
    user_data["user"]["social"]["medalBoard"]["template"] = json_body["templateGroup"]
    write_json(user_data, USER_JSON_PATH)

    return {
        "playerDataDelta": {
            "modified": {
                "social": {
                    "medalBoard": {
                        "type": json_body["type"],
                        "template": json_body["templateGroup"],
                    }
                }
            },
            "deleted": {},
        }
    }
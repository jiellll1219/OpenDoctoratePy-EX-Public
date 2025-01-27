import json
from flask import request
from constants import USER_JSON_PATH, CONFIG_PATH
from utils import read_json, write_json


def socialsetAssistCharList():
    try:
        request_data = request.get_json()
        charInstId = request_data.get("assistCharList")[-1].get("charInstId")
        user_data = read_json(USER_JSON_PATH, encoding="utf-8")
        config = read_json(CONFIG_PATH, encoding="utf-8")
        config["charConfig"]["assistUnit"] = {
            "charId": user_data["user"]["troop"]["chars"].get(str(charInstId), {}).get("charId"),
            "skinId": user_data["user"]["troop"]["chars"].get(str(charInstId), {}).get("skin"),
            "skillIndex": request_data.get("assistCharList")[-1].get("skillIndex"),
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        data = {"playerDataDelta":{"modified":{"social":{"assistCharList":request_data.get("assistCharList")}},"deleted":{}}}
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def socialgetSortListInfo():

    data = {"playerDataDelta":{"deleted":{},"modified":{}},"result":[]}

    return data

def socialgetFriendList():
    
    data = request.data

    return data

def socialsearchPlayer():

    data = {"list": [], "request": []}

    return data

def socialgetFriendRequestList():

    data = request.data

    return data

def socialprocessFriendRequest():

    data = request.data

    return data

def socialsendFriendRequest():

    data = request.data

    return data

def socialsetFriendAlias():

    data = request.data

    return data

def socialdeleteFriend():
    
    data = request.data

    return data
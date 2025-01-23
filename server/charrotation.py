from utils import read_json, write_json
from flask import request
from constants import SYNC_DATA_TEMPLATE_PATH, USER_JSON_PATH, CONFIG_PATH
import re

def setCurrent():
    json_body = request.get_json()
    target_instid = str(json_body["instId"])
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf8")

    user_json_data["user"]["charRotation"]["current"] = sync_data["user"]["charRotation"]["current"] = target_instid
    profile = sync_data["user"]["charRotation"]["preset"][target_instid]["profile"]

    for slots in sync_data["user"]["charRotation"]["preset"][target_instid]["slots"]:
        if slots.get("skinId") == profile:
            charid = slots.get("charId")
            break

    user_json_data["user"]["status"]["secretary"] = sync_data["user"]["status"]["secretary"] = charid
    user_json_data["user"]["status"]["secretarySkinId"] = sync_data["user"]["status"]["secretarySkinId"] = sync_data["user"]["charRotation"]["preset"][target_instid]["profile"]
    user_json_data["user"]["background"]["selected"] = sync_data["user"]["background"]["selected"] = sync_data["user"]["charRotation"]["preset"][target_instid]["background"]
    user_json_data["user"]["homeTheme"]["selected"] = sync_data["user"]["homeTheme"]["selected"] = sync_data["user"]["charRotation"]["preset"][target_instid]["homeTheme"]

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    write_json(user_json_data, USER_JSON_PATH, encoding="utf8")

    return {
        "playerDataDelta": {
            "modified": {
                "charRotation": {
                    "current": target_instid
                },
                "status": {
                    "secretary": sync_data["user"]["status"]["secretary"],
                    "secretarySkinId": sync_data["user"]["status"]["secretarySkinId"]
                },
                "background": {
                    "selected": sync_data["user"]["background"]["selected"]
                },
                "homeTheme": {
                    "selected": sync_data["user"]["homeTheme"]["selected"]
                },
            },
            "deleted": {}
        },
        "pushMessage": [],
    }

def createPreset():

    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    charrotation_data = sync_data["user"]["charRotation"]
    user_data = read_json(USER_JSON_PATH, encoding="utf8")
    defult_preset_data = {
        "background": "bg_rhodes_day",
        "homeTheme": "tm_rhodes_day",
        "name": "unname",
        "profile": "char_171_bldsk@witch#1",
        "profileInst": "171",
        "slots": [
            {
                "charId": "char_171_bldsk",
                "skinId": "char_171_bldsk@witch#1"
            }
        ]
    }

    new_id = str(len(charrotation_data["preset"]) + 1)
    if new_id not in charrotation_data["preset"]:
        sync_data["user"]["charRotation"]["preset"][new_id] = charrotation_data["preset"][new_id] = {}
    sync_data["user"]["charRotation"]["preset"][new_id] = charrotation_data["preset"][new_id] = defult_preset_data

    sync_data["user"]["charRotation"] = user_data["user"]["charRotation"] = charrotation_data
    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    write_json(user_data, USER_JSON_PATH, encoding="utf8")

    return {
        "playerDataDelta": {
            "modified": {
                "charRotation": charrotation_data
            },
            "deleted": {}
        },
        "pushMessage": [],
        "instId": 2,
    }

def deletePreset():
    json_body = request.get_json()
    target_instid = json_body["instId"]
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf8")

    sync_data["user"]["charRotation"]["preset"].pop(target_instid)
    user_json_data["user"]["charRotation"]["preset"].pop(target_instid)

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    write_json(user_json_data, USER_JSON_PATH, encoding="utf8")

    return {
        "playerDataDelta": {
            "modified": {},
            "deleted": {
                "charRotation": {
                    "preset": target_instid
                } 
            }
        },
        "pushMessage": []
    }

def updatePreset():
    json_body = request.get_json()
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf8")
    config = read_json(CONFIG_PATH, encoding="utf8")
    inst_id = json_body.get("instId")
    result = {
        "playerDataDelta": {
            "modified": {
                "charRotation": sync_data["user"]["charRotation"]
            },
            "deleted": {}
        },
        "pushMessage": [],
        "result": 0
    }

    preset_data = sync_data["user"]["charRotation"]["preset"][inst_id]
    for key, value in json_body["data"].items():
        if value is not None:
            preset_data[key] = value

    if json_body.get("data", {}).get("background") is not None:
        try:
            config["userConfig"]["background"] = json_body["data"]["background"]
        except:
            pass
        result["playerDataDelta"]["modified"]["background"] = {}
        result["playerDataDelta"]["modified"]["background"]["selected"] = ""
        result["playerDataDelta"]["modified"]["background"]["selected"] = sync_data["user"]["background"]["selected"] = json_body["data"]["homeTheme"]

    if json_body.get("data", {}).get("homeTheme") is not None:
        try:
            config["userConfig"]["theme"] = json_body["data"]["homeTheme"]
        except:
            pass
        result["playerDataDelta"]["modified"]["homeTheme"] = {}
        result["playerDataDelta"]["modified"]["homeTheme"]["selected"] = ""
        result["playerDataDelta"]["modified"]["homeTheme"]["selected"] = sync_data["user"]["homeTheme"]["selected"] = json_body["data"]["homeTheme"]

    if json_body.get("data", {}).get("profile") is not None:
        try:
            str_char = re.search(r'([^@]+)@', json_body["data"]["profile"])
            config["userConfig"]["secretary"] = str_char.group(1)
            config["userConfig"]["secretarySkinId"] = json_body["data"]["profile"]
        except:
            pass
        result["playerDataDelta"]["modified"]["status"] = {}
        result["playerDataDelta"]["modified"]["status"]["secretary"] = ""
        result["playerDataDelta"]["modified"]["status"]["secretary"] = sync_data["user"]["status"]["secretary"] = str_char.group(1)
        result["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = ""
        result["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = sync_data["user"]["profile"]["secretarySkinId"] = json_body["data"]["profile"]

    user_json_data["user"]["charRotation"] = sync_data["user"]["charRotation"]

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_json_data, USER_JSON_PATH)
    write_json(config, CONFIG_PATH)
    
    return result
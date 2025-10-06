from utils import read_json, write_json
from flask import request
from constants import SYNC_DATA_TEMPLATE_PATH
import re

def setCurrent():
    json_body = request.get_json()
    target_instid = str(json_body["instId"])
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    sync_data["user"]["charRotation"]["current"] = target_instid
    profile = sync_data["user"]["charRotation"]["preset"][target_instid]["profile"]

    for slots in sync_data["user"]["charRotation"]["preset"][target_instid]["slots"]:
        if slots["skinId"] == profile:
            charid = slots["charId"]
            break

    sync_data["user"]["status"]["secretary"] = charid
    sync_data["user"]["status"]["secretarySkinId"] = sync_data["user"]["charRotation"]["preset"][target_instid]["profile"]
    sync_data["user"]["background"]["selected"] = sync_data["user"]["charRotation"]["preset"][target_instid]["background"]
    sync_data["user"]["homeTheme"]["selected"] = sync_data["user"]["charRotation"]["preset"][target_instid]["homeTheme"]

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)

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

    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    charrotation_data = sync_data["user"]["charRotation"]
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

    sync_data["user"]["charRotation"] = charrotation_data
    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)

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
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    sync_data["user"]["charRotation"]["preset"].pop(target_instid)

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)

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

    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    inst_id = json_body["instId"]
    result = {
        "playerDataDelta": {
            "modified": {
                "charRotation": {}
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

    if json_body["data"]["background"] is not None:

        sync_data["user"]["charRotation"]["preset"][inst_id]["background"] = json_body["data"]["background"]
        result["playerDataDelta"]["modified"]["background"] = {}
        result["playerDataDelta"]["modified"]["background"]["selected"] = ""
        result["playerDataDelta"]["modified"]["background"]["selected"] = sync_data["user"]["background"]["selected"] = json_body["data"]["background"]

    if json_body["data"]["homeTheme"] is not None:

        sync_data["user"]["charRotation"]["preset"][inst_id]["homeTheme"] = json_body["data"]["homeTheme"]
        result["playerDataDelta"]["modified"]["homeTheme"] = {}
        result["playerDataDelta"]["modified"]["homeTheme"]["selected"] = ""
        result["playerDataDelta"]["modified"]["homeTheme"]["selected"] = sync_data["user"]["homeTheme"]["selected"] = json_body["data"]["homeTheme"]

    if json_body["data"]["profile"] is not None:
        str_char = re.search(r'^[^@#]+', json_body["data"]["profile"])

        sync_data["user"]["charRotation"]["preset"][inst_id]["profile"] = json_body["data"]["profile"]
        result["playerDataDelta"]["modified"]["status"] = {}
        result["playerDataDelta"]["modified"]["status"]["secretary"] = ""
        result["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = ""
        result["playerDataDelta"]["modified"]["status"]["profileInst"] = ""

        result["playerDataDelta"]["modified"]["status"]["secretary"] = sync_data["user"]["status"]["secretary"] = str_char.group(0)
        result["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = sync_data["user"]["status"]["secretarySkinId"] = json_body["data"]["profile"]
        sync_data["user"]["charRotation"]["preset"][inst_id]["slots"] = json_body["data"]["slots"]
        sync_data["user"]["charRotation"]["profileInst"]  = sync_data["user"]["status"]["profileInst"] = json_body["data"]["profileInst"]

    result["playerDataDelta"]["modified"]["charRotation"] = sync_data["user"]["charRotation"]

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)
    
    return result

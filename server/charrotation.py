from utils import read_json, write_json
from flask import request
from constants import SYNC_DATA_TEMPLATE_PATH, USER_JSON_PATH, CONFIG_PATH
import json

def setCurrent():
    json_body = request.get_json()
    target_instid = json_body["instId"]
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf8")

    sync_data["user"]["charRotation"]["current"] = target_instid
    user_json_data["user"]["charRotation"]["current"] = target_instid
    target_instid_data = sync_data["user"]["charRotation"]["presets"][target_instid]

    profile_str = target_instid_data["profile"]
    user_json_data["user"]["status"]["secretary"] = sync_data["user"]["status"]["secretary"] = profile_str.split('@')[0]
    user_json_data["user"]["status"]["secretarySkinId"] = sync_data["user"]["status"]["secretarySkinId"] = target_instid_data["profile"]
    user_json_data["user"]["background"]["selected"] = sync_data["user"]["background"]["selected"] = target_instid_data["background"]
    user_json_data["user"]["homeTheme"]["selected"] = sync_data["user"]["homeTheme"]["selected"] = target_instid_data["homeTheme"]

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    write_json(user_json_data, USER_JSON_PATH, encoding="utf8")

    return {
        "playerDataDelta": {
            "modified": {
                "charRotation": {
                    "current": ""
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
    json_body = request.get_json()

    charrotation_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")["user"]["charRotation"]
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

    new_id = str(len(charrotation_data["presets"]) + 1)
    charrotation_data["presets"][new_id].append(defult_preset_data)

    user_data["user"]["charRotation"] = charrotation_data
    write_json(charrotation_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")

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

    sync_data["user"]["charRotation"]["presets"].pop(target_instid)
    user_json_data["user"]["charRotation"]["presets"].pop(target_instid)

    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    write_json(user_json_data, USER_JSON_PATH, encoding="utf8")

    return {
        "playerDataDelta": {
            "modified": {
                "charRotation": sync_data["user"]["charRotation"],
            }
        },
        "pushMessage": [],
        "result": 0
    }

def updatePreset():
    json_body = request.get_json()
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf8")
    config = read_json(CONFIG_PATH, encoding="utf8")
    charrotation_data = sync_data["user"]["charRotation"]

    # 获取报文的 instId
    inst_id = json_body.get("instId")
    # 从 charrotation_data 中获取对应的 preset 数据
    preset_data = charrotation_data.get("charRotation", {}).get("preset", {}).get(inst_id)
    # 更新数据
    for key, value in preset_data.items():
        if value is not None:
            json_body["data"][key] = value  # 更新请求的 data 部分

    user_json_data["user"]["charRotation"] = sync_data["user"]["charRotation"]
    write_json(sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_json_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "charRotation": sync_data["user"]["charRotation"]["preset"],
                "status": {
                    "secretary": config["userConfig"]["secretary"],
                    "secretatySkinId": config["userConfig"]["secretarySkinId"]
                }
            },
            "deleted": {}
        },
        "pushMessage": [],
        "result": "@@@SUC@@@"
    }

    json_str = json.dumps(result, indent=4)
    return json_str.replace('"@@@SUC@@@"', 'SUCCESS')
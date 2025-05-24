from flask import request
from constants import SYNC_DATA_TEMPLATE_PATH
from utils import read_json, write_json, decrypt_battle_data, run_after_response
from quest import questBattleStart
from virtualtime import time
import json

def getSeasonRecord():
    json_body = request.get_json()
    # print (json_body)
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    stage_info = {}

    for keys in sync_data["user"]["dungeon"]["stages"].keys():
        if keys.startswith("act1break_0") or keys.startswith("act1break_1"):
            one_stage_info = {
                keys: {
                    "stageId": keys,
                    "state": "COMPLETE"
                }
            }
            stage_info.update(one_stage_info)
        elif keys.startswith("act1break_sp"):
            one_stage_info = {
                keys: {
                    "stageId": keys,
                    "state": "PLAYED"
                }
            }
            stage_info.update(one_stage_info)

    squad = sync_data["user"]["troop"]["squads"]["0"]["slots"]

    result = {
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        },
        "pushMessage": [],
        "seasons": {
            "act1break": {
                "bestRecord": {
                    "stageId": "act1break_12",
                    "buff": [],
                    "showTs": time(),
                    "squad": [],
                    "assistChar": {}
                },
                "stageInfo": stage_info
            }
        }
    }

    return result

def rewardAllMilestone():
    json_body = request.get_json()
    print (json_body)

    return {}

def rewardMilestone():
    json_body = request.get_json()
    print (json_body)

    return {}

def vecV2changeBuffList():
    json_body = request.get_json()
    # {"activityId": "act1break", "buffList": ["act1break_rune01", "act1break_rune04"]}

    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    activity_id = json_body["activityId"]
    buff_list = json_body["buffList"]

    activity_data = sync_data["user"]["activity"]["VEC_BREAK_V2"][activity_id]
    activity_data["activatedBuff"] = buff_list

    result = {
        "PlayerDataDelta": {
            "modified": {
                "activity": {
                    "VEC_BREAK_V2":{
                        activity_id: activity_data
                    }
                    
                }
            },
            "deleted": {},
        }
    }

    run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
    return result

def defendBattleStart():
    json_body = request.get_json()
    # {
    #     "activityId": "act1break",
    #     "stageId": "act1break_sp02",
    #     "squad": {
    #         "squadId": "",
    #         "name": "",
    #         "slots": [
    #             {
    #                 "charInstId": 4133,
    #                 "skillIndex": 2,
    #                 "currentEquip": "uniequip_002_logos"
    #             }
    #         ]
    #     }
    # }
    global battle_data
    battle_data = json_body
    result = questBattleStart()

    return result

def defendBattleFinish():
    json_body = request.get_json()
    global battle_data
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    # battle_data = json_body["data"]
    # decrypt_data = decrypt_battle_data(battle_data)

    # 基础信息
    activity_data_id = battle_data["activityId"]
    slots_data = battle_data["squad"]["slots"]
    stage_id = battle_data["stageId"]
    activity_data = sync_data["user"]["activity"]["VEC_BREAK_V2"][activity_data_id]

    # 通关信息更新
    defend_stages_data = activity_data["defendStages"].get(stage_id)
    if defend_stages_data is None:
        defend_squad = [
            {
                "charInstId": slot["charInstId"],
                "currentTmpl": None
            }
            for slot in slots_data
        ]
        defend_stages_data = {
            "stageId": stage_id,
            "defendSquad": defend_squad,
            "recvTimeLimited": True,
            "recvNormal": True
        }
        activity_data["defendStages"][stage_id] = defend_stages_data
        activated_buff = activity_data["activatedBuff"]
        activated_buff.append(stage_id)
    else:
        pass

    # 等级点数
    ponit = activity_data["milestone"]["point"]

    #构建响应内容
    result = {
        "PlayerDataDelta": {
            "modified": {
                "activity": {
                    "VEC_BREAK_V2": {
                        activity_data_id: {
                            "milestone": {
                                "point": ponit
                            },
                            "defendStages": {
                                stage_id: defend_stages_data
                            }
                        }
                    }
                }
            }
        },
        "pushMessage": [],
        "result": 0,
        "apFailReturn": 0,
        "goldScale": 0.0,
        "expScale": 0.0,
        "suggestFriend": False,
        "msBefore": ponit,
        "msAfter": ponit,
        "finTs": time()
    }

    battle_data = None
    run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
    return result

def setDefend():
    # 换驻防编队、清空驻防编队
    json_body = request.get_json()
    #{"activityId": "act1break", "stageId": "act1break_sp02", "squadSlots": [{"charInstId": 4133}]}
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    activity_data = sync_data["user"]["activity"]["VEC_BREAK_V2"][json_body["activityId"]]
    stage_id = json_body["stageId"]
    squad_slots = json_body["squadSlots"]

    activity_data["defendStages"][stage_id]["defendSquad"] = squad_slots

    result = {
        "PlayerDataDelta": {
            "modified": {
                "activity": {
                    "VEC_BREAK_V2": {
                        json_body["activityId"]: {
                            "defendStages": {
                                stage_id: {
                                    "defendSquad": squad_slots
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
    return result

def vecV2BattleStart():
    json_body = request.get_json()

    global battle_data
    battle_data = json_body
    result = questBattleStart()

    return result

def vecV2battleFinish():
    json_body = request.get_json()
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    global battle_data

    # battle_data = json_body["data"]
    # decrypt_data = decrypt_battle_data(battle_data)

    activity_data_id = battle_data["activityId"]
    activity_data = sync_data["user"]["activity"]["VEC_BREAK_V2"][activity_data_id]
    ponit = activity_data["milestone"]["point"]

    result = {
        "playerDataDelta": {},
        "pushMessage": [],
        "result": 0,
        "apFailReturn": 0,
        "goldScale": 0.0,
        "expScale": 0.0,
        "suggestFriend": False,
        "msBefore": ponit,
        "msAfter": ponit,
        "finTs": time()
    }

    battle_data = None
    return result
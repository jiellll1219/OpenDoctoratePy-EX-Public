from time import time

from flask import request

from constants import BATTLE_REPLAY_JSON_PATH, USER_JSON_PATH, CONFIG_PATH
from utils import read_json, write_json


def questBattleStart():

    data = request.data
    request_data = request.get_json()
    data = {
        "apFailReturn": 0,
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        "inApProtectPeriod": False,
        "isApProtect": 0,
        "notifyPowerScoreNotEnoughIfFailed": False,
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0
    }

    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)
    replay_data["current"] = request_data["stageId"]
    write_json(replay_data, BATTLE_REPLAY_JSON_PATH)

    return data


def questBattleFinish():

    data = request.data
    data = {
        "result":0,
        "apFailReturn": 0,
        "expScale": 1.2,
        "goldScale": 1.2,
        "rewards": [],
        "firstRewards": [],
        "unlockStages": [],
        "unusualRewards": [],
        "additionalRewards": [],
        "furnitureRewards": [],
        "alert": [],
        "suggestFriend": False,
        "pryResult": [],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def questSaveBattleReplay():

    data = request.data
    request_data = request.get_json()

    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)

    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {
                "dungeon": {
                    "stages": {
                        replay_data["current"]: {
                            "hasBattleReplay": 1
                        }
                    }
                }
            },
            "deleted": {}
        }
    }

    char_config = replay_data["currentCharConfig"]

    if char_config in list(replay_data["saved"].keys()):
        replay_data["saved"][char_config].update({
            replay_data["current"]: request_data["battleReplay"]
        })
    else:
        replay_data["saved"].update({
            char_config: {
                replay_data["current"]: request_data["battleReplay"]
            }
        })
    replay_data["current"] = None
    write_json(replay_data, BATTLE_REPLAY_JSON_PATH)

    return data


def questGetBattleReplay():

    data = request.data
    stageId = request.get_json()["stageId"]

    replay_data = read_json(BATTLE_REPLAY_JSON_PATH)
    battleData = {
        "battleReplay": replay_data["saved"][replay_data["currentCharConfig"]][stageId],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }
    
    return battleData


def questChangeSquadName():

    data = request.data
    request_data = request.get_json()
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "squads":{}
                }
            },
            "deleted":{}
        }
    }

    if request_data["squadId"] and request_data["name"]:
        data["playerDataDelta"]["modified"]["troop"]["squads"].update({
            str(request_data["squadId"]): {
                "name": request_data["name"]
            }
        })

        saved_data = read_json(USER_JSON_PATH)
        saved_data["user"]["troop"]["squads"][str(request_data["squadId"])]["name"] = request_data["name"]
        write_json(saved_data, USER_JSON_PATH)

        return data


def questSquadFormation():

    data = request.data
    request_data = request.get_json()
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "squads":{}
                }
            },
            "deleted":{}
        }
    }

    if request_data["squadId"] and request_data["slots"]:
        data["playerDataDelta"]["modified"]["troop"]["squads"].update({
            str(request_data["squadId"]): {
                "slots": request_data["slots"]
            }
        })

        saved_data = read_json(USER_JSON_PATH)
        saved_data["user"]["troop"]["squads"][str(request_data["squadId"])]["slots"] = request_data["slots"]
        write_json(saved_data, USER_JSON_PATH)

        return data


def questGetAssistList():

    data = request.data
    assist_unit_config = read_json(CONFIG_PATH)["charConfig"]["assistUnit"]
    saved_data = read_json(USER_JSON_PATH)["user"]["troop"]["chars"]
    assist_unit = {}

    for _, char in saved_data.items():
        if char["charId"] == assist_unit_config["charId"]:
            assist_unit.update({
                "charId": char["charId"],
                "skinId": assist_unit_config["skinId"],
                "skills": char["skills"],
                "mainSkillLvl": char["mainSkillLvl"],
                "skillIndex": assist_unit_config["skillIndex"],
                "evolvePhase": char["evolvePhase"],
                "favorPoint": char["favorPoint"],
                "potentialRank": char["potentialRank"],
                "level": char["level"],
                "crisisRecord": {},
                "currentEquip": char["currentEquip"],
                "equip": char["equip"]
            })
            break

    data = {
        "allowAskTs": int(time()),
        "assistList": [
            {
                "uid": "88888888",
                "aliasName": "",
                "nickName": "ABCDEF",
                "nickNumber": "8888",
                "level": 200,
                "avatarId": "0",
                "avatar": {
                    "type": "ASSISTANT",
                    "id": "char_421_crow#1"
                },
                "lastOnlineTime": int(time()),
                "assistCharList": [
                    assist_unit
                ],
                "powerScore": 500,
                "isFriend": True,
                "canRequestFriend": False,
                "assistSlotIndex": 0
            }
        ],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def markStoryAcceKnown():
    return {"playerDataDelta": {"modified": {"storyreview": {"tags": {"knownStoryAcceleration": 1}}}, "deleted": {}}}


def confirmBattleCar():
    return {
        "playerDataDelta": {
            "modified": {
                "car": {
                    "battleCar": request.get_json()["car"]
                }
            },
            "deleted": {}
        }
    }

def typeAct20side_competitionStart():
    return {"result": 0, "battleId": "abcdefgh-1234-5678-a1b2c3d4e5f6", "playerDataDelta": {"modified": {}, "deleted": {}}}


def typeAct20side_competitionFinish():
    return {"performance": 0, "expression": 0, "operation": 0, "total": 0, "level": "B", "isNew": False, "playerDataDelta": {"modified": {}, "deleted": {}}}

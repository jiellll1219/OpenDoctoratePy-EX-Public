from time import time

from flask import request

from constants import CONFIG_PATH, CRISIS_JSON_BASE_PATH, RUNE_JSON_PATH
from utils import read_json, write_json


def crisisGetCrisisInfo():

    data = request.data
    selected_crisis = read_json(CONFIG_PATH)["crisisConfig"]["selectedCrisis"]

    if selected_crisis:
        rune = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf-8")
        current_time = round(time())
        next_day = round(time()) + 86400

        rune["ts"] = current_time
        rune["playerDataDelta"]["modified"]["crisis"]["lst"] = current_time
        rune["playerDataDelta"]["modified"]["crisis"]["nst"] = next_day
        rune["playerDataDelta"]["modified"]["crisis"]["training"]["nst"] = next_day

        for i in rune["playerDataDelta"]["modified"]["crisis"]["season"]:
            rune["playerDataDelta"]["modified"]["crisis"]["season"][i]["temporary"] = {
                "schedule": "rg1",
                "nst": next_day,
                "point": -1,
                "challenge": {
                    "taskList": {
                        "dailyTask_1": {
                            "fts": -1,
                            "rts": -1
                        }
                    },
                    "topPoint": -1,
                    "pointList": {
                        "0": -1,
                        "1": -1,
                        "2": -1,
                        "3": -1,
                        "4": -1,
                        "5": -1,
                        "6": -1,
                        "7": -1,
                        "8": -1
                    }
                }
            }
    else:
        rune = {
            "ts": round(time()),
            "data": {},
            "playerDataDelta": {}
        }

    return rune


def crisisBattleStart():

    data = request.data
    data = request.get_json()
    selected_crisis = read_json(CONFIG_PATH)["crisisConfig"]["selectedCrisis"]
    rune_data = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf8")["data"]["stageRune"][data["stageId"]]

    total_risks = 0
    for each_rune in data["rune"]:
        total_risks += rune_data[each_rune]["points"]

    write_json({
        "chosenCrisis": selected_crisis,
        "chosenRisks": data["rune"],
        "totalRisks": total_risks
    }, RUNE_JSON_PATH)
    
    data = {
        'battleId': 'abcdefgh-1234-5678-a1b2c3d4e5f6',
        'playerDataDelta': {
            'modified': {},
            'deleted': {}
        },
        'result': 0,
        'sign': "abcde",
        'signStr': "abcdefg"
    }

    return data


def crisisBattleFinish():

    total_risks = read_json(RUNE_JSON_PATH)["totalRisks"]

    data = request.data
    data = {
        "result": 0,
        "score": total_risks,
        "updateInfo": {
            "point": {
                "before": -1,
                "after": total_risks
            }
        },
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


from virtualtime import time

from flask import request

from constants import CONFIG_PATH, CRISIS_JSON_BASE_PATH, CRISIS_V2_JSON_BASE_PATH, RUNE_JSON_PATH, SHOP_PATH
from utils import read_json, write_json


def crisisGetCrisisInfo():

    data = request.data
    selected_crisis = read_json(CONFIG_PATH)["crisisConfig"]["selectedCrisis"]

    if selected_crisis:
        rune = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf-8")
        current_time = time()
        next_day = time() + 86400

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
            "ts": time(),
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

def crisisV2_getInfo():
    selected_crisis = read_json(CONFIG_PATH)["crisisV2Config"]["selectedCrisis"]
    if selected_crisis:
        rune = read_json(
            f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf-8"
        )
    else:
        rune = {
            "info": {},
            "ts": time() - 10,
            "playerDataDelta": {"modified": {}, "deleted": {}},
        }
    return rune


def crisisV2_battleStart():
    request_data = request.get_json()
    battle_data = {
        "mapId": request_data["mapId"],
        "runeSlots": request_data["runeSlots"],
    }
    write_json(battle_data, RUNE_JSON_PATH)
    return {
        "result": 0,
        "battleId": "abcdefgh-1234-5678-a1b2c3d4e5f6",
        "playerDataDelta": {"modified": {}, "deleted": {}},
    }


def crisisV2_battleFinish():
    battle_data = read_json(RUNE_JSON_PATH)
    mapId = battle_data["mapId"]
    runeSlots = battle_data["runeSlots"]
    scoreCurrent = [0, 0, 0, 0, 0, 0]
    selected_crisis = read_json(CONFIG_PATH)["crisisV2Config"]["selectedCrisis"]
    rune = read_json(
        f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json", encoding="utf-8"
    )

    nodes = {}
    for slot in rune["info"]["mapDetailDataMap"][mapId]["nodeDataMap"]:
        if not slot.startswith("node_"):
            continue
        nodeData = rune["info"]["mapDetailDataMap"][mapId]["nodeDataMap"][slot]
        slotPackId = nodeData["slotPackId"]
        if not slotPackId:
            continue
        if slotPackId not in nodes:
            nodes[slotPackId] = {}
        if nodeData["mutualExclusionGroup"]:
            mutualExclusionGroup = nodeData["mutualExclusionGroup"]
        else:
            mutualExclusionGroup = slot
        if mutualExclusionGroup not in nodes[slotPackId]:
            nodes[slotPackId][mutualExclusionGroup] = {}
        if "runeId" in nodeData:
            runeId = rune["info"]["mapDetailDataMap"][mapId]["nodeDataMap"][slot][
                "runeId"
            ]
            if runeId:
                runeData = rune["info"]["mapDetailDataMap"][mapId]["runeDataMap"][
                    runeId
                ]
                score = runeData["score"]
            else:
                score = 0
        else:
            score = 0
        nodes[slotPackId][mutualExclusionGroup][slot] = score

    slots = set(runeSlots)
    for slotPackId in nodes:
        flag = True
        for mutualExclusionGroup in nodes[slotPackId]:
            score_max = 0
            for slot in nodes[slotPackId][mutualExclusionGroup]:
                score_max = max(
                    score_max, nodes[slotPackId][mutualExclusionGroup][slot]
                )
            flag2 = False
            for slot in nodes[slotPackId][mutualExclusionGroup]:
                if nodes[slotPackId][mutualExclusionGroup][slot] != score_max:
                    continue
                if slot in slots:
                    flag2 = True
                    break
            if not flag2:
                flag = False
                break
        if flag:
            bagData = rune["info"]["mapDetailDataMap"][mapId]["bagDataMap"][slotPackId]
            scoreCurrent[bagData["dimension"]] += bagData["rewardScore"]

    runeIds = []

    for slot in runeSlots:
        nodeData = rune["info"]["mapDetailDataMap"][mapId]["nodeDataMap"][slot]
        if "runeId" in nodeData:
            runeId = rune["info"]["mapDetailDataMap"][mapId]["nodeDataMap"][slot][
                "runeId"
            ]
            runeIds.append(runeId)
            runeData = rune["info"]["mapDetailDataMap"][mapId]["runeDataMap"][runeId]
            scoreCurrent[runeData["dimension"]] += runeData["score"]
    return {
        "result": 0,
        "mapId": mapId,
        "runeSlots": runeSlots,
        "runeIds": runeIds,
        "isNewRecord": False,
        "scoreRecord": [0, 0, 0, 0, 0, 0],
        "scoreCurrent": scoreCurrent,
        "runeCount": [0, 0],
        "commentNew": [],
        "commentOld": [],
        "ts": 1700000000,
        "playerDataDelta": {"modified": {}, "deleted": {}},
    }


def crisisV2_getSnapshot():
    return {
        "detail": {},
        "simple": {},
        "playerDataDelta": {"modified": {}, "deleted": {}},
    }

def crisisV2_getGoodList():

    result = read_json(SHOP_PATH, encoding="utf-8")["crisisV2"]

    return result

def crisisV2_confirmMissions():
    # 未完成
    return {
        "pushMessage": [],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }
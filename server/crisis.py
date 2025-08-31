from virtualtime import time

from flask import request

from constants import CONFIG_PATH, CRISIS_JSON_BASE_PATH, CRISIS_V2_JSON_BASE_PATH, RUNE_JSON_PATH, SHOP_PATH, \
    USER_JSON_PATH, CRISIS_V2_TABLE_PATH
from utils import read_json, write_json, decrypt_battle_data


def crisisGetCrisisInfo():

    data = request.data
    selected_crisis = read_json(CONFIG_PATH)["crisisConfig"]["selectedCrisis"]

    if selected_crisis:
        rune = read_json(f"{CRISIS_JSON_BASE_PATH}{selected_crisis}.json")
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
            f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json"
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
        f"{CRISIS_V2_JSON_BASE_PATH}{selected_crisis}.json"
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

    result = read_json(SHOP_PATH)["crisisV2"]

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


def recalRune_battleStart():
    # 获取请求数据
    request_data = request.get_json()

    # 保存战斗数据到临时文件
    battle_data = {
        "seasonId": request_data["seasonId"],
        "stageId": request_data["stageId"],
        "runes": request_data["runes"],
        "slots": request_data["slots"],
        "assistFriend": request_data.get("assistFriend")
    }

    write_json(battle_data, RUNE_JSON_PATH)

    return {
        "result": 0,
        "battleId": "abcdefgh-1234-5678-a1b2c3d4e5f6",
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        },
    }


def recalRune_battleFinish():
    # 读取保存的战斗数据
    rune_data = read_json(RUNE_JSON_PATH)

    # 获取请求数据（虽然响应中没有直接使用，但实际可能需要处理）
    request_data = request.get_json()

    crisis_v2_table = read_json(CRISIS_V2_TABLE_PATH)

    # 获取当前关卡数据
    season_id = rune_data["seasonId"]
    stage_id = rune_data["stageId"]

    stage_data = crisis_v2_table["recalRuneData"]["seasons"][season_id]["stages"][stage_id]

    # 计算总分
    total_score = 0
    for rune_id in rune_data["runes"]:
        if rune_id in stage_data["runes"]:
            total_score += stage_data["runes"][rune_id]["score"]

    battle_data = decrypt_battle_data(request.json["data"])
    # 从战斗数据中提取关键信息
    complete_state = battle_data["completeState"]
    HP = battle_data["battleData"]["stats"]["leftHp"]

    is_completed = (complete_state == 3)

    # 从syncData获取用户当前进度
    user_data = read_json(USER_JSON_PATH)
    recal_Rune = user_data["user"]["recalRune"]

    # 检查是否是新记录
    current_record = recal_Rune["seasons"][season_id]["stage"][stage_id]["record"]
    is_new_record = is_completed and (total_score >= current_record)

    # 设置战斗状态：只有complete_state是3的时候代表战斗成功，设置为1，否则就是0
    battle_state = 1 if is_completed else 0

    # 获取当前存储的战斗状态
    current_battle_state = recal_Rune["seasons"][season_id]["stage"][stage_id].get("state", 0)

    # 战斗失败state为0的时候并不会影响本地已经为1的state
    # 如果当前状态已经是成功(1)，即使这次失败也不更新为失败状态
    if current_battle_state == 1 and battle_state == 0:
        battle_state = 1  # 保持成功状态

    # 只有当需要更新用户数据的时候才写入
    need_to_write = False
    # 只有当需要更新用户数据的时候才写入
    if is_new_record:
        recal_Rune["seasons"][season_id]["stage"][stage_id].update({
            "state": battle_state,
            "record": total_score,
            "runes": rune_data["runes"]
        })
        need_to_write = True
    else:
        # 即使不是新纪录，也要更新当前尝试的状态（如果之前没有记录）
        current_stage_data = recal_Rune["seasons"][season_id]["stage"][stage_id]
        if "state" not in current_stage_data or current_stage_data["state"] != battle_state:
            recal_Rune["seasons"][season_id]["stage"][stage_id]["state"] = battle_state
            need_to_write = True

    # 只有在需要更新数据时才写入文件
    if need_to_write:
        # 构建要更新的recalRune数据结构
        recalRune_update = {
            "state": battle_state,
            "record": total_score,
            "runes": rune_data["runes"]
        }

        # 更新用户数据
        user_data["user"]["recalRune"]["seasons"][season_id]["stage"][stage_id] = recalRune_update
        write_json(user_data, USER_JSON_PATH)

    # 构建响应
    response = {
        "seasonId": season_id,
        "stageId": stage_id,
        "state": battle_state,
        "score": total_score,
        "newRecord": is_new_record,
        "runes": rune_data["runes"],
        "hp": HP,  # 剩余生命值
        "ts": time(),
        "playerDataDelta": {
            "modified": {
                "recalRune": recal_Rune if need_to_write else {}
            },
            "deleted": {}
        }
    }

    return response
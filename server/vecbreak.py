from flask import request
from constants import SYNC_DATA_TEMPLATE_PATH, SERVER_DATA_PATH
from utils import read_json, write_json, decrypt_battle_data, run_after_response
from quest import questBattleStart
from virtualtime import time
import json

def getSeasonRecord():
    json_body = request.get_json()
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    server_data = read_json(SERVER_DATA_PATH)

    stage_info = {}

    for keys in sync_data["user"]["dungeon"]["stages"].keys():
        if keys.startswith("act1break_"):
            one_stage_info = {
                keys: {
                    "stageId": keys,
                    "state": "COMPLETE"
                }
            }
            stage_info.update(one_stage_info)

    buff = server_data["vecbreakV2"]["buff"]
    squad = server_data["vecbreakV2"]["squad"]
    assistChar = server_data["vecbreakV2"]["assistChar"]

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
                    "buff": buff,
                    "showTs": time(),
                    "squad": squad,
                    "assistChar": assistChar,
                },
                "stageInfo": stage_info
            }
        }
    }
    return result

def rewardAllMilestone():
    json_body = request.get_json()

    return {}

def rewardMilestone():
    json_body = request.get_json()

    return {}

def vecV2changeBuffList():
    json_body = request.get_json()

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
    server_data = read_json(SERVER_DATA_PATH)
    global battle_data

    # 解密战斗数据
    decrypt_data = decrypt_battle_data(json_body["data"])
    # 判断是否写入
    write_in = decrypt_data["percent"] == 100
    # 获取关卡编号
    stage_num = int(battle_data["stageId"].split("_")[-1])
    # 判断是否达到最大关卡
    is_max_level = stage_num >= server_data["vecbreakV2"].get("MaxLevel", 0)
    # 获取活动数据
    activity_data = sync_data["user"]["activity"]["VEC_BREAK_V2"][battle_data["activityId"]]
    # 获取当前积分
    current_point = activity_data["milestone"]["point"]

    # 如果关卡编号不是act1break_0或act1break_1，或未达到100完成度，或不是记录中最高的关卡，则不写入记录
    run = write_in and not is_max_level and battle_data["stageId"].startswith(("act1break_0", "act1break_1"))
    def run_after(stage_num):
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH) 
        server_data = read_json(SERVER_DATA_PATH)
        global battle_data
        # 生成新的队伍记录
        new_squad = []
        for slot in battle_data["squad"]["slots"]:
            # 获取对应的角色ID
            char_inst_id = str(slot["charInstId"])
            
            if char_inst_id not in sync_data["user"]["troop"]["chars"]:
                continue

            # 获取角色基础数据
            char_data = sync_data["user"]["troop"]["chars"][char_inst_id]
            
            # 处理装备数据
            equip_id = slot["currentEquip"] or char_data["currentEquip"]
            equip_level = char_data["equip"].get(equip_id, 1) if equip_id else 1
            
            # 构建角色完整数据
            char_template = {
                "charId": char_data["charId"],
                "currentTmpl": None,
                "potentialRank": char_data["potentialRank"],
                "level": char_data["level"],
                "mainSkillLvl": char_data["mainSkillLvl"],
                "evolvePhase": char_data["evolvePhase"],
                "skin": char_data["skin"],
                "skill": {
                    "skillIndex": slot["skillIndex"],
                    "specializeLevel": char_data["skills"][slot["skillIndex"]]["specializeLevel"]
                },
                "equip": {
                    "id": equip_id,
                    "level": equip_level
                }
            }
            new_squad.append(char_template)

        assistChar = None #TODO:助战问题暂不处理

        # 更新服务器数据
        server_data["vecbreakV2"] = {
            "maxLevel": stage_num,
            "buff": sync_data["user"]["activity"]["VEC_BREAK_V2"]["act1break"]["activatedBuff"],
            "squad": new_squad,
            "assistChar": assistChar
        }

        battle_data = None
        write_json(server_data, SERVER_DATA_PATH)

    if run:
        run_after_response(run_after, stage_num)

    return {
        "playerDataDelta": {"modified": {}, "deleted": {}},
        "result": 0,
        "msBefore": current_point,
        "msAfter": current_point,
        "finTs": time()
    }

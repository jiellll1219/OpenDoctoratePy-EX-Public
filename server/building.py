from time import time
from flask import request
from utils import read_json, write_json
import json
from constants import SYNC_DATA_TEMPLATE_PATH, USER_JSON_PATH

def Sync():

    result = {
        "ts": round(time()),
        "playerDataDelta": {
            "modified": {
                "building": {},
                "event": {
                    "building": round(time()) + 3000
                }
            },
            "deleted": {}
        }
    }
    return result

def GetRecentVisitors():

    result = {"num":0}
    return result

def GetInfoShareVisitorsNum():

    result = {"num":0}
    return result

def AssignChar(json_body):

    room_slot_id = json_body["roomSlotId"]
    char_inst_id_list = json_body["charInstIdList"]

    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    room_slots = user_sync_data["building"]["roomSlots"]

    for key, value in room_slots.items():
        room_char_inst_ids = value["charInstIds"]
        for i in range(len(room_char_inst_ids)):
            for n in range(len(char_inst_id_list)):
                if char_inst_id_list[n] == room_char_inst_ids[i]:
                    room_char_inst_ids[i] = -1

    user_sync_data["building"]["roomSlots"][room_slot_id]["charInstIds"] = char_inst_id_list

    if room_slot_id == "slot_13":
        trainer = char_inst_id_list[0]
        trainee = char_inst_id_list[1]

        training_room = user_sync_data["building"]["rooms"]["TRAINING"][room_slot_id]
        training_room["trainee"]["charInstId"] = trainee
        training_room["trainee"]["targetSkill"] = -1
        training_room["trainee"]["speed"] = 1000
        training_room["trainer"]["charInstId"] = trainer

        if trainee == -1:
            training_room["trainee"]["state"] = 0
        else:
            training_room["trainee"]["state"] = 3

        if trainer == -1:
            training_room["trainer"]["state"] = 0
        else:
            training_room["trainer"]["state"] = 3

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    player_data_delta = {
        "modified": {
            "building": user_sync_data["building"],
            "event": user_sync_data["event"]
        },
        "deleted": {}
    }

    result = {
        "playerDataDelta": player_data_delta
    }

    return result

def ChangeDiySolution(json_body):

    room_slot_id = json_body["roomSlotId"]
    solution = json_body["solution"]

    user_sync_data = SYNC_DATA_TEMPLATE_PATH

    dormitory = user_sync_data["building"]["rooms"]["DORMITORY"]
    dormitory[room_slot_id]["diySolution"] = solution

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    player_data_delta = {
        "modified": {
            "building": user_sync_data["building"],
            "event": user_sync_data["event"]
        },
        "deleted": {}
    }

    result = {
        "playerDataDelta": player_data_delta
    }

    return result

def ChangeManufactureSolution(json_body):

    room_slot_id = json_body.get("roomSlotId")
    target_formula_id = json_body.get("targetFormulaId")
    solution_count = json_body.get("solutionCount")
    user_sync_data = SYNC_DATA_TEMPLATE_PATH

    output_solution_cnt = user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['outputSolutionCnt']
    formula_id = user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['formulaId']

    if output_solution_cnt != 0:
        if 5 <= int(formula_id) <= 12:
            item_id = None
            if int(formula_id) == 5:
                item_id = "3212"
            elif int(formula_id) == 6:
                item_id = "3222"
            elif int(formula_id) == 7:
                item_id = "3232"
            elif int(formula_id) == 8:
                item_id = "3242"
            elif int(formula_id) == 9:
                item_id = "3252"
            elif int(formula_id) == 10:
                item_id = "3262"
            elif int(formula_id) == 11:
                item_id = "3272"
            elif int(formula_id) == 12:
                item_id = "3282"
            
            user_sync_data['inventory'][formula_id] += output_solution_cnt
            user_sync_data['inventory'][item_id] -= 2 * output_solution_cnt
            user_sync_data['inventory']["32001"] -= 1 * output_solution_cnt

        elif int(formula_id) > 12:
            item_id = None
            if int(formula_id) == 13:
                item_id = "30012"
                user_sync_data['status']['gold'] -= 1600 * output_solution_cnt
            elif int(formula_id) == 14:
                item_id = "30062"
                user_sync_data['status']['gold'] -= 1000 * output_solution_cnt

            user_sync_data['inventory'][formula_id] += output_solution_cnt
            user_sync_data['inventory'][item_id] -= 2 * output_solution_cnt

        else:
            user_sync_data['inventory'][formula_id] += output_solution_cnt

    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['state'] = 1
    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['formulaId'] = target_formula_id
    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['lastUpdateTime'] = int(time())
    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['completeWorkTime'] = -1
    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['remainSolutionCnt'] = 0
    user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['outputSolutionCnt'] = solution_count

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    modified = {
        "building": user_sync_data['building'],
        "event": user_sync_data['event'],
        "inventory": user_sync_data['inventory'],
        "status": user_sync_data['status']
    }

    result = {
        "playerDataDelta": {
            "modified": modified,
            "deleted": {}
        }
    }

    return result

def SettleManufacture(json_body):

    room_slot_id_list = json_body.get('roomSlotIdList')

    user_sync_data = SYNC_DATA_TEMPLATE_PATH

    for room_slot_id in room_slot_id_list:
        output_solution_cnt = user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['outputSolutionCnt']
        formula_id = user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]['formulaId']

        if output_solution_cnt != 0:
            formula_id_int = int(formula_id)
            if 5 <= formula_id_int <= 12:
                item_id = None
                if formula_id_int == 5:
                    item_id = "3212"
                elif formula_id_int == 6:
                    item_id = "3222"
                elif formula_id_int == 7:
                    item_id = "3232"
                elif formula_id_int == 8:
                    item_id = "3242"
                elif formula_id_int == 9:
                    item_id = "3252"
                elif formula_id_int == 10:
                    item_id = "3262"
                elif formula_id_int == 11:
                    item_id = "3272"
                elif formula_id_int == 12:
                    item_id = "3282"

                user_sync_data['inventory'][formula_id] += output_solution_cnt
                user_sync_data['inventory'][item_id] -= 2 * output_solution_cnt
                user_sync_data['inventory']['32001'] -= 1 * output_solution_cnt
            elif formula_id_int > 12:
                item_id = None
                if formula_id_int == 13:
                    item_id = "30012"
                    user_sync_data['status']['gold'] -= 1600 * output_solution_cnt
                elif formula_id_int == 14:
                    item_id = "30062"
                    user_sync_data['status']['gold'] -= 1000 * output_solution_cnt

                user_sync_data['inventory'][formula_id] += output_solution_cnt
                user_sync_data['inventory'][item_id] -= 2 * output_solution_cnt
            else:
                user_sync_data['inventory'][formula_id] += output_solution_cnt

        room = user_sync_data['building']['rooms']['MANUFACTURE'][room_slot_id]
        room['state'] = 0
        room['formulaId'] = ""
        room['lastUpdateTime'] = int(time())
        room['completeWorkTime'] = -1
        room['remainSolutionCnt'] = 0
        room['outputSolutionCnt'] = 0

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    player_data_delta = {
        "modified": {
            "building": user_sync_data['building'],
            "event": user_sync_data['event'],
            "inventory": user_sync_data['inventory'],
            "status": user_sync_data['status']
        },
        "deleted": {}
    }

    result = {
        "playerDataDelta": player_data_delta
    }

    return result

def WorkshopSynthesis():

    data = request.data

    return data

def UpgradeSpecialization():

    data = request.data

    return data

def CompleteUpgradeSpecialization():

    data = request.data

    return data

def DeliveryOrder():

    data = request.data

    return data

def DeliveryBatchOrder():

    data = request.data

    return data

def CleanRoomSlot():

    result = request.data

    return result

def getAssistReport():

    result = {
        "reports": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }
    
    return result

def setBuildingAssist():
    
    # 解析请求数据
    json_body = json.loads(request.data)
    type = int(json_body["type"])
    char_inst_id = str(json_body["charInstId"])
    # 读取 SYNC_DATA_TEMPLATE_PATH 对应的文件内容并转换为字典
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    # 获取当前 assist 列表
    assist_list = user_sync_data["user"]["building"]["assist"]

    # 检查 assist 中是否已经存在相同的 charInstId，如果有，将其位置修改为 空位（-1）
    for index, value in enumerate(assist_list):
        if value == char_inst_id:
            assist_list[index] = -1

    # 在传入的 type 位置写入 charInstId
    assist_list[type] = char_inst_id
        
    # 更新 user_sync_data 中的 assist 列表
    user_sync_data["user"]["building"]["assist"] = assist_list

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    # 处理 modified 数据
    user_sync_data_building = user_sync_data["user"]["building"]
    user_sync_data_event = user_sync_data["user"]['event']

    # 返回结果
    result = {
        "reports": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "building": user_sync_data_building,
                "event": user_sync_data_event
            }
        }
    }

    return result

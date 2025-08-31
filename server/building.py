from virtualtime import time
from flask import request
from utils import read_json, write_json, get_memory
from constants import SYNC_DATA_TEMPLATE_PATH, USER_JSON_PATH
import json

def Sync():
    # 读取用户数据
    user_data = read_json(USER_JSON_PATH)

    # 更新基建数据中的角色实例ID列表
    def update_building_char_InstId_List(building_data):
        # 遍历基建数据中的房间插槽列表
        for i in building_data["roomSlots"]:
            # 遍历房间插槽中的角色实例ID列表
            for j, k in enumerate(building_data["roomSlots"][i]["charInstIds"]):
                # 如果角色实例ID为-1，则跳过
                if k == -1:
                    continue
                # 将角色实例ID转换为字符串
                k = str(k)
                # 更新角色实例ID和索引
                building_data["chars"][k]["roomSlotId"] = i
                building_data["chars"][k]["index"] = j

    # 创建角色字典
    chars = {
        i: {
            "charId": user_data["user"]["troop"]["chars"][i]["charId"],
            "lastApAddTime": 1695000000,
            "ap": 8640000,
            "roomSlotId": "",
            "index": -1,
            "changeScale": 0,
            "bubble": {"normal": {"add": -1, "ts": 0}, "assist": {"add": -1, "ts": 0}},
            "workTime": 0,
        }
        for i in user_data["user"]["troop"]["chars"]
    }
    # 将角色字典赋值给基建数据
    user_data["user"]["building"]["chars"] = chars
    # 更新基建数据中的角色实例ID列表
    update_building_char_InstId_List(user_data["user"]["building"])
    # 读取基建table数据
    building_table = get_memory("building_data")
    # 创建家具字典
    furniture = {
        i: {"count": 9999, "inUse": 0}
        for i in building_table["customData"]["furnitures"]
    }
    # 将家具字典赋值给基建数据
    user_data["user"]["building"]["furniture"] = furniture
    # 将基建数据写入文件
    write_json(user_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "building": user_data["user"]["building"]
            },
            "deleted": {}
        }
    }
    
    return result

def GetRecentVisitors():

    result = {
        "visitors": []
    }
    return result

def GetInfoShareVisitorsNum():

    result = {
        "num":0
    }
    return result

def AssignChar():

    json_body = json.loads(request.data)
    roomSlotId = json_body["roomSlotId"]
    char_inst_id_list = json_body["charInstIdList"]

    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    room_slots = user_sync_data["user"]["building"]["roomSlots"]

    for key, value in room_slots.items():
        room_char_inst_ids = value["charInstIds"]
        for i in range(len(room_char_inst_ids)):
            for n in range(len(char_inst_id_list)):
                if char_inst_id_list[n] == room_char_inst_ids[i]:
                    room_char_inst_ids[i] = -1

    user_sync_data["user"]["building"]["roomSlots"][roomSlotId]["charInstIds"] = char_inst_id_list

    if roomSlotId == "slot_13":
        trainer = char_inst_id_list[0]
        trainee = char_inst_id_list[1]

        training_room = user_sync_data["user"]["building"]["rooms"]["TRAINING"][roomSlotId]
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

def ChangeDiySolution():

    json_body = request.get_json()

    roomSlotId = json_body["roomSlotId"]
    solution = json_body["solution"]

    user_json_data = read_json(USER_JSON_PATH)

    if roomSlotId == "slot_36":
        user_json_data["user"]["building"]["rooms"]["MEETING"]["slot_36"]["diySolution"] = solution
        building_modified = {
            "rooms": {
                "MEETING": {
                    "slot_36": {
                        "diySolution": solution
                    }
                }
            }
        }
    else:
        for roomId in user_json_data["user"]["building"]["roomSlots"].keys():
            if roomId == roomSlotId:
                rooms_type = user_json_data["user"]["building"]["roomSlots"][roomId]["roomId"]
                user_json_data["user"]["building"]["rooms"][rooms_type][roomSlotId]["diySolution"] = solution
                building_modified = {
                    "rooms": {
                        rooms_type: {
                            roomSlotId: {
                                "diySolution": solution 
                            }
                        }
                    }
                }
                break

    write_json(user_json_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "building": building_modified,
                "event": user_json_data["user"]["event"]
            },
            "deleted": {}
        }
    }

    return result

def ChangeManufactureSolution():

    json_body = json.loads(request.data)

    roomSlotId = str(json_body["roomSlotId"])
    target_FormulaId = str(json_body["targetFormulaId"])
    solution_count = str(json_body["solutionCount"])
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    outputSolutionCnt = user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['outputSolutionCnt']
    FormulaId = user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['formulaId']

    if outputSolutionCnt != 0:
        if 5 <= int(FormulaId) <= 12:
            item_id = None
            if int(FormulaId) == 5:
                item_id = "3212"
            elif int(FormulaId) == 6:
                item_id = "3222"
            elif int(FormulaId) == 7:
                item_id = "3232"
            elif int(FormulaId) == 8:
                item_id = "3242"
            elif int(FormulaId) == 9:
                item_id = "3252"
            elif int(FormulaId) == 10:
                item_id = "3262"
            elif int(FormulaId) == 11:
                item_id = "3272"
            elif int(FormulaId) == 12:
                item_id = "3282"
            
            user_sync_data["user"]['inventory'][FormulaId] += outputSolutionCnt
            user_sync_data["user"]['inventory'][item_id] -= 2 * outputSolutionCnt
            user_sync_data["user"]['inventory']["32001"] -= 1 * outputSolutionCnt

        elif int(FormulaId) > 12:
            item_id = None
            if int(FormulaId) == 13:
                item_id = "30012"
                user_sync_data['status']['gold'] -= 1600 * outputSolutionCnt
            elif int(FormulaId) == 14:
                item_id = "30062"
                user_sync_data['status']['gold'] -= 1000 * outputSolutionCnt

            user_sync_data["user"]['inventory'][FormulaId] += outputSolutionCnt
            user_sync_data["user"]['inventory'][item_id] -= 2 * outputSolutionCnt

        else:
            user_sync_data["user"]['inventory'][FormulaId] += outputSolutionCnt

    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['state'] = 1
    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['formulaId'] = target_FormulaId
    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['lastUpdateTime'] = int(time())
    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['completeWorkTime'] = -1
    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['remainSolutionCnt'] = 0
    user_sync_data["user"]['building']['rooms']['MANUFACTURE'][roomSlotId]['outputSolutionCnt'] = solution_count

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "building": user_sync_data['building'],
                "event": user_sync_data['event'],
                "inventory": user_sync_data['inventory'],
                "status": user_sync_data['status']
            },
            "deleted": {}
        }
    }

    return result

def SettleManufacture():

    json_body = json.loads(request.data)
    roomSlotId = json_body["roomSlotId"]
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    outputSolutionCnt = user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["outputSolutionCnt"]
    FormulaId = user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["formulaId"]

    if outputSolutionCnt != 0:
            if 5 <= int(FormulaId) <= 12:
                item_id = None
                if int(FormulaId) == 5:
                    item_id = "3212"
                elif int(FormulaId) == 6:
                    item_id = "3222"
                elif int(FormulaId) == 7:
                    item_id = "3232"
                elif int(FormulaId) == 8:
                    item_id = "3242"
                elif int(FormulaId) == 9:
                    item_id = "3252"
                elif int(FormulaId) == 10:
                    item_id = "3262"
                elif int(FormulaId) == 11:
                    item_id = "3272"
                elif int(FormulaId) == 12:
                    item_id = "3282"
                user_sync_data["user"]["inventory"][FormulaId] += outputSolutionCnt
                user_sync_data["user"]["inventory"][item_id] -= 2 * outputSolutionCnt
                user_sync_data["user"]["inventory"]["32001"] -= 1 * outputSolutionCnt
            elif int(FormulaId) > 12:
                item_id = None
                if int(FormulaId) == 13:
                    item_id = "30012"
                    user_sync_data["user"]["status"]["gold"] -= 1600 * outputSolutionCnt
                elif int(FormulaId) == 14:
                    item_id = "30062"
                    user_sync_data["user"]["status"]["gold"] -= 1000 * outputSolutionCnt
                user_sync_data["user"]["inventory"][FormulaId] += outputSolutionCnt
                user_sync_data["user"]["inventory"][item_id] -= 2 * outputSolutionCnt
            else:
                user_sync_data["user"]["inventory"][FormulaId] += outputSolutionCnt

    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["state"] = 0
    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["formulaId"] = ""
    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["lastUpdateTime"] = int(time.time())
    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["completeWorkTime"] = -1
    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["remainSolutionCnt"] = 0
    user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["outputSolutionCnt"] = 0

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
        "modified": {
            "building": user_sync_data["building"],
            "event": user_sync_data["event"],
            "inventory": user_sync_data["inventory"],
            "status": user_sync_data["status"]
        },
        "deleted": {}
    }
    }

    return result

def WorkshopSynthesis():

    json_body = json.loads(request.data)
    roomSlotId = json_body["roomSlotId"]
    work_count = json_body["times"]

    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    workshop_formulas = user_sync_data["user"]["building"]["rooms"]["MANUFACTURE"][roomSlotId]["formulaId"]

    costs = workshop_formulas["costs"]
    for cost in costs:
        item_id = cost["id"]
        item_count = cost["count"]
        user_sync_data["inventory"][item_id] -= item_count * work_count

    user_sync_data["user"]["inventory"][workshop_formulas["itemId"]] += workshop_formulas["costs"] * work_count
    user_sync_data["user"]["status"]["gold"] -= workshop_formulas["goldCost"] * work_count

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
        "modified": {
            "building": user_sync_data["building"],
            "event": user_sync_data["event"],
            "inventory": user_sync_data["inventory"],
            "status": user_sync_data["status"]
        },
        "deleted": {}
        },
        "results": {
        "type": "MATERIAL",
        "id": workshop_formulas["itemId"],
        "count": work_count
        }
    }

    return result

def UpgradeSpecialization():

    json_body = json.loads(request.data)
    


    data = request.data

    return data

def CompleteUpgradeSpecialization():

    data = request.data

    return data

def DeliveryOrder():

    json_body = json.loads(request.data)
    slotId = json_body["slotId"]
    orderId = json_body["orderId"]

    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    gold_num = user_sync_data["user"]["building"]["rooms"]["TRADING"][slotId]["stock"]["count"]

    user_sync_data["user"]["inventory"]["3003"] -= gold_num
    user_sync_data["user"]["status"]["gold"] += gold_num * 500

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
        
    modified = {
        "building": user_sync_data["building"],
        "inventory": user_sync_data["inventory"],
        "status": user_sync_data["status"]
    }
    
    result = {
        "palyerDataDelta":{
            "modified": modified,
            "deleted": {}
        }
    }

    return result

def DeliveryBatchOrder():

    json_body = json.loads(request.data)
    slotId = json_body["slotId"]
    orderId = json_body["orderId"]

    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    gold_num = user_sync_data["user"]["building"]["rooms"]["TRADING"][slotId]["stock"]["count"]

    user_sync_data["user"]["inventory"]["3003"] -= gold_num
    user_sync_data["user"]["status"]["gold"] += gold_num * 500
    # if slotId == "slot_24":
    #     user_sync_data["user"]["inventory"]["3003"] -= 2
    #     user_sync_data["user"]["status"]["gold"] += 1000

    # elif slotId == "slot_14":
    #     user_sync_data["user"]["inventory"]["3003"] -= 4
    #     user_sync_data["user"]["status"]["gold"] += 2000

    # elif slotId == "slot_5":
    #     user_sync_data["user"]["inventory"]["3003"] -= 6
    #     user_sync_data["user"]["status"]["gold"] += 3000

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
        
    modified = {
        "building": user_sync_data["building"],
        "inventory": user_sync_data["inventory"],
        "status": user_sync_data["status"]
    }
    
    result = {
        "palyerDataDelta":{
            "modified": modified,
            "deleted": {}
        }
    }

    return result

def CleanRoomSlot():

    result = request.data

    return result
 
def getAssistReport():

    result = {
        "reports": [
            {
            "ts": time(),
            "manufacture": {},
            "trading": {},
            "favor": []
            },
            {
            "ts": time() - 86400,
            "manufacture": {},
            "trading": {},
            "favor": []
            },
            {
            "ts": time() - 172800,
            "manufacture": {},
            "trading": {},
            "favor": []
            },
            {
            "ts": time() - 345600,
            "manufacture": {},
            "trading": {},
            "favor": []
            }
        ],
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

    # 检查 assist 中是否已经存在相同的 charInstId，如果有，将其位置修改为 -1
    for index, value in enumerate(user_sync_data["user"]["building"]["assist"]):
        if value == char_inst_id:
            user_sync_data["user"]["building"]["assist"][index] = -1

    # 在传入的 type 位置写入 charInstId
    user_sync_data["user"]["building"]["assist"][type] = char_inst_id

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

def changeStrategy():

    json_body = json.loads(request.data)

    slot_id = json_body["slotId"]
    strategy = json_body["strategy"]
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    user_sync_data["user"]["building"]["rooms"]["TRADING"][slot_id]["type"] = strategy
    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    modified = user_sync_data["user"]["building"]["rooms"]["TRADING"][slot_id]
    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": modified
        }
    }

    return result

def changRoomLevel():

    json_body = request.get_json()
    roomSlotId = json_body["roomSlotId"]
    targetLevel = json_body["targetLevel"]
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    user_sync_data["user"]["building"]["roomSlots"][roomSlotId]["level"] = targetLevel

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    modified = user_sync_data["user"]["building"]["roomSlots"][roomSlotId]

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": modified
        }
    }

    return result

def addPresetQueue():
    json_body = request.get_json()
    # {'slotId': 'slot_36'}

    result = {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "chars": {},
                    "roomSlots": {},
                    "rooms": {},
                    "status": {}
                }
            },
            "deleted": {}
        }
    }

    return result

def deletePresetQueue():
    json_body = request.get_json()

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "chars": {},
                    "roomSlots": {},
                    "rooms": {},
                    "status": {}
                }
            },
            "deleted": {}
        }
    }

def editPresetQueue():
    json_body = request.get_json()

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "chars": {},
                    "roomSlots": {},
                    "rooms": {},
                    "status": {}
                }
            },
            "deleted": {}
        }
    }

def usePresetQueue():
    json_body = request.get_json()

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "chars": {},
                    "roomSlots": {},
                    "rooms": {},
                    "status": {}
                }
            },
            "deleted": {}
        }
    }

def editLockQueue():
    json_body = request.get_json()
    # {'lockPos': {'slot_28': [0, 0, 0, 0, 1], 'slot_20': [0, 0, 0, 0, 0], 'slot_9': [0, 0, 0, 0, 0], 'slot_3': [0, 0, 0, 0, 0]}}
    building_data = get_memory("building_data")

    # TODO: 待编写

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    
                }
            }
        }
    }

def batchRestChar():
    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH)
    building_data = user_data["user"]["building"]

    # TODO: 待编写

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    
                }
            }
        }
    }

def buildRoom():
    json_body = request.get_json()
    print(json_body)
    # {'roomSlotId': 'slot_47', 'roomId': 'PRIVATE'}
    user_data = read_json(USER_JSON_PATH)
    building_data = user_data["user"]["building"]

    # TODO: 待编写

    return {
        "playerDataDelta": {
            "modified": {
                "building": {

                }
            }
        }
    }

def setPrivateDormOwner():
    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH)
    target_slot_id = json_body["slotId"]
    owners_id = json_body["charInsId"]

    user_data["user"]["building"]["rooms"]["PRIVATE"][target_slot_id]["owners"] = [owners_id]

    write_json(user_data, USER_JSON_PATH)

    return {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "rooms": {
                        "PRIVATE": {
                            target_slot_id: {
                                "owners": [owners_id]
                            }
                        }
                    }
                }
            },
            "deleted": {}
        }
    }

def changeBGM():
    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH)

    music_id = json_body["musicId"]

    user_data["user"]["building"]["music"]["selected"] = music_id

    result = {
        "playerDataDelta": {
            "modified": {
                "building": {
                    "music": {
                        "selected": music_id
                    }
                }
            },
            "deleted": {}
        }
    }
    return result

def getClueBox():

    return {
        "box": []
    }

def getClueFriendList():

    return {
        "result": []
    }
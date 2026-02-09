from flask import request
from virtualtime import time

from constants import (
    NORMALGACHA_PATH, 
    SYNC_DATA_TEMPLATE_PATH, 
    GACHA_HISTORY_PATH,
    SERVER_DATA_PATH
)
from utils import read_json, write_json, get_memory, run_after_response

import json
import random
import os

def syncNormalGacha():

    #使用utf-8读取normalGacha.json的数据
    NormalGachaData = read_json(NORMALGACHA_PATH)
    
    #定义要返回的json内容
    playerDataDelta = {
        "playerDataDelta":{
            "modified": {
                "recruit": {
                    "normal": {
                        "slots": NormalGachaData["detailInfo"]["availCharInfo"]["perAvailList"]
                    }
                }
            },
            "deleted": {}
        }
    }

    return playerDataDelta
    

def normalGacha():
    json_body = request.get_json()

    # 从请求体中获取slotId和tagList
    slot_id = json_body["slotId"]
    tag_list = json_body["tagList"]
    duration = json_body["duration"]

    # 修改招募相关信息
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    target_data = user_sync_data["user"]["recruit"]["normal"]["slots"][str(slot_id)]
    target_data["state"] = 2
    target_data["selectTags"] = [{"pick": 1, "tagId": tag} for tag in tag_list]
    target_data["startTs"] = time()
    target_data["durationInSec"] = duration
    target_data["maxFinishTs"] = time() + duration
    target_data["realFinishTs"] = time() + duration

    # 减少招募许可数量
    # user_sync_data["user"]["status"]["recruitLicense"] -= 1

    # 更新用户数据并将其写回JSON文件
    run_after_response(write_json, user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    # 构造返回的结果JSON对象
    result = {
        "playerDataDelta": {
            "modified": {
                "recruit": {
                    "normal": {
                        "slots": {
                            str(slot_id): user_sync_data["user"]["recruit"]["normal"]["slots"][str(slot_id)]
                        }
                    }
                }
            },
            "deleted": {}
        }
    }

    return result

def finishNormalGacha():

    json_body = json.loads(request.data)
    slot_id = json_body["slotId"]

    user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    chars = user_data["user"]["troop"]["chars"]  # 玩家角色数据
    building_chars = user_data["user"]["building"]["chars"]  # 建筑角色数据
    avail_char_info = read_json(NORMALGACHA_PATH)["detailInfo"]["availCharInfo"]["perAvailList"]  # 可用角色信息
    random_rank_array = []  # 随机等级数组

    for i, char_info in enumerate(avail_char_info):
        total_percent = int(char_info["totalPercent"] * 100)  # 总百分比
        rarity_rank = char_info["rarityRank"]  # 稀有度等级

        random_rank_object = {"rarityRank": rarity_rank, "index": i}  # 随机等级对象
        random_rank_array.extend([random_rank_object] * total_percent)

    random.shuffle(random_rank_array)  # 打乱顺序
    random_rank = random.choice(random_rank_array)  # 随机选择等级
    random_char_id = random.choice(avail_char_info[random_rank["index"]]["charIdList"])  # 随机选择角色ID

    repeat_char_id = 0  # 重复角色ID
    for j in range(1, len(chars) + 1):
        if chars[str(j)]["charId"] == random_char_id:
            repeat_char_id = j
            break

    item_get = []  # 获得物品列表
    is_new = 0  # 是否为新角色
    char_inst_id = repeat_char_id  # 角色实例ID

    if repeat_char_id == 0:  # 如果是新角色
        char_data = {}  # 角色数据
        skils_array = get_memory("character_table")[random_char_id]["skills"]  # 技能数组
        skils = []  # 技能列表

        for skill in skils_array:
            new_skill = {
                "skillId": skill["skillId"],  # 技能ID
                "state": 0,  # 技能状态
                "specializeLevel": 0,  # 技能专精等级
                "completeUpgradeTime": -1,  # 完成升级时间
                "unlock": 1 if skill["unlockCond"]["phase"] == 0 else 0  # 是否解锁
            }
            skils.append(new_skill)

        inst_id = len(chars) + 1  # 实例ID
        char_inst_id = inst_id
        char_data["instId"] = inst_id  # 实例ID
        char_data["charId"] = random_char_id  # 角色ID
        char_data["favorPoint"] = 0  # 好感度
        char_data["potentialRank"] = 0  # 潜能等级
        char_data["mainSkillLvl"] = 1  # 主技能等级
        char_data["skin"] = f"{random_char_id}#1"  # 皮肤
        char_data["level"] = 1  # 等级
        char_data["exp"] = 0  # 经验值
        char_data["evolvePhase"] = 0  # 精英阶段
        char_data["gainTime"] = int(time)  # 获得时间
        char_data["skills"] = skils  # 技能
        char_data["equip"] = {}  # 装备
        char_data["voiceLan"] = get_memory("charword_table")["charDefaultTypeDict"][random_char_id]  # 角色语音
        char_data["defaultSkillIndex"] = -1 if not skils else 0  # 默认技能索引

        sub1 = random_char_id.split("_", 2)[2]  # 分割字符
        char_name = sub1.split("_", 1)[1]  # 分割角色名

        if f"uniequip_001_{char_name}" in get_memory("uniequip_table"):
            equip = {
                f"uniequip_001_{char_name}": {"hide": 0, "locked": 0, "level": 1},  # 装备
                f"uniequip_002_{char_name}": {"hide": 0, "locked": 0, "level": 1}  # 装备
            }
            char_data["equip"] = equip
            char_data["currentEquip"] = f"uniequip_001_{char_name}"  # 当前装备

        chars[str(inst_id)] = char_data  # 更新角色数据

        char_group = {"favorPoint": 0}  # 角色分组
        sync_data_template = read_json(SYNC_DATA_TEMPLATE_PATH)
        sync_data_template["troop"]["charGroup"][random_char_id] = char_group  # 更新玩家角色组
        # if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
        #     run_after_response(write_json, sync_data_template, SYNC_DATA_TEMPLATE_PATH) # 更新同步数据

        building_char = {
            "charId": random_char_id,
            "lastApAddTime": int(time),
            "ap": 8640000,
            "roomSlotId": "",
            "index": -1,
            "changeScale": 0,
            "bubble": {"normal": {"add": -1, "ts": 0}, "assist": {"add": -1, "ts": -1}},
            "workTime": 0
        }  # 基建中的角色数据
        building_chars[str(inst_id)] = building_char  # 更新建筑角色数据
        chars[str(inst_id)] = char_data  # 更新角色数据

        shd = {"type": "HGG_SHD", "id": "4004", "count": 1}  # 物品
        item_get.append(shd)  # 添加物品

        is_new = 1  # 是新角色
        user_json_path = read_json(SYNC_DATA_TEMPLATE_PATH)
        user_json_path["status"]["hggShard"] += 1  # 更新玩家状态
        # if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
        #     run_after_response(write_json, user_json_path, SYNC_DATA_TEMPLATE_PATH)
    else:
        repeat_char = chars[str(repeat_char_id)]  # 重复角色
        potential_rank = repeat_char["potentialRank"]  # 潜能等级
        rarity = read_json(SYNC_DATA_TEMPLATE_PATH)[random_char_id]["rarity"]  # 稀有度

        item_name, item_type, item_id, item_count = "", "", "", 0  # 物品名、类型、ID、数量
        if rarity in [0, 1, 2, 3]:
            item_name = "lggShard"
            item_type = "LGG_SHD"
            item_id = "4005"
            if rarity == 2:
                item_count = 5
            elif rarity == 3:
                item_count = 30
            else:
                item_count = 1
        elif rarity in [4, 5]:
            item_name = "hggShard"
            item_type = "HGG_SHD"
            item_id = "4004"
            item_count = 5 if potential_rank != 5 else 8 if rarity == 4 else 10 if potential_rank != 5 else 15

        shd = {"type": item_type, "id": item_id, "count": item_count}  # 物品
        item_get.append(shd)  # 添加物品

        potential = {"type": "MATERIAL", "id": f"p_{random_char_id}", "count": 1}  # 潜能
        item_get.append(potential)  # 添加潜能

        user_json_path = read_json(SYNC_DATA_TEMPLATE_PATH)
        user_json_path["status"][item_name] += item_count  # 更新玩家状态
        user_json_path["inventory"][f"p_{random_char_id}"] += 1  # 更新玩家库存
        # if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
        #     run_after_response(write_json, user_json_path, SYNC_DATA_TEMPLATE_PATH) # 保存玩家数据

        chars[str(repeat_char_id)] = repeat_char  # 更新角色数据

    user_json_path = read_json(SYNC_DATA_TEMPLATE_PATH)
    user_json_path["troop"]["chars"] = chars  # 更新玩家角色数据
    user_json_path["recruit"]["normal"]["slots"][slot_id]["state"] = 1  # 更新招募状态
    user_json_path["recruit"]["normal"]["slots"][slot_id]["selectTags"] = []  # 更新选择标签

    char_get = {
        "itemGet": item_get,  # 获得物品
        "charId": random_char_id,  # 角色ID
        "charInstId": char_inst_id,  # 角色实例ID
        "isNew": is_new  # 是否新角色
    }

    return {
        "playerDataDelta": {
            "modified": {
                "recruit": user_json_path["recruit"],  # 修改的招募数据
                "status": user_json_path["status"],  # 修改的状态数据
                "troop": user_json_path["troop"]  # 修改的玩家队伍数据
            },
            "deleted": {}  # 删除的数据
        },
        "charGet": char_get  # 获得的角色数据
    }


def getPoolDetail():

    json_body = request.get_json()
    pool_Id = json_body["poolId"]

    try:
        pool = read_json(f"data/gacha/{pool_Id}.json")
    except:
        pool = read_json(f"data/gacha/DEFAULT.json")
    return pool

def boostNormalGacha():
    json_body = request.get_json()
    real_finish_ts = int(time())

    user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    user_data["user"]["recruit"]["normal"]["slots"][str(json_body["slotId"])]["realFinishTs"] = real_finish_ts
    user_data["user"]["recruit"]["normal"]["slots"][str(json_body["slotId"])]["state"] = 3

    run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)

    result =  {
        "playerDataDelta": {
            "modified": {
                "recruit": {
                    "normal": {
                        "slots": {
                            str(json_body["slotId"]): {
                                "state": 3,
                                "realFinishTs": real_finish_ts,
                            }
                        }
                    }
                }
            },
            "deleted": {},
        }
    }

    return result

def choosePoolUp():
    # {
    #     "poolId": "FESCLASSIC_52_0_2",
    #     "chooseChar": {
    #         "5": [
    #             "char_010_chen",
    #             "char_017_huang"
    #         ],
    #         "4": [
    #             "char_108_silent",
    #             "char_128_plosis",
    #             "char_148_nearl"
    #         ]
    #     }
    # }

    # TODO:待编写
    user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    return {}

def advancedGacha():

    json_body = request.get_json()
    use_Tkt_type = json_body["useTkt"]
    pool_Id = json_body["poolId"]

    match (use_Tkt_type, pool_Id.startswith("BOOT")):
        case (6, _):  # use_Tkt_type == 6
            ticket_type, amount = "classicGachaTicket", 600
        case (_, True):  # pool_Id.startswith("BOOT")
            ticket_type, amount = "gachaTicket", 380
        case _:  # 默认情况
            ticket_type, amount = "gachaTicket", 600

    return Gacha(ticket_type, amount, json_body)

def tenAdvancedGacha():
    
    json_body = request.get_json()
    use_Tkt_type = json_body["useTkt"]
    pool_Id = json_body["poolId"]

    match (use_Tkt_type, pool_Id.startswith("BOOT")):
        case (6, _):  # use_Tkt_type == 6
            ticket_type, amount = "classicTenGachaTicket", 6000
        case (1, _):  # use_Tkt_type == 1
            ticket_type, amount = "gachaTicket", 6000
        case (_, True):  # pool_Id.startswith("BOOT")
            ticket_type, amount = "tenGachaTicket", 3800
        case _:  # 默认情况
            ticket_type, amount = "tenGachaTicket", 6000

    return Gacha(ticket_type, amount, json_body)

def Gacha(ticket_type, use_diamond_shard, json_body):
    # 读取用户同步数据
    user_json_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    # 读取卡池历史记录数据
    gacha_history_data = read_json(GACHA_HISTORY_PATH)
    # 读取角色信息数据
    character_table_data = get_memory("character_table")
    # 获取卡池ID
    pool_id = json_body['poolId']
    # 获取卡池路径
    pool_path = os.path.join(os.getcwd(), 'data', 'gacha', f'{pool_id}.json')
    #读取卡池信息
    serverdata = read_json(SERVER_DATA_PATH)
    ex_gacha_data = serverdata["gacha"]["count"]
    # 获取当前时间戳
    ts = time()

    prefix_mapping = {
        "SINGLE": "NORM",
        "NORM": "NORM",
        "BOOT": "BOOT",
        "CLASSIC": "CLASSIC"
    }

    gacha_type = next((value for prefix, value in prefix_mapping.items() if json_body["poolId"].startswith(prefix)), json_body["poolId"])

    # 如果卡池文件不存在，返回错误信息
    if not os.path.exists(pool_path):
        return {
            "result": 1,
            "errMsg": "未找到该卡池文件"
        }

    # 读取卡池数据
    pool_json = read_json(pool_path)

    # 获取目标卡池的保底数，如果不存在则设置为 0
    gacha_count = int(ex_gacha_data.setdefault(gacha_type, 0))

    # 初始化需要的变量
    gacha_results = []
    new_chars = []
    item_get = []
    # 获取用户角色数据
    chars = user_json_data["user"]['troop']['chars']

    # 根据卡池类型计算抽卡次数
    if pool_id.startswith("BOOT"):
        draw_count = use_diamond_shard // 380
    else:
        draw_count = use_diamond_shard // 600

    # 循环抽卡
    for for_times, _ in enumerate(range(draw_count)):
        # 判断是否使用寻访凭证
        if json_body['useTkt'] in [1, 2, 6, 7]:
            # 判断剩余寻访凭证是否足够
            if user_json_data["user"]['status'][ticket_type] <= 0:
                return {
                    "result": 2,
                    "errMsg": "剩余寻访凭证不足"
                }
        # 判断剩余合成玉是否足够
        elif user_json_data["user"]['status']['diamondShard'] < use_diamond_shard:
            return {
                "result": 3,
                "errMsg": "剩余合成玉不足"
            }

        # 初始化最小值标志
        minimum = False
        # 初始化卡池对象名称
        pool_object_name = "newbee" if pool_id.startswith("BOOT") else "normal"
        # 获取卡池数据
        pool = user_json_data["user"]['gacha'].get(pool_object_name, {})

        # 如果是新手卡池
        if pool_id.startswith("BOOT"):
            # 更新卡池计数
            cnt = pool.get('cnt', 0) - 1
            user_json_data["user"]['gacha'][pool_object_name]['cnt'] = cnt
            # 更新抽卡次数
            gacha_count += 1
            # 如果卡池计数为0，更新卡池开放标志
            if cnt == 0:
                user_json_data["user"]['gacha'][pool_object_name]['openFlag'] = 0
        # 如果是普通卡池
        else:
            # 如果卡池数据中不存在该卡池，初始化卡池数据
            if pool_object_name not in user_json_data["user"]['gacha']:
                user_json_data["user"]['gacha'][pool_object_name] = {}

            # 如果卡池数据中不存在该卡池ID，初始化卡池ID数据
            if pool_id not in user_json_data["user"]['gacha'][pool_object_name]:
                user_json_data["user"]['gacha'][pool_object_name][pool_id] = {
                    "cnt": 0,
                    "maxCnt": 10,
                    "rarity": 4,
                    "avail": True
                }

            # 获取卡池数据
            pool = user_json_data["user"]['gacha'][pool_object_name][pool_id]
            # 更新卡池计数
            cnt = pool['cnt'] + 1
            user_json_data["user"]['gacha'][pool_object_name][pool_id]['cnt'] = cnt
            # 更新抽卡次数
            gacha_count += 1

            # 如果卡池计数为10且卡池可用，更新卡池可用标志
            # if cnt == 10 and pool['avail']:
            #     user_json_data['gacha'][pool_object_name][pool_id]['avail'] = False
            #     minimum = True

        # 获取卡池角色信息
        avail_char_info = pool_json['detailInfo']['availCharInfo']['perAvailList']
        # 如果不是新手卡池，获取卡池UP角色信息
        if not pool_id.startswith('BOOT'):
            try:
                up_char_info = pool_json['detailInfo']['upCharInfo']['perCharList']
            except Exception:
                up_char_info = []

        # 初始化随机权重数组
        random_rank_array = []

        # 遍历卡池角色信息
        for i, char_info in enumerate(avail_char_info):
            # 权重转换为整数
            total_percent = int(float(char_info['totalPercent']) * 200)
            # 获取稀有度等级
            rarity_rank = char_info['rarityRank']
            # 如果稀有度等级为5，增加权重
            if rarity_rank == 5:
                total_percent += (gacha_count + 50) // 50 * 2

            # 如果不是最小值或者稀有度等级大于等于卡池稀有度，添加权重
            if not minimum or rarity_rank >= pool['rarity']:
                random_rank_array.extend([{
                    "rarityRank": rarity_rank,
                    "index": i
                }] * total_percent)

        # 打乱随机权重数组
        random.shuffle(random_rank_array)
        # 随机选择权重
        random_rank = random.choice(random_rank_array)

        # 该部分代码在该分支中是不被需要的
        # 如果pool_id以'BOOT'开头，并且random_rank的rarityRank大于等于pool的rarity
        # if pool_id.startswith('BOOT') and random_rank['rarityRank'] >= pool['rarity']:
        #     # 将user_json_data中user的gacha的pool_object_name的pool_id的avail设置为False
        #     user_json_data["user"]['gacha'][pool_object_name][pool_id]['avail'] = False

        # 如果稀有度等级为5（六星），重置抽卡次数
        if random_rank['rarityRank'] == 5:
            gacha_count = 0

        # 处理保底次数
        ex_gacha_data[gacha_type] = gacha_count
        run_after_response(write_json, serverdata, SERVER_DATA_PATH)

        # 获取随机角色ID列表
        random_char_array = avail_char_info[random_rank['index']]['charIdList']

        # 如果不是新手卡池，添加UP角色权重
        if not pool_id.startswith('BOOT'):
            try:
                for up_char in up_char_info:
                    if up_char['rarityRank'] == random_rank['rarityRank']:
                        up_char_percent = int(up_char['percent'] * 100) - 15
                        random_char_array.extend(up_char['charIdList'] * up_char_percent)
            except Exception:
                pass

        # 打乱随机角色ID列表
        random.shuffle(random_char_array)
        # 随机选择角色ID
        random_char_id = random.choice(random_char_array)
        # 初始化重复角色ID
        repeat_char_id = 0

        # 下方被注释的代码在此分支中是不被需要的
        # 遍历用户角色数据，判断是否重复
        for k, char_data in chars.items():
            if char_data['charId'] == random_char_id:
                repeat_char_id = int(k)
                break
        
        # 清空item_get
        item_get = []
        
        if repeat_char_id == 0:
            char_data = {
                "instId": int(random_char_id.split("_")[1]),
                "charId": random_char_id,
                "favorPoint": 0,
                "potentialRank": 0,
                "mainSkillLvl": 1,
                "skin": f"{random_char_id}#1",
                "level": 1,
                "exp": 0,
                "evolvePhase": 0,
                "gainTime": time,
                "skills": [],
                "voiceLan": get_memory("character_table")['charDefaultTypeDict'][random_char_id],
                "defaultSkillIndex": 0,
                "currentEquip": None
            }

            # 获取角色的技能信息
            skills = get_memory("character_table")[random_char_id]['skills']
            for skill in skills:
                char_data['skills'].append({
                    "skillId": skill['skillId'],
                    "state": 0,
                    "specializeLevel": 0,
                    "completeUpgradeTime": -1,
                    "unlock": 1 if skill['unlockCond']['phase'] == 0 else 0
                })

            # 判断是否为特殊角色
            if f"uniequip_001_{random_char_id.split('_')[2]}" in get_memory("uniequip_table")["equipDict"]:
                equip = {
                    f"uniequip_001_{random_char_id.split('_')[2]}": {"hide": 0, "locked": 0, "level": 1},
                    f"uniequip_002_{random_char_id.split('_')[2]}": {"hide": 0, "locked": 0, "level": 1}
                }
                char_data["equip"] = equip
                char_data["currentEquip"] = f"uniequip_001_{random_char_id.split('_')[2]}"

            # 将新角色添加到用户同步数据中
            # user_json_data['troop']['chars'][char_data['instId']] = char_data
            # user_json_data['troop']['charGroup'][random_char_id] = {"favorPoint": 0}
            # user_json_data['building']['chars'][char_data['instId']] = {
            #     "charId": random_char_id,
            #     "lastApAddTime": time,
            #     "ap": 8640000,
            #     "roomSlotId": "",
            #     "index": -1,
            #     "changeScale": 0,
            #     "bubble": {
            #         "normal": {"add": -1, "ts": 0},
            #         "assist": {"add": -1, "ts": -1}
            #     },
            #     "workTime": 0
            # }

            # 将新角色添加到结果列表中
            char_get = {
                "charInstId": char_data['instId'],
                "charId": random_char_id,
                "isNew": 1,
                "item_get": [{
                    "type": "HGG_SHD",
                    "id": "4004",
                    "count": 1
                }]
            }
            # user_json_data["user"]['status']['hggShard'] += 1
            # user_json_data["user"]['inventory'][f"p_{random_char_id}"] = 0
            new_chars.append(char_get)

            # 此处存在问题，如果此角色为新角色，item_get可能会导致游戏出现错误1002，全局不返回itemGet则没有问题
            item_get.append({
                "type": "HGG_SHD",
                "id": "4004",
                "count": 1
            })
            
        else:
            # 获取已拥有角色的信息
            potential_rank = user_json_data["user"]['troop']['chars'][str(repeat_char_id)]['potentialRank']
            rarity = random_rank['rarityRank']

            # 根据角色星级获取奖励
            if not pool_id.startswith("CLASSIC"):
                item_type = "LGG_SHD"
                item_id = "4005"
                if rarity in [0, 1]:
                    item_count = 1
                elif rarity == 2:
                    item_count = 5
                elif rarity == 3:
                    item_count = 30
                elif rarity == 4:
                    item_name = "hggShard"
                    item_type = "HGG_SHD"
                    item_id = "4004"
                    item_count = 5 if potential_rank != 5 else 8
                elif rarity == 5:
                    item_name = "hggShard"
                    item_type = "HGG_SHD"
                    item_id = "4004"
                    item_count = 10 if potential_rank != 5 else 15
            else:
                item_type = "CLASSIC_SHD"
                item_id = "classic_normal_ticket"
                if rarity in [0, 1, 2]:
                    item_count = 1
                elif rarity == 3:
                    item_count = 5
                elif rarity == 4:
                    item_count = 50
                elif rarity == 5:
                    item_count = 100
                    
            new_item_get_1 = {}
            new_item_get_1["type"] = item_type
            new_item_get_1["id"] = item_id
            new_item_get_1["count"] = item_count
            item_get.append(new_item_get_1)
            # user_json_data["user"]["status"][item_name] = user_json_data["status"].get(int(item_name)) + item_count

            new_item_get_3 = {}
            new_item_get_3["type"] = "MATERIAL"
            new_item_get_3["id"] = "p_" + str(random_char_id)
            new_item_get_3["count"] = 1
            item_get.append(new_item_get_3)
            # user_json_data["user"]["inventory"]["p_" + random_char_id] = user_json_data["inventory"].get(int("p_" + random_char_id)) + 1

            charinstId = {}
            charinstId[str(repeat_char_id)] = user_json_data["user"]["troop"]["chars"][str(repeat_char_id)]
            chars[str(repeat_char_id)] = user_json_data["user"]["troop"]["chars"][str(repeat_char_id)]

        # 如果角色ID不重复，添加新角色
        if repeat_char_id == 0:
            # char_data = {
            #     "instId": len(chars) + 1,
            #     "charId": random_char_id,
            #     "gainTime": int(time.time()),
            #     "level": 1,
            #     "exp": 0,
            #     "evolvePhase": 0,
            #     "skills": [],
            #     "currentEquip": None
            # }

            # 获取角色技能数据
            # skills = read_json(CHARACTER_TABLE_PATH)[random_char_id]['skills']
            # for skill in skills:
            #     char_data['skills'].append({
            #         "skillId": skill['skillId'],
            #         "state": 0,
            #         "unlock": 1 if skill['unlockCond']['phase'] == 0 else 0
            #     })

            # 添加角色数据
            # chars[char_data['instId']] = char_data
            # 把新角色状态设定为True
            isNew = True
            # 添加抽卡结果
            gacha_results.append({
                "charInstId": char_data['instId'],
                "charId": random_char_id,
                "isNew": 1,
                "itemGet": item_get
            })
            # 添加新增角色
            # new_chars.append(char_data)
        # 如果角色ID重复，添加重复角色
        else:
            # 把新角色状态设定为False
            isNew = False
            # 添加抽卡结果
            gacha_results.append({
                "charInstId": repeat_char_id,
                "charId": random_char_id,
                "isNew": 0,
                "itemGet": item_get
            })
        
        #历史记录写入
        char_name = character_table_data[random_char_id]["name"]
        history_data = {
            "charId": random_char_id,
            "charName": char_name,
            "rarity": random_rank['rarityRank'],
            "isNew": isNew,
            "gachaTs": ts,
            "pos": for_times
        }

        # 确保 gacha_id 在 history_data 中存在
        if pool_id not in gacha_history_data:
            gacha_history_data[pool_id] = []

        # 提取现有数据
        existing_data = gacha_history_data[pool_id]

        # 构建索引字典，用于快速查找现有数据的位置
        index_map = {(item.get('gachaTs'), item.get('pos')): idx for idx, item in enumerate(existing_data)}

       # 处理单个新数据
        unique_key = (history_data.get('gachaTs'), history_data.get('pos'))
        if unique_key in index_map:
            # 如果 gachaTs 和 pos 相同，覆盖原位置
            existing_data[index_map[unique_key]] = history_data
        else:
            # 如果 gachaTs 和 pos 不同，插入到最前面
            existing_data.insert(0, history_data)

        # 更新回到 gacha_history_data
        gacha_history_data[pool_id] = existing_data
        # 写入历史记录
        run_after_response(write_json, gacha_history_data, GACHA_HISTORY_PATH)

    # 写入用户数据
    run_after_response(write_json, user_json_data, SYNC_DATA_TEMPLATE_PATH)

    if draw_count == 1:

        gacha_result = gacha_results[0]

        char_get_data = {
            "charInstId": gacha_result["charInstId"],
            "charId": gacha_result["charId"],
            "isNew": gacha_result["isNew"],
            "itemGet": item_get,
        }

        result = {
            "result": 0,
            "charGet": char_get_data,
            "playerDataDelta": {
                "modified": {},
                "deleted": {}
            }
        }

    else:
        
        result = {
            "result": 0,
            "gachaResultList": gacha_results,
            "playerDataDelta": {
                "modified": {},
                "deleted": {}
            }
        }

    # 返回结果
    return result


def gacha():

    data = '''
    <!DOCTYPE html>
    <html lang="zh-cn" data-darkreader-mode="dynamic" data-darkreader-scheme="dark" style="font-size: 101.037px;">

    <head>
        <meta name="referrer" content="no-referrer">
        <meta charset="utf-8" />
        <meta http-equiv="pragma" content="no-cache" />
        <meta http-equiv="cache-control" content="no-cache" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
        <meta name="renderer" content="webkit" />
        <meta name="force-rendering" content="webkit" />
        <meta name="viewport"
            content="user-scalable=no,initial-scale=1,maximum-scale=1,minimum-scale=1,width=device-width,height=device-height,viewport-fit=cover" />
        <meta name="copyright" content="Hypergryph" />
        <meta name="format-detection" content="telephone=no,email=no,address=no" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <title>寻访记录 | 明日方舟 - Arknights</title>
        <link href="https://web.hycdn.cn/arknights/webview/favicon.ico" rel="icon">
        <link as="image" href="https://web.hycdn.cn/arknights/webview/assets/img/nav-item-bg.80a64c.png" rel="preload">
        <link href="https://web.hycdn.cn/arknights/webview/commons.5dd297.css" rel="stylesheet">
        <link href="https://web.hycdn.cn/arknights/webview/rollHistory.755ea6.css" rel="stylesheet">
    </head>

    <body>
        <div id="root"></div>

        <script>
            const timingStart = +new Date()
            window.__READY_STATUS = "not_ready"
            window.__JS_EXECUTED = false

            function _post(url, data, callback) {
                const xhr = new XMLHttpRequest()
                xhr.open("POST", url)
                xhr.setRequestHeader("Content-Type", "application/json")
                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        callback && callback(xhr.responseText)
                    }
                }
                xhr.send(JSON.stringify(data))
            }

            window.onerror = function (e, s, l, c) {
                let message = ""
                if (e) {
                    if (e.message) {
                        message = e.message
                    } else if (e.toString) {
                        message = e.toString()
                    }
                }

                _post("/analytics/collect", {
                    type: "js_error",
                    url: window.location.href,
                    ua: navigator.userAgent,
                    e: message,
                    s,
                    l,
                    c,
                })
            }

            window.__TIMEOUT_ID = window.setTimeout(function () {
                function getPerformanceTiming() {
                    if (!performance || !performance.timing) {
                        return {}
                    }
                    const timingEnd = +new Date()
                    const t = performance.timing
                    return {
                        timingStart,
                        timingEnd,
                        redirect: t.redirectEnd - t.redirectStart,
                        appCache: t.domainLookupStart - t.fetchStart,
                        dns: t.domainLookupEnd - t.domainLookupStart,
                        tcp: t.connectEnd - t.connectStart,
                        ttfb: t.responseStart - t.requestStart,
                        contentDownload: t.responseEnd - t.responseStart,
                        httpTotal: t.responseEnd - t.requestStart,
                        domContentLoaded:
                            t.domContentLoadedEventEnd - t.navigationStart,
                        loaded: t.loadEventEnd - t.navigationStart,
                    }
                }

                _post("/analytics/collect", {
                    type: window.__READY_STATUS,
                    url: window.location.href,
                    ua: navigator.userAgent,
                    t: getPerformanceTiming(),
                    jsExecuted: window.__JS_EXECUTED,
                })
            }, 8000)
        </script>

        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/analytics.1585a3.js"></script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/rollHistory_i18n.86dc52.js"></script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/react.0bb887.js"></script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/commons.cd79f1.js"></script>
        <script crossorigin="anonymous" src="https://web.hycdn.cn/arknights/webview/rollHistory.b30980.js"></script>
        <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
        <div id="safe-area-left" style="position: absolute; top: 0px; left: 0px; width: env(safe-area-inset-left); pointer-events: none;"></div>
        <div id="safe-area-right" style="position: absolute; top: 0px; left: 0px; width: env(safe-area-inset-right); pointer-events: none;"></div>
    </body>

    </html>
    '''
    return data

def cate():

    time_stamp = time()
    gacha_table = get_memory("gacha_table")
    result_data = []
    max_count = 4

    gacha_pools = gacha_table.get("gachaPoolClient", [])
    sorted_gacha_pools = sorted(
        gacha_pools,
        key=lambda pool: (
            abs(int(pool["openTime"]) - time_stamp) if int(pool["openTime"]) <= time_stamp <= int(pool["endTime"])
            else abs(int(pool["endTime"]) - time_stamp)
        )
    )

    nearest_gachas = sorted_gacha_pools[:max_count]

    for gacha in nearest_gachas:
        gacha_info = {
            "id": gacha["gachaPoolId"],
            "name":  sorted_gacha_pools.get("gachaPoolId", {}).get("poolName", "") if gacha["gachaPoolId"].startswith("LIMITED") else "中坚寻访" if gacha["gachaPoolId"].startswith("CLASSIC") else "标准寻访" if gacha["gachaPoolId"].startswith("NORM") else "标准寻访"
        }
        
        # 仅当时间戳在openTime和endTime之间时才添加"active": True
        if gacha["openTime"] <= time_stamp <= gacha["endTime"]:
            gacha_info["active"] = True

        result_data.append(gacha_info)
    
    result = {
        "code": 0,
        "msg": "",
        "data": result_data
    }

    return (json.dumps(result, ensure_ascii=False))


def history():
    gacha_history_data = read_json(GACHA_HISTORY_PATH)
    gacha_table = get_memory("gacha_table")
    category = request.args.get("category", None)  # 卡池id
    list_data = []
    has_more = False

    # 使用传递的 gachaTs 作为时间基准；若没有传递，则使用当前时间
    ts = int(request.args.get("gachaTs", time()))
    
    # 获取请求中的 pos 参数，用于标识开始位置
    request_pos_get = 0 if int(request.args.get("pos", 0)) == 0 else int(request.args.get("pos"))
    request_pos = request_pos_get - 1 if request_pos_get > 0 else 0
    
    # 直接获取并排序 category 对应的记录列表
    if gacha_history_data.get(category) is not None:
        gacha_history_data[category].sort(key=lambda x: (abs(int(x["gachaTs"]) - ts), -x["pos"]))
    
        # 从 request_pos 开始获取 10 条数据
        gacha_history_data_2 = gacha_history_data[category][request_pos:request_pos + 10]
        
        # 查找 category 对应的 gachaPoolName
        pool_name = ""
        for item in gacha_table["gachaPoolClient"]:
            if item.get("gachaPoolId") == category:
                pool_name = item.get("gachaPoolName", "")
                break

        # 动态生成 list_data
        for info in gacha_history_data_2:
            list_data.append({
                "poolId": category,
                "poolName": pool_name,
                "charId": info["charId"],
                "charName": info["charName"],
                "rarity": info["rarity"],
                "isNew": info["isNew"],
                "gachaTs": info["gachaTs"],
                "pos": info["pos"]
            })
    
        # 检查是否有更多符合条件的记录，如果有更多数据则设置 hasMore 为 True
        has_more = len(gacha_history_data[category]) > (request_pos + 10)

    result = {
        "code": 0,
        "msg": "",
        "data": {
            "list": list_data,
            "hasMore": has_more
        }
    }

    return result

def bulletinVersion():

    result = {
        "code": 0,
        "msg": "",
        "data": {
            "version": "718ebe1cd854994dfe0e2d50e834a81a"
        }
    }

    return result

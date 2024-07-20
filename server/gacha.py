from flask import request
from virtualtime import time

from constants import (
    NORMALGACHA_PATH, 
    SYNC_DATA_TEMPLATE_PATH, 
    USER_JSON_PATH, 
    EQUIP_TABLE_URL, 
    CHARACTER_TABLE_URL, 
    CHARWORD_TABLE_URL, 
    EX_CONFIG_PATH
)
from utils import read_json, write_json

import json
import random
import os

def syncNormalGacha():

    #使用utf-8读取normalGacha.json的数据
    NormalGachaData = read_json(NORMALGACHA_PATH, encoding="utf-8")
    
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

    return {
        "playerDataDelta": playerDataDelta
    }
    

def gachanormalGacha():
    json_body = json.loads(request.data)

    # 从请求体中获取slotId和tagList
    slot_id = json_body["slotId"]
    tag_list = json_body["tagList"]

    # 修改招募相关信息
    user_sync_data = read_json(USER_JSON_PATH, encoding="utf-8")
    user_sync_data["user"]["recruit"]["normal"]["slots"][str(slot_id)]["state"] = 2
    select_tags = [{"pick": 1, "tagId": tag} for tag in tag_list]
    user_sync_data["user"]["recruit"]["normal"]["slots"][str(slot_id)]["selectTags"] = select_tags

    # 减少招募许可数量
    user_sync_data["user"]["status"]["recruitLicense"] -= 1

    # 更新用户数据并将其写回JSON文件
    write_json(USER_JSON_PATH, user_sync_data)

    # 构造返回的结果JSON对象
    return {
        "playerDataDelta": {
            "modified": {
                "recruit": user_sync_data["user"]["recruit"],
                "status": user_sync_data["user"]["status"]
            },
            "deleted": {}
        }
    }


def finishNormalGacha():

    json_body = json.loads(request.data)
    slot_id = json_body["slotId"]

    chars = read_json(USER_JSON_PATH)["user"]["troop"]["chars"]  # 玩家角色数据
    building_chars = read_json(SYNC_DATA_TEMPLATE_PATH)["user"]["building"]["chars"]  # 建筑角色数据
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
        skils_array = read_json(CHARACTER_TABLE_URL)[random_char_id]["skills"]  # 技能数组
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
        char_data["voiceLan"] = read_json(CHARWORD_TABLE_URL)["charDefaultTypeDict"][random_char_id]  # 角色语音
        char_data["defaultSkillIndex"] = -1 if not skils else 0  # 默认技能索引

        sub1 = random_char_id.split("_", 2)[2]  # 分割字符
        char_name = sub1.split("_", 1)[1]  # 分割角色名

        if f"uniequip_001_{char_name}" in read_json(EQUIP_TABLE_URL):
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
        if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
            write_json(sync_data_template, SYNC_DATA_TEMPLATE_PATH) # 更新同步数据

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
        user_json_path = read_json(USER_JSON_PATH)
        user_json_path["status"]["hggShard"] += 1  # 更新玩家状态
        if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
            write_json(USER_JSON_PATH, user_json_path)
    else:
        repeat_char = chars[str(repeat_char_id)]  # 重复角色
        potential_rank = repeat_char["potentialRank"]  # 潜能等级
        rarity = read_json(USER_JSON_PATH)[random_char_id]["rarity"]  # 稀有度

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

        user_json_path = read_json(USER_JSON_PATH)
        user_json_path["status"][item_name] += item_count  # 更新玩家状态
        user_json_path["inventory"][f"p_{random_char_id}"] += 1  # 更新玩家库存
        if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
            write_json(USER_JSON_PATH, user_json_path) # 保存玩家数据

        chars[str(repeat_char_id)] = repeat_char  # 更新角色数据

    user_json_path = read_json(USER_JSON_PATH)
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

    pool = read_json(f"data/gacha/{pool_Id}.json", encoding="utf-8")
    return pool

def advancedGacha():

    json_body = request.json
    use_Tkt_type = json_body["useTkt"]
    pool_Id = json_body["poolId"]

    if use_Tkt_type == 6:
        return Gacha("classicGachaTicket", 600, json_body)
    elif pool_Id.startswith("BOOT"):
        return Gacha("gachaTicket", 380, json_body)
    else:
        return Gacha("gachaTicket", 600, json_body)

def tenAdvancedGacha():
    
    json_body = request.json
    use_Tkt_type = json_body["useTkt"]
    pool_Id = json_body["poolId"]

    if use_Tkt_type == 6:
        return Gacha("classicTenGachaTicket", 6000, json_body)
    elif use_Tkt_type == 1:
        return Gacha("gachaTicket", 6000, json_body)
    elif pool_Id.startswith("BOOT"):
        return Gacha("tenGachaTicket", 3800, json_body)
    else:
        return Gacha("tenGachaTicket", 6000, json_body)

def Gacha(ticket_type, use_diamond_shard, json_body):

    # 读取用户同步数据
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    pool_id = json_body['poolId']
    pool_path = os.path.join(os.getcwd(), 'data', 'gacha', f'{pool_id}.json')

    # 获取使用的寻访凭证的类型编号
    use_tkt = json_body['useTkt']

    # 判断当前干员寻访是否可以使用
    if not os.path.exists(pool_path):
        return {
            "result": 1,
            "errMsg": "该当前干员寻访无法使用，详情请关注公告"
        }

    # 读取当前干员寻访的json数据
    with open(pool_path, 'r') as file:
        pool_json = json.load(file)

    # 初始化结果列表和新的角色列表
    gacha_result_list = []
    new_chars = []
    char_get = {}
    troop = {}
    chars = user_sync_data['troop']['chars']

    # 计算使用的合成玉数量
    if json_body['poolId'].startswith("BOOT"):
        used_diammond = use_diamond_shard // 380    #used_diamond为抽卡次数
    else:
        used_diammond = use_diamond_shard // 600

    # 循环使用合成玉
    for count in range(used_diammond):
        # 判断是否使用寻访凭证
        if use_tkt in [1, 2, 6, 7]:
            # 判断剩余寻访凭证是否足够
            if user_sync_data['status'][ticket_type] <= 0:
                return {
                    "result": 2,
                    "errMsg": "剩余寻访凭证不足"
                }
        # 判断剩余合成玉是否足够
        elif user_sync_data['status']['diamondShard'] < use_diamond_shard:
            return {
                "result": 3,
                "errMsg": "剩余合成玉不足"
            }

        # 初始化最小值和寻访池对象名称
        minimum = False
        pool_object_name = "newbee" if json_body['poolId'].startswith("BOOT") else "normal"
        pool = user_sync_data['gacha'].get(pool_object_name, {})

        # 判断是否为新手寻访池
        if json_body['poolId'].startswith("BOOT"):
            pool = user_sync_data['gacha'].get(pool_object_name, {})
            cnt = pool.get('cnt', 0) - 1
            user_sync_data['gacha'][pool_object_name]['cnt'] = cnt
            user_sync_data['status']['gachaCount'] += 1

            # 判断是否已经达到最大寻访次数
            if cnt == 0:
                user_sync_data['gacha'][pool_object_name]['openFlag'] = 0
        else:
            # 判断是否为新寻访池
            if pool_object_name not in user_sync_data['gacha']:
                user_sync_data['gacha'][pool_object_name] = {}

            # 判断是否为新寻访池中的某个池子
            if pool_id not in user_sync_data['gacha'][pool_object_name]:
                user_sync_data['gacha'][pool_object_name][pool_id] = {
                    "cnt": 0,
                    "maxCnt": 10,
                    "rarity": 4,
                    "avail": True
                }

            pool = user_sync_data['gacha'][pool_object_name][pool_id]
            cnt = pool['cnt'] + 1
            user_sync_data['gacha'][pool_object_name][pool_id]['cnt'] = cnt
            user_sync_data['status']['gachaCount'] += 1

            # 判断是否已经达到最大寻访次数
            if cnt == 10 and pool['avail']:
                user_sync_data['gacha'][pool_object_name][pool_id]['avail'] = False
                minimum = True

        # 获取可寻访的角色信息
        avail_char_info = pool_json['detailInfo']['availCharInfo']['perAvailList']
        up_char_info = pool_json['detailInfo']['upCharInfo']['perCharList']
        random_rank_array = []

        # 计算每个稀有等级的概率
        for i, char_info in enumerate(avail_char_info):
            total_percent = int(char_info['totalPercent'] * 200)
            rarity_rank = char_info['rarityRank']
            if rarity_rank == 5:
                total_percent += (user_sync_data['status']['gachaCount'] + 50) // 50 * 2

            # 判断是否为最小值
            if not minimum or rarity_rank >= pool['rarity']:
                for _ in range(total_percent):
                    random_rank_array.append({
                        "rarityRank": rarity_rank,
                        "index": i
                    })

        # 随机选择一个角色
        random.shuffle(random_rank_array)
        random_rank = random.choice(random_rank_array)
        if json_body['poolId'] != "BOOT_0_1_1" and random_rank['rarityRank'] >= pool['rarity']:
            user_sync_data['gacha'][pool_object_name][pool_id]['avail'] = False

        # 判断是否为六星角色
        if random_rank['rarityRank'] == 5:
            user_sync_data['status']['gachaCount'] = 0

        # 获取角色的id列表
        random_char_array = avail_char_info[random_rank['index']]['charIdList']

        # 计算五星角色的概率
        for up_char in up_char_info:
            if up_char['rarityRank'] == random_rank['rarityRank']:
                percent = int(up_char['percent'] * 100) - 15
                for char_id in up_char['charIdList']:
                    random_char_array.extend([char_id] * percent)

        # 随机选择一个角色
        random.shuffle(random_char_array)
        random_char_id = random.choice(random_char_array)
        repeat_char_id = 0

        # 判断是否已经拥有该角色
        for k, char_data in user_sync_data['troop']['chars'].items():
            if char_data['charId'] == random_char_id:
                repeat_char_id = int(k)
                break

        # 判断是否为新角色
        if repeat_char_id == 0:
            char_data = {
                "instId": len(user_sync_data['troop']['chars']) + 1,
                "charId": random_char_id,
                "favorPoint": 0,
                "potentialRank": 0,
                "mainSkillLvl": 1,
                "skin": f"{random_char_id}#1",
                "level": 1,
                "exp": 0,
                "evolvePhase": 0,
                "gainTime": int(time),
                "skills": [],
                "voiceLan": read_json(CHARWORD_TABLE_URL)['charDefaultTypeDict'][random_char_id],
                "defaultSkillIndex": 0,
                "currentEquip": None
            }

            # 获取角色的技能信息
            skills = read_json(CHARACTER_TABLE_URL)[random_char_id]['skills']
            for skill in skills:
                char_data['skills'].append({
                    "skillId": skill['skillId'],
                    "state": 0,
                    "specializeLevel": 0,
                    "completeUpgradeTime": -1,
                    "unlock": 1 if skill['unlockCond']['phase'] == 0 else 0
                })

            # 判断是否为特殊角色
            if f"uniequip_001_{random_char_id.split('_')[2]}" in EQUIP_TABLE_URL:
                equip = {
                    f"uniequip_001_{random_char_id.split('_')[2]}": {"hide": 0, "locked": 0, "level": 1},
                    f"uniequip_002_{random_char_id.split('_')[2]}": {"hide": 0, "locked": 0, "level": 1}
                }
                char_data["equip"] = equip
                char_data["currentEquip"] = f"uniequip_001_{random_char_id.split('_')[2]}"

            # 将新角色添加到用户同步数据中
            user_sync_data['troop']['chars'][char_data['instId']] = char_data
            user_sync_data['troop']['charGroup'][random_char_id] = {"favorPoint": 0}
            user_sync_data['building']['chars'][char_data['instId']] = {
                "charId": random_char_id,
                "lastApAddTime": int(time),
                "ap": 8640000,
                "roomSlotId": "",
                "index": -1,
                "changeScale": 0,
                "bubble": {
                    "normal": {"add": -1, "ts": 0},
                    "assist": {"add": -1, "ts": -1}
                },
                "workTime": 0
            }

            # 将新角色添加到结果列表中
            char_get = {
                "charInstId": char_data['instId'],
                "charId": random_char_id,
                "isNew": 1,
                "itemGet": [{
                    "type": "HGG_SHD",
                    "id": "4004",
                    "count": 1
                }]
            }
            user_sync_data['status']['hggShard'] += 1
            user_sync_data['inventory'][f"p_{random_char_id}"] = 0
            gacha_result_list.append(char_get)
            new_chars.append(char_get)
        else:
            # 获取已拥有角色的信息
            char_data = user_sync_data['troop']['chars'][str(repeat_char_id)]
            potential_rank = char_data['potentialRank']
            rarity = random_rank['rarityRank']

            # 根据角色星级获取奖励
            item_name = item_type = item_id = None
            item_count = 0
            if rarity == 0:
                item_name, item_type, item_id, item_count = "lggShard", "LGG_SHD", "4005", 1
            elif rarity == 1:
                item_name, item_type, item_id, item_count = "bggShard", "BGG_SHD", "4003", 1
            elif rarity == 2:
                item_name, item_type, item_id, item_count = "goldCert", "GOLD_CERT", "3002", 2
            elif rarity == 3:
                item_name, item_type, item_id, item_count = "goldCert", "GOLD_CERT", "3002", 5
            elif rarity == 4:
                item_name, item_type, item_id, item_count = "diamondShard", "DIAMOND_SHARD", "4001", 15
            elif rarity == 5:
                item_name, item_type, item_id, item_count = "diamondShard", "DIAMOND_SHARD", "4001", 50

            char_get = {
                "charInstId": repeat_char_id,
                "charId": random_char_id,
                "isNew": 0,
                "itemGet": [{
                    "type": item_type,
                    "id": item_id,
                    "count": item_count
                }]
            }
            gacha_result_list.append(char_get)
        
    # 将奖励添加到用户同步数据中
    user_sync_data['status'][item_name] += item_count

    # 扣除对应消耗的抽卡资源
    if EX_CONFIG_PATH["gacha"]["isFree"] == False:
        if use_tkt in [1, 2, 6, 7] and user_sync_data['status'][ticket_type] >= used_diammond:
            user_sync_data['status'][ticket_type] -= used_diammond
        else:
            user_sync_data['status']["diamondShard"] -= use_diamond_shard

    if EX_CONFIG_PATH["gacha"]["saveCharacter"] == True:
        write_json(user_sync_data, USER_JSON_PATH)


    # 返回结果
    return {
        "result": 0,
        "data": {
            "userSyncData": user_sync_data,
            "gachaResultList": gacha_result_list
        }
    }

from flask import request, jsonify
from datetime import datetime

from constants import NORMALGACHA_PATH
from constants import SYNC_DATA_TEMPLATE_PATH
from constants import USER_JSON_PATH
from constants import EQUIP_TABLE_URL
from constants import CHARACTER_TABLE_URL
from constants import CHARWORD_TABLE_URL
from utils import read_json, write_json

import json
import random

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
    json_body = request.json

    # 从请求体中获取slotId和tagList
    slot_id = json_body.get("slotId")
    tag_list = json_body.get("tagList")

    # 修改招募相关信息
    user_sync_data = read_json(USER_JSON_PATH, encoding="utf-8")
    user_sync_data["recruit"]["normal"]["slots"][str(slot_id)]["state"] = 2
    select_tags = [{"pick": 1, "tagId": tag} for tag in tag_list]
    user_sync_data["recruit"]["normal"]["slots"][str(slot_id)]["selectTags"] = select_tags

    # 减少招募许可数量
    user_sync_data["status"]["recruitLicense"] -= 1

    # 更新用户数据并将其写回JSON文件
    write_json(USER_JSON_PATH, user_sync_data)

    # 构造返回的结果JSON对象
    result = {
        "playerDataDelta": {
            "modified": {
                "recruit": user_sync_data["recruit"],
                "status": user_sync_data["status"]
            },
            "deleted": {}
        }
    }

    return jsonify(result)

def finishNormalGacha():

    json_body = request.json
    slot_id = json_body.get("slotId")

    chars = read_json(USER_JSON_PATH)["troop"]["chars"]  # 玩家角色数据
    building_chars = read_json(SYNC_DATA_TEMPLATE_PATH)["building"]["chars"]  # 建筑角色数据
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
        char_data["gainTime"] = int(datetime.now().timestamp())  # 获得时间
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
        write_json(sync_data_template, SYNC_DATA_TEMPLATE_PATH)

        building_char = {
            "charId": random_char_id,
            "lastApAddTime": int(datetime.now().timestamp()),
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
        write_json(USER_JSON_PATH, user_json_path)

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

    data = {
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

    return data  # 返回结果

def getPoolDetail():

    data = request.data

    return data

def advancedGacha():

    data = request.data

    return data

def tenAdvancedGacha():
    
    data = request.data

    return data
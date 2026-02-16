from datetime import datetime

from flask import request

from constants import SHOP_PATH, SYNC_DATA_TEMPLATE_PATH
from utils import read_json, write_json, run_after_response, get_memory


def getGoodPurchaseState():

    data = request.data
    data = {
    "playerDataDelta": {
        "modified": {},
        "deleted": {}
    },
    "result": {}
    }

    return data

# 获取json的内容并返回

def getShopGoodList(shop_type):
    return read_json(SHOP_PATH)[shop_type.lower()]
  
def buyShopGood(shop_type: str):
    # 皮肤购买
    if shop_type == "Skin":
        good_id = json_body["goodId"]

        skin_good_list = get_memory("shop")["skin"]
        sync_data_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    
        # 遍历goodList列表
        for good in skin_good_list["goodList"]:
            # 获取价格
            origin_price = good["originPrice"]
    
        # 扣除Diamond货币并添加皮肤
        sync_data_data["user"]["skin"]["characterSkins"][good_id[3:]] = 1
        sync_data_data["user"]["skin"]["skinTs"][good_id[3:]] = int(datetime.now().timestamp())
        sync_data_data["user"]["status"]["androidDiamond"] -= origin_price
        sync_data_data["user"]["status"]["iosDiamond"] -= origin_price

        # 返回内容
        result = {
            "playerDataDelta": {
                "deleted": {},
                "modified": {
                    "skin": sync_data_data["user"]["skin"],
                    "status": {
                        "androidDiamond": sync_data_data["user"]["status"]["androidDiamond"],
                        "iosDiamond": sync_data_data["user"]["status"]["iosDiamond"]
                    }
                }
            },
            "result": 0
        }
        
        # run_after_response(write_json, sync_data_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    json_body = request.get_json()
    # 商品ID
    good_id = str(json_body["goodId"])
    # 购买数量
    count = int(json_body["count"])

    def bomb():
        return {}, 500

    items = []
    modified = {
        "status": {},
        "inventory": {},
        "troop": {}
    }

    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    good_list = get_memory("shop")[shop_type.lower()]["goodList"]
    gacha_map = {
        "TKT_GACHA": "gachaTicket",
        "TKT_GACHA_10": "tenGachaTicket",
        "CLASSIC_TKT_GACHA": "classicGachaTicket",
        "CLASSIC_TKT_GACHA_10": "classicTenGachaTicket"
    }
    currency_map = {
        "low": "lggShard",
        "high": "hggShard",
        "extra": "4006",
        "classic": "classicShard",
        "epgs": "EPGS_COIN"
    }

    # 从good_list中获取 goodId
    good = next((g for g in good_list if g["goodId"] == good_id), None)
    # 没有就跟客户端爆了
    if not good:
        bomb

    # 要扣的数值
    price = good["price"] * count

    currency = None
    inventory = None

    # 获取货币类型
    match shop_type.lower():
        case "low"|"high"|"classic":
            currency = currency_map[shop_type.lower()]
            inventory:dict = sync_data["user"]["status"]
        case "extra"|"epgs":
            currency = currency[shop_type.lower()]
            inventory:dict = sync_data["user"]["inventory"]
        case _:
            bomb
    
    # 如果货币不足
    if inventory.get(currency, 0) < price:
        bomb
    else:
        # 否则正常扣除
        inventory[currency] -= price

    item = good["item"]
    if item is None:
        bomb
    else:
        item_type = item["type"]

    # 实际增加数量 = 配置数量 × 购买次数
    item_count = item.get("count", 1) * count

    # user：用户数据根节点
    user = sync_data["user"]

    # 角色类型（CHAR = 干员/角色）
    if item_type == "CHAR":
        # troop.chars：角色实例表（instId → 角色数据）
        chars = user["troop"]["chars"]

        # char_id：角色配置ID（非实例ID）
        char_id = item["id"]

        # repeat_inst：已拥有角色的实例ID（如果重复获得）
        repeat_inst = next(
            (iid for iid, c in chars.items() if c["charId"] == char_id),
            None
        )

        #  新角色 
        if repeat_inst is None:
            # inst_id：角色实例ID（唯一）
            inst_id = str(len(chars) + 1)

            char_data = {
                "instId": int(inst_id), # 实例ID
                "charId": char_id, # 角色配置ID
                "favorPoint": 0, # 好感度
                "potentialRank": 0, # 潜能等级
                "mainSkillLvl": 1, # 主技能等级
                "skin": f"{char_id}#1", # 默认皮肤
                "level": 1, # 等级
                "exp": 0, # 经验
                "evolvePhase": 0, # 精英化阶段
                "gainTime": int(datetime.now().timestamp()), # 获得时间戳
                "skills": [], # 技能列表
                "defaultSkillIndex": -1, # 默认技能
                "currentEquip": None # 模块
            }

            # 写入角色表
            chars[inst_id] = char_data

            # 当前角色实例游标（用于新角色ID生成）
            user["troop"]["curCharInstId"] = int(inst_id) + 1

            # 更新troop修改信息
            modified["troop"]["chars"] = {inst_id: char_data}
            modified["troop"]["curCharInstId"] = user["troop"]["curCharInstId"]

            # 返回给客户端的结构
            items.append({
                "id": char_id,
                "type": "CHAR",
                "charGet": {
                    "charInstId": int(inst_id),
                    "charId": char_id,
                    "isNew": 1 # 新角色
                }
            })

        #  重复角色 
        else:
            # 更新troop修改信息
            modified["troop"]["chars"] = {repeat_inst: chars[repeat_inst]}

            items.append({
                "id": char_id,
                "type": "CHAR",
                "charGet": {
                    "charInstId": int(repeat_inst),
                    "charId": char_id,
                    "isNew": 0 # 非新角色
                }
            })

    # 合成玉
    elif item_type == "DIAMOND_SHD":
        user["status"]["diamondShard"] += item_count
        user["status"]["androidDiamond"] += item_count

        modified["status"].update({
            "diamondShard": user["status"]["diamondShard"],
            "androidDiamond": user["status"]["androidDiamond"],
        })

        # 添加到items列表
        items.append({
            "id": "4001",
            "type": "DIAMOND_SHD",
            "count": item_count
        })

    # 龙门币
    elif item_type == "GOLD":
        user["status"]["gold"] += item_count
        modified["status"]["gold"] = user["status"]["gold"]

        # 添加到items列表
        items.append({
            "id": "4002",
            "type": "GOLD",
            "count": item_count
        })

    # 寻访凭证
    elif "GACHA" in item_type:
        key = gacha_map.get(item_type)

        if key:
            user["status"][key] += item_count
            modified["status"][key] = user["status"][key]

            # 添加到items列表
            items.append({
                "id": item["id"],
                "type": item_type,
                "count": item_count
            })

    # 其它
    else:
        # 仓库
        inv = user.setdefault("inventory", {})

        # 物品ID
        item_id = item["id"]

        inv[item_id] = inv.get(item_id, 0) + item_count
        modified["inventory"][item_id] = inv[item_id]

        # 添加到items列表
        items.append({
            "id": item_id,
            "type": item_type,
            "count": item_count
        })

    # 返回内容
    result = {
        "playerDataDelta": {
            "deleted": {},
            # 只返回有变动的数据块
            "modified": {k: v for k, v in modified.items() if v}
        },
        "items": items,
        "result": 0
    }

    return result

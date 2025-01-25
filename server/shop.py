from flask import request
from utils import read_json, write_json
from datetime import datetime

from constants import CASHGOODLIST_PATH, EPGSGOODLIST_PATH, EXTRAGOODLIST_PATH, FURNIGOODLIST_PATH, GPGOODLIST_PATH, HIGHGOODLIST_PATH, LMTGSGOODLIST_PATH, LOWGOODLIST_PATH, REPGOODLIST_PATH, SKINGOODLIST_PATH, SOCIALGOODLIST_PATH, CLASSICGOODLIST_PATH
from constants import USER_JSON_PATH, SYNC_DATA_TEMPLATE_PATH

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
def getCashGoodList():

    CashGoodListData = read_json(CASHGOODLIST_PATH, encoding="utf-8")

    return CashGoodListData

def getGPGoodList():
    GPGoodListData = read_json(GPGOODLIST_PATH, encoding="utf-8")

    return GPGoodListData

def getSkinGoodList():
    SkinGoodListData = read_json(SKINGOODLIST_PATH, encoding="utf-8")

    return SkinGoodListData

def getLowGoodList():
    LowGoodListData = read_json(LOWGOODLIST_PATH, encoding="utf-8")

    return LowGoodListData

def getHighGoodList():
    HighGoodListData = read_json(HIGHGOODLIST_PATH, encoding="utf-8")

    return HighGoodListData

def getExtraGoodList():
    ExtraGoodListData = read_json(EXTRAGOODLIST_PATH, encoding="utf-8")

    return ExtraGoodListData

def getEPGSGoodList():
    EPGSGoodListData = read_json(EPGSGOODLIST_PATH, encoding="utf-8")

    return EPGSGoodListData

def getRepGoodList():
    RepGoodListData = read_json(REPGOODLIST_PATH, encoding="utf-8")

    return RepGoodListData

def getFurniGoodList():
    FurniGoodListData = read_json(FURNIGOODLIST_PATH, encoding="utf-8")

    return FurniGoodListData

def getSocialGoodList():
    SocialGoodListData = read_json(SOCIALGOODLIST_PATH, encoding="utf-8")

    return SocialGoodListData

def getClassicGoodList():
    ClassicGoodListData = read_json(CLASSICGOODLIST_PATH, encoding="utf-8")

    return ClassicGoodListData

def getLMTGSGoodList():
    LMTGSGoodListData = read_json(LMTGSGOODLIST_PATH, encoding="utf-8")

    return LMTGSGoodListData

# 购买逻辑基本相同，注释只写一遍
def buySkinGood():

    json_body = request.get_json()
    good_id = json_body.get('goodId')

    skin_good_list = read_json(SKINGOODLIST_PATH)
    user_json_data = read_json(USER_JSON_PATH, encoding="utf-8")
 
    # 遍历goodList列表
    for good in skin_good_list['goodList']:
    # 获取originPrice的值
        origin_price = good['originPrice']
 
    # 扣除Diamond货币并添加皮肤
    user_json_data['user']['skin']['characterSkins'][good_id[3:]] = 1
    user_json_data['user']['skin']['skinTs'][good_id[3:]] = int(datetime.now().timestamp())
    user_json_data['user']['status']['androidDiamond'] -= origin_price
    user_json_data['user']['status']['iosDiamond'] -= origin_price

    # 返回内容
    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": {
                    "androidDiamond": user_json_data['user']['status']['androidDiamond'],
                    "iosDiamond": user_json_data['user']['status']['iosDiamond']
                }
            }
        },
        "result": 0
    }

    return result
    

def buyLowGood():

    json_body = request.get_json()

    good_id = json_body.get('goodId')
    count = json_body.get('count')

    items = []
    low_good_list = read_json(LOWGOODLIST_PATH, encoding="utf-8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf-8")

    for low_good in low_good_list['goodList']:
        if low_good['goodId'] == good_id:
            user_json_data['user']['status']['lggShard'] -= low_good['price'] * count

            reward_id = low_good['item']['id']
            reward_count = low_good['item']['count'] * count
            for item in user_json_data['user']['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    write_json(user_json_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

def buyHighGood():

    json_body = request.get_json()

    good_id = json_body.get('goodId')
    count = json_body.get('count')

    items = []
    high_good_list = read_json(HIGHGOODLIST_PATH, encoding="utf-8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf-8")

    for high_good in high_good_list['goodList']:
        if high_good['goodId'] == good_id:
            user_json_data['user']['status']['hggShard'] -= high_good['price'] * count

            reward_id = high_good['item']['id']
            reward_count = high_good['item']['count'] * count
            for item in user_json_data['user']['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    write_json(user_json_data, SYNC_DATA_TEMPLATE_PATH)

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

def buyExtraGood():

    json_body = request.get_json()

    good_id = json_body.get('goodId')
    count = json_body.get('count')

    items = []
    extra_good_list = read_json(EXTRAGOODLIST_PATH, encoding="utf-8")
    user_json_data = read_json(USER_JSON_PATH, encoding="utf-8")

    for extra_good in extra_good_list['goodList']:
        if extra_good['goodId'] == good_id:
            user_json_data['user']['inventory']['4006'] -= extra_good['price'] * count

            reward_id = extra_good['item']['id']
            reward_count = extra_good['item']['count'] * count
            for item in user_json_data['user']['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    write_json(user_json_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

def buyClassicGood():

    json_body = request.get_json()
    good_id = json_body.get('goodId')
    count = json_body.get('count')

    items = []
    classic_good_list = read_json(CLASSICGOODLIST_PATH, encoding="utf-8")
    
    user_json_data = read_json(USER_JSON_PATH, encoding="utf-8")

    for classic_good in classic_good_list['goodList']:
        if classic_good['goodId'] == good_id:
            user_json_data['user']['status']['REP_COIN'] -= classic_good['price'] * count

            reward_id = classic_good['item']['id']
            reward_count = classic_good['item']['count'] * count
            for item in user_json_data['user']['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    write_json(user_json_data, USER_JSON_PATH)

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

def buyFurniGroup():

    # 把user_json_data和FurniGoodList转换为json数据（直接调用会导致TypeError: string indices must be integers, not 'str'，因为这是一个指向json文件的路径，需要读取后进行操作。）
    user_json_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    furni_good_list = read_json(FURNIGOODLIST_PATH)

    # 根据请求信息更新数据
    def buy_furni_group(request_info):
        goods = request_info["goods"]
        cost_type = request_info["costType"]

        total_cost = 0
        
        # 计算总购买花费
        for good in goods:
            good_id = good["id"]
            count = good["count"]
            for furni in furni_good_list["goods"]:
                if furni["goodid"] == good_id:
                    if cost_type == "DIAMOND":
                        total_cost += count * furni["priceDia"]
                    elif cost_type == "COIN_FURN":
                        total_cost += count * furni["priceCoin"]

        # 扣除货币
        if cost_type == "DIAMOND":
            user_json_data["status"]["androidDiamond"] -= total_cost
        elif cost_type == "COIN_FURN":
            user_json_data["inventory"]["3401"] -= total_cost

        # 添加物品
        for good in goods:
            good_id = good["id"]
            count = good["count"]
            for furni_info in user_json_data["FURNI"]["info"]:
                if furni_info["id"] == good_id:
                    furni_info["count"] += count

        # 更新数据
        buy_furni_group(request_info)

        # 将更新后的数据保存回文件
        write_json(USER_JSON_PATH, user_json_data)

    items = []

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

def buyFurniGood():

    user_json_data = read_json(SYNC_DATA_TEMPLATE_PATH)
    furni_good_list = read_json(FURNIGOODLIST_PATH)

    def update_data(request_info):
        good_id = request_info["goodId"]
        buy_count = request_info["buyCount"]
        cost_type = request_info["costType"]

        for furni_info in user_json_data["FURNI"]["info"]:
            if furni_info["id"] == good_id:
                furni_info["count"] += buy_count

        for good in furni_good_list["goods"]:
            if good["goodid"] == good_id:
                if cost_type == "DIAMOND":
                    user_json_data["status"]["androidDiamond"] -= buy_count * good["priceDia"]
                elif cost_type == "COIN_FURN":
                    user_json_data["inventory"]["3401"] -= buy_count * good["priceCoin"]

        update_data(request_info)

        write_json(USER_JSON_PATH, user_json_data)

    items = []

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": user_json_data['user']['skin'],
                "status": user_json_data['user']['status'],
                "shop": user_json_data['user']['shop'],
                "troop": user_json_data['user']['troop'],
                "inventory": user_json_data['user']['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result

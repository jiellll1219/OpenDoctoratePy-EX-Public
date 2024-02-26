from flask import request
from utils import read_json, write_json
from datetime import datetime

from constants import CASHGOODLIST_PATH, EPGSGOODLIST_PATH, EXTRAGOODLIST_PATH, FURNIGOODLIST_PATH, GPGOODLIST_PATH, HIGHGOODLIST_PATH, LMTGOODLIST_PATH, LOWGOODLIST_PATH, REPGOODLIST_PATH, SKINGOODLIST_PATH, SOCIALGOODLIST_PATH, CLASSICGOODLIST_PATH
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

# 购买逻辑基本相同，注释只写一遍
def buySkinGood():

    json_body = request.get_json()
    good_id = json_body.get('goodId')
 
    # 遍历goodList列表
    for good in SKINGOODLIST_PATH['goodList']:
    # 获取originPrice的值
        origin_price = good['originPrice']
 
    # 扣除Diamond货币并添加皮肤
    SYNC_DATA_TEMPLATE_PATH['skin']['characterSkins'][good_id[3:]] = 1
    SYNC_DATA_TEMPLATE_PATH['skin']['skinTs'][good_id[3:]] = int(datetime.now().timestamp())
    SYNC_DATA_TEMPLATE_PATH['status']['androidDiamond'] -= origin_price
    SYNC_DATA_TEMPLATE_PATH['status']['iosDiamond'] -= origin_price

    USER_JSON_PATH['skin']['characterSkins'][good_id[3:]] = 1
    USER_JSON_PATH['skin']['skinTs'][good_id[3:]] = int(datetime.now().timestamp())
    USER_JSON_PATH['status']['androidDiamond'] -= origin_price
    USER_JSON_PATH['status']['iosDiamond'] -= origin_price

    # 返回内容
    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": SYNC_DATA_TEMPLATE_PATH['skin'],
                "status": {
                    "androidDiamond": SYNC_DATA_TEMPLATE_PATH['status']['androidDiamond'],
                    "iosDiamond": SYNC_DATA_TEMPLATE_PATH['status']['iosDiamond']
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

    for low_good in LOWGOODLIST_PATH['goodList']:
        if low_good['goodId'] == good_id:
            SYNC_DATA_TEMPLATE_PATH['status']['lggShard'] -= low_good['price'] * count

            reward_id = low_good['item']['id']
            reward_count = low_good['item']['count'] * count
            for item in USER_JSON_PATH['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": SYNC_DATA_TEMPLATE_PATH['skin'],
                "status": SYNC_DATA_TEMPLATE_PATH['status'],
                "shop": SYNC_DATA_TEMPLATE_PATH['shop'],
                "troop": SYNC_DATA_TEMPLATE_PATH['troop'],
                "inventory": SYNC_DATA_TEMPLATE_PATH['inventory']
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

    for high_good in HIGHGOODLIST_PATH['goodList']:
        if high_good['goodId'] == good_id:
            SYNC_DATA_TEMPLATE_PATH['status']['hggShard'] -= high_good['price'] * count

            reward_id = high_good['item']['id']
            reward_count = high_good['item']['count'] * count
            for item in USER_JSON_PATH['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": SYNC_DATA_TEMPLATE_PATH['skin'],
                "status": SYNC_DATA_TEMPLATE_PATH['status'],
                "shop": SYNC_DATA_TEMPLATE_PATH['shop'],
                "troop": SYNC_DATA_TEMPLATE_PATH['troop'],
                "inventory": SYNC_DATA_TEMPLATE_PATH['inventory']
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

    for extra_good in EXTRAGOODLIST_PATH['goodList']:
        if extra_good['goodId'] == good_id:
            SYNC_DATA_TEMPLATE_PATH['inventory']['4006'] -= extra_good['price'] * count

            reward_id = extra_good['item']['id']
            reward_count = extra_good['item']['count'] * count
            for item in USER_JSON_PATH['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": SYNC_DATA_TEMPLATE_PATH['skin'],
                "status": SYNC_DATA_TEMPLATE_PATH['status'],
                "shop": SYNC_DATA_TEMPLATE_PATH['shop'],
                "troop": SYNC_DATA_TEMPLATE_PATH['troop'],
                "inventory": SYNC_DATA_TEMPLATE_PATH['inventory']
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

    for classic_good in CLASSICGOODLIST_PATH['goodList']:
        if classic_good['goodId'] == good_id:
            SYNC_DATA_TEMPLATE_PATH['status']['REP_COIN'] -= classic_good['price'] * count

            reward_id = classic_good['item']['id']
            reward_count = classic_good['item']['count'] * count
            for item in USER_JSON_PATH['inventory']:
                if item['id'] == reward_id:
                    item['count'] += reward_count

            break

    result = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "skin": SYNC_DATA_TEMPLATE_PATH['skin'],
                "status": SYNC_DATA_TEMPLATE_PATH['status'],
                "shop": SYNC_DATA_TEMPLATE_PATH['shop'],
                "troop": SYNC_DATA_TEMPLATE_PATH['troop'],
                "inventory": SYNC_DATA_TEMPLATE_PATH['inventory']
            }
        },
        "items": items,
        "result": 0
    }

    return result
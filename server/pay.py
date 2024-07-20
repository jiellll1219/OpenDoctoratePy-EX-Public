from flask import request
from utils import read_json, write_json
from datetime import datetime, timezone
from admin.GiveItem import GiveItem
import json

from constants import ALLPRODUCTLIST_PATH, CASHGOODLIST_PATH, SYNC_DATA_TEMPLATE_PATH, GPGOODLIST_PATH

timestamp = datetime.now(timezone.utc).isoformat()

def GetUnconfirmedOrderIdList():

    data = request.data
    data = {
        "orderIdList": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

    return data

def getAllProductList():

    data = request.data
    data = read_json(ALLPRODUCTLIST_PATH,encoding='utf-8')

    return data

def getcreateOrder():

    goodid = json.loads(request.data)
    data = {
    "playerDataDelta": {
        "modified": {},
        "deleted": {}
    },
    "result": 0,
    "orderId": goodid["goodId"],
    "orderIdList": []
}

    return data


def createOrderAlipay():

    data = request.data
    data = {
        "timestamp":timestamp,
        "status":200,
        "message":"OK",
        "path":"/pay/createOrderAlipay"
    }

    return data

def createOrderWechat():

    data = request.data
    data = {
        "timestamp":timestamp,
        "status":200,
        "message":"OK",
        "path":"/pay/createOrderWechat"
    }

    return data

def payconfirmOrder():

    data = {
        "status": 0
    }

    return data

def payconfirmOrderAlipay():

    data = {
        "status": 0
    }

    return data

def confirmOrder(good_id, cash_good):

    if good_id.startswith("GP_"):
        if good_id.startswith("GP_gW"):
            GP_items = GPGOODLIST_PATH["weeklyGroup"]["packages"][good_id]["items"]
        elif good_id.startswith("GP_gM"):
            GP_items = GPGOODLIST_PATH["monthlyGroup"]["packages"][good_id]["items"]
        elif good_id.startswith("GP_Once"):
            GP_items = GPGOODLIST_PATH["oneTimeGP"]
            for i in range(GP_items.size()):
                if GP_items.getJSONObject(i).getString("goodId").equals(good_id):
                    GP_items = GP_items.getJSONObject(i).getJSONArray("items")
                    break
        for i in range(GP_items.size()):
            reward_id = GP_items["id"]
            reward_type = GP_items["type"]
            reward_count = GP_items["count"]
            read_json[SYNC_DATA_TEMPLATE_PATH][reward_id][reward_type][reward_count]
    else:
        if cash_good.booleanValue():
            CS = True
            CS["id"] = good_id
            CS["count"] = 1
            SYNC_DATA_TEMPLATE_PATH["receiveItems"]["items"].append(CS)

            diamond_num = cash_good.getIntValue("doubleCount")
        else:
            diamond_num = SYNC_DATA_TEMPLATE_PATH["status"]["androidDiamond"] + SYNC_DATA_TEMPLATE_PATH["status"]["iosDiamond"]

        SYNC_DATA_TEMPLATE_PATH["status"]["androidDiamond"] += diamond_num
        SYNC_DATA_TEMPLATE_PATH["status"]["iosDiamond"] += diamond_num

        item = True
        item["id"] = "4002"
        item["type"] = "DIAMOND"
        item["count"] = diamond_num
        SYNC_DATA_TEMPLATE_PATH["receiveItems"]["items"].append(item)

    write_json(SYNC_DATA_TEMPLATE_PATH)

    result = True
    result["playerDataDelta"] = True
    result["result"] = 0
    result["receiveItems"] = True

    return result

def confirmOrderAlipay():

    return {
        "result": 0
    }

def confirmOrderWechat():

    return {
        "result": 0
    }

def confirmorder(secret, json_body, response):

    good_id = json_body["orderId"]

    items = []
    receive_items = {}

    if "CS" in good_id:
        CashGood = {}
        for i in range(len(CASHGOODLIST_PATH["goodList"])):
            if CASHGOODLIST_PATH["goodList"][i]["goodId"] == good_id:
                CashGood = CASHGOODLIST_PATH["goodList"][i]
                break

        double_cash = True
        info = SYNC_DATA_TEMPLATE_PATH["shop"]["CASH"]["info"]

        diamond_num = 0
        for j in range(len(info)):
            id = info[j]["id"]
            if id == good_id:
                double_cash = False
                break

        if double_cash:
            CS = {"id": good_id, "count": 1}
            info.append(CS)
            diamond_num = CashGood["doubleCount"]
        else:
            diamond_num = CashGood["diamondNum"] + CashGood["plusNum"]

        write_json (SYNC_DATA_TEMPLATE_PATH)["status"]["androidDiamond"] += diamond_num
        write_json (SYNC_DATA_TEMPLATE_PATH)["status"]["iosDiamond"] += diamond_num

        item = {"id": "4002", "type": "DIAMOND", "count": diamond_num}
        items.append(item)

    if "GP_" in good_id:
        GPItems = []

        if "GP_gW" in good_id:
            GPItems = GPGOODLIST_PATH["weeklyGroup"]["packages"][good_id]["items"]

        if "GP_gM" in good_id:
            GPItems = GPGOODLIST_PATH["monthlyGroup"]["packages"][good_id]["items"]

        if "GP_Once" in good_id:
            for j in range(len(GPGOODLIST_PATH["oneTimeGP"])):
                if GPGOODLIST_PATH["oneTimeGP"][j]["goodId"] == good_id:
                    GPItems = GPGOODLIST_PATH["oneTimeGP"][j]["items"]
                    break

        for i in range(len(GPItems)):
            reward_id = GPItems[i]["id"]
            reward_type = GPItems[i]["type"]
            reward_count = GPItems[i]["count"]

            GiveItem(SYNC_DATA_TEMPLATE_PATH, reward_id, reward_type, reward_count, items)

    write_json(SYNC_DATA_TEMPLATE_PATH)

    result = {}
    playerDataDelta = {}
    modified = {}

    receive_items["items"] = items

    modified["status"] = SYNC_DATA_TEMPLATE_PATH["status"]
    modified["shop"] = SYNC_DATA_TEMPLATE_PATH["shop"]
    modified["troop"] = SYNC_DATA_TEMPLATE_PATH["troop"]
    modified["skin"] = SYNC_DATA_TEMPLATE_PATH["skin"]
    modified["inventory"] = SYNC_DATA_TEMPLATE_PATH["inventory"]
    playerDataDelta["modified"] = modified
    playerDataDelta["deleted"] = {}
    result["playerDataDelta"] = playerDataDelta
    result["result"] = 0
    result["receiveItems"] = receive_items
    return result

def confirmOrderState():

    return {
        "status": 200,
        "data": {
            "payState": 3
        }
    }

from flask import request
from utils import read_json, write_json
from datetime import datetime, timezone

from constants import ALLPRODUCTLIST_PATH, CASHGOODLIST_PATH

timestamp = datetime.now(timezone.utc).isoformat()

def payGetUnconfirmedOrderIdList():

    data = request.data
    data = {
        "orderIdList": [],
        "playerDataDelta": {
            "deleted": {},
            "modified": {}
        }
    }

    return data


def paygetAllProductList():

    data = request.data
    data = read_json(ALLPRODUCTLIST_PATH,encoding='utf-8')

    return data

def paygetcreateOrder():

    data = request.data
    data = {
    "playerDataDelta": {
        "modified": {},
        "deleted": {}
    },
    "result": 0,
    "orderId": CASHGOODLIST_PATH["goodList"]["goodId"],
    "orderIdList": []
}

    return data


def createOrderAlipay():

    data = request.data
    data = {
        "timestamp":timestamp,
        "status":404,
        "error":"Not Found",
        "message":"",
        "path":"/pay/createOrderAlipay"
    }

    return data

def createOrderWechat():

    data = request.data
    data = {
        "timestamp":timestamp,
        "status":404,
        "error":"Not Found",
        "message":"",
        "path":"/pay/createOrderWechat"
    }

    return data

from flask import request

from constants import TEMPLATE_SHOP_PATH
from utils import read_json


def getGoodList():
    shop_id = str(request.get_json()["shopId"])
    data = read_json(TEMPLATE_SHOP_PATH)[shop_id]
    return {
        "data": data,
        "nextSyncTime": -1,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }


def buyGood():
    json_body = request.get_json

    return json_body

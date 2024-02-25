from flask import request
from utils import read_json, write_json

from constants import CASHGOODLIST_PATH, EPGSGOODLIST_PATH, EXTRAGOODLIST_PATH, FURNIGOODLIST_PATH, GPGOODLIST_PATH, HIGHGOODLIST_PATH, LMTGOODLIST_PATH, LOWGOODLIST_PATH, REPGOODLIST_PATH, SKINGOODLIST_PATH, SOCIALGOODLIST_PATH, CLASSICGOODLIST_PATH

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
from time import time

from flask import request

from constants import MAILLIST_PATH
from utils import read_json, write_json


def mailGetMetaInfoList():

    data = request.data

    result = []
    mail_data = read_json(MAILLIST_PATH, encoding="utf-8")
    
    for mailId in mail_data["mailList"]:

        if int(mailId) in mail_data["deletedIDs"]:
            continue

        config = {
            "createAt": round(time()),
            "hasItem": 1,
            "mailId": mailId,
            "state": 1 if int(mailId) in mail_data["recievedIDs"] else 0,
            "type": 1
        }
        
        result.append(config)

    data = {
        "result": result,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def mailListMailBox():

    data = request.data
    mails = []
    hasGift = 0
    mail_data = read_json(MAILLIST_PATH, encoding="utf-8")

    for mailId in mail_data["mailList"]:

        if int(mailId) in mail_data["deletedIDs"]:
            continue

        if int(mailId) not in mail_data["recievedIDs"]:
            hasGift = 1

        config = {
            "createAt": round(time()),
            "expireAt": round(time()) + 31536000,
            "mailId": mailId,
            "platform": -1,
            "state": 1 if int(mailId) in mail_data["recievedIDs"] else 0,
            "style": {},
            "type": 1,
            "uid": ""
        }

        mails.append(dict(mail_data["mailList"][str(mailId)], **config))

    data = {
        "mailList": mails,
        "playerDataDelta": {
            "modified": {
                "pushFlags": {
                    "hasGifts": hasGift
                }
            },
            "deleted": {}
        }
    }

    return data


def getItems(request_data, key):

    items = []
    hasGift = 1
    mail_data = read_json(MAILLIST_PATH, encoding="utf-8")

    getIDList = request_data[key]
    if key != "sysMailIdList":
        getIDList = [request_data[key]]

    for mailId in getIDList:
        mail_data["recievedIDs"].append(int(mailId))

        if "items" in mail_data["mailList"][str(mailId)].keys():
            items += mail_data["mailList"][str(mailId)]["items"]
    
    if len(mail_data["mailList"]) == len(mail_data["recievedIDs"]):
        hasGift = 0

    write_json(mail_data, MAILLIST_PATH)

    return items, hasGift


def mailReceiveMail():
    
    data = request.data
    request_data = request.get_json()

    result = getItems(request_data, "mailId")

    data = {
        "items": result[0],
        "playerDataDelta": {
            "modified": {
                "consumable": {}, # TODO
                "inventory":{},
                "pushFlags": {
                    "hasGifts": result[1]
                },
                "status": {}
            },
            "deleted": {}
        }
    }

    return data


def mailReceiveAllMail():

    data = request.data
    request_data = request.get_json()

    result = getItems(request_data, "sysMailIdList")

    data = {
        "items": result[0],
        "playerDataDelta": {
            "modified": {
                "consumable": {}, # TODO
                "inventory":{},
                "pushFlags": {
                    "hasGifts": 0
                },
                "status": {}
            },
            "deleted": {}
        }
    }
    
    return data


def mailRemoveAllReceivedMail():

    data = request.data
    request_data = request.get_json()
    mail_data = read_json(MAILLIST_PATH, encoding="utf-8")

    for mailId in request_data["sysMailIdList"]:
        if mailId not in mail_data["deletedIDs"]:
            mail_data["deletedIDs"].append(mailId)

    write_json(mail_data, MAILLIST_PATH)

    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data
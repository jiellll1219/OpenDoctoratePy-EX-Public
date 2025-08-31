from virtualtime import time

from flask import request

from constants import MAILLIST_PATH, MAILCOLLECTION_PATH
from utils import read_json, write_json


# 获取邮件列表的元信息
def mailGetMetaInfoList():

    # 获取请求的数据
    data = request.data

    # 初始化结果列表
    result = []
    # 读取邮件列表数据
    mail_data = read_json(MAILLIST_PATH)
    
    # 遍历邮件列表
    for mailId in mail_data["mailList"]:

        # 如果邮件ID在已删除的ID列表中，则跳过
        if int(mailId) in mail_data["deletedIDs"]:
            continue

        # 构造邮件元信息
        config = {
            "createAt": round(time()),
            "hasItem": 1,
            "mailId": mailId,
            "state": 1 if int(mailId) in mail_data["recievedIDs"] else 0,
            "type": 1
        }
        
        # 将邮件元信息添加到结果列表中
        result.append(config)

    # 构造返回数据
    data = {
        "result": result,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    # 返回数据
    return data


# 获取邮件列表
def mailListMailBox():

    # 获取请求的数据
    data = request.data
    # 初始化邮件列表
    mails = []
    # 初始化是否有礼物
    hasGift = 0
    # 读取邮件列表数据
    mail_data = read_json(MAILLIST_PATH)

    # 遍历邮件列表
    for mailId in mail_data["mailList"]:

        # 如果邮件ID在已删除的ID列表中，则跳过
        if int(mailId) in mail_data["deletedIDs"]:
            continue

        # 如果邮件ID不在已接收的ID列表中，则将是否有礼物标记为1
        if int(mailId) not in mail_data["recievedIDs"]:
            hasGift = 1

        # 构造邮件信息
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

        # 将邮件信息添加到邮件列表中
        mails.append(dict(mail_data["mailList"][str(mailId)], **config))

    # 构造返回数据
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

    # 返回数据
    return data


# 获取邮件中的物品
def getItems(request_data, key):

    # 初始化物品列表
    items = []
    # 初始化是否有礼物
    hasGift = 1
    # 读取邮件列表数据
    mail_data = read_json(MAILLIST_PATH)

    # 获取邮件ID列表
    getIDList = request_data[key]
    # 如果key不是sysMailIdList，则将getIDList转换为列表
    if key != "sysMailIdList":
        getIDList = [request_data[key]]

    # 遍历邮件ID列表
    for mailId in getIDList:
        # 将邮件ID添加到已接收的ID列表中
        mail_data["recievedIDs"].append(int(mailId))

        # 如果邮件中有物品，则将物品添加到物品列表中
        if "items" in mail_data["mailList"][str(mailId)].keys():
            items += mail_data["mailList"][str(mailId)]["items"]
    
    # 如果邮件列表中的邮件数量等于已接收的邮件数量，则将是否有礼物标记为0
    if len(mail_data["mailList"]) == len(mail_data["recievedIDs"]):
        hasGift = 0

    # 将邮件列表数据写入文件
    write_json(mail_data, MAILLIST_PATH)

    # 返回物品列表和是否有礼物
    return items, hasGift


# 接收邮件
def mailReceiveMail():
    
    # 获取请求的数据
    data = request.data
    # 获取请求的JSON数据
    request_data = request.get_json()

    # 获取邮件中的物品和是否有礼物
    result = getItems(request_data, "mailId")

    # 构造返回数据
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

    # 返回数据
    return data


# 接收所有邮件
def mailReceiveAllMail():

    # 获取请求的数据
    data = request.data
    # 获取请求的JSON数据
    request_data = request.get_json()

    # 获取邮件中的物品和是否有礼物
    result = getItems(request_data, "sysMailIdList")

    # 构造返回数据
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
    
    # 返回数据
    return data


# 移除所有已接收的邮件
def mailRemoveAllReceivedMail():

    # 获取请求的数据
    data = request.data
    # 获取请求的JSON数据
    request_data = request.get_json()
    # 读取邮件列表数据
    mail_data = read_json(MAILLIST_PATH)

    # 遍历已接收的邮件ID列表
    for mailId in request_data["sysMailIdList"]:
        # 如果邮件ID不在已删除的ID列表中，则将其添加到已删除的ID列表中
        if mailId not in mail_data["deletedIDs"]:
            mail_data["deletedIDs"].append(mailId)

    # 将邮件列表数据写入文件
    write_json(mail_data, MAILLIST_PATH)

    # 构造返回数据
    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    # 返回数据
    return data

def mailCollectionGetList():

    mailcollect_data = read_json(MAILCOLLECTION_PATH)

    return mailcollect_data
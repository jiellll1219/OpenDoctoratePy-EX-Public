import json

import requests
from flask import request

from constants import USER_JSON_PATH, SYNC_DATA_TEMPLATE_PATH
from utils import read_json, write_json

import time


def userCheckIn():

    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def userChangeSecretary():
    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]
    data = {
        "playerDataDelta": {
            "modified": {
                "status": {
                    "secretary": "",
                    "secretarySkinId": "",
                }
            },
            "deleted": {},
        }
    }

    if charInstId and skinId:
        data["playerDataDelta"]["modified"]["status"]["secretary"] = (
            skinId.split("@")[0] if "@" in skinId else skinId.split("#")[0]
        )
        data["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = skinId
        saved_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf-8")
        saved_data["user"]["status"]["secretary"] = (
            skinId.split("@")[0] if "@" in skinId else skinId.split("#")[0]
        )
        saved_data["user"]["status"]["secretarySkinId"] = skinId
        write_json(saved_data, SYNC_DATA_TEMPLATE_PATH)
    return data


def userLogin():

    data = request.data
    data = {
        "accessToken": "1",
        "birth": None,
        "channelId": "",
        "isAuthenticate": True,
        "isLatestUserAgreement": True,
        "isMinor": False,
        "needAuthenticate": False,
        "result": 0,
        "token": "abcd",
        "yostar_username": "1234567890@123.com",
        "yostar_uid": "1",
        "uid": "10000023"
    }

    return data


def userOAuth2V1Grant():
    
    data = request.data
    data = {
        "data": {
            "code": "abcd",
            "uid": "10000023"
        },
        "msg": "OK",
        "status": 0
    }

    return data


def userV1NeedCloudAuth():

    data = request.data
    data = {
        "msg": "OK",
        "status": 0
    }
    
    return data


def userV1getToken():

    data = request.data
    data = {
        "channelUid": "1",
        "error": "",
        "extension": json.dumps({
            "isMinor": False,
            "isAuthenticate": True
        }),
        "isGuest": 0,
        "result": 0,
        "token": "abcd",
        "uid": "10000023"
    }

    return data


def userAuth():

    data = request.data
    data = {
        "isAuthenticate": True,
        "isGuest": False,
        "isLatestUserAgreement": True,
        "isMinor": False,
        "needAuthenticate": False,
        "uid": "10000023"
    }

    return data


def userChangeAvatar():

    data = request.data
    avatar = request.get_json()

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["status"]["avatar"] = avatar
    write_json(saved_data, USER_JSON_PATH)

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "status": {
                    "avatar": avatar
                }
            }
        }
    }

    return data


def appGetSettings():

    data = request.data
    data = requests.get("https://passport.arknights.global/app/getSettings").json()
    return data


def appGetCode():

    data = request.data
    data = requests.get("https://passport.arknights.global/app/getCode").json()
    return data


def userYostarCreatelogin():

    data = request.data
    data = {
        "isNew": 0,
        "result": 0,
        "token": "1",
        "uid": "10000023",
        "yostar_uid": "1",
        "yostar_username": "1234567890@123.com"
    }

    return data

def userAgreement():

    data = request.data
    data = {
        "data": [
            "¯\_(ツ)_/¯"
        ],
        "version": "4.0.0"
    }

    return data

def auth_v1_token_by_phone_password():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "token": "doctorate"
        }
    }


def info_v1_basic():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "hgId": "1",
            "phone": "12345678901",
            "email": "1234567890@123.com",
            "identityNum": "10000023",
            "identityName": "JieG",
            "isMinor": False,
            "isLatestUserAgreement": True
        }
    }


def oauth2_v2_grant():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "code": "JieG",
            "uid": "10000023"
        }
    }


def app_v1_config():
    return {
    "status": 0,
    "msg": "OK",
    "data": {
        "antiAddiction": {
            "minorPeriodEnd": 21,
            "minorPeriodStart": 20
        },
        "payment": [
            {
                "key": "alipay",
                "recommend": True
            },
            {
                "key": "wechat",
                "recommend": False
            },
            {
                "key": "pcredit",
                "recommend": False
            }
        ],
        "customerServiceUrl": "https://chat.hypergryph.com/chat/h5/v2/index.html",
        "cancelDeactivateUrl": "https://user.hypergryph.com/cancellation",
        "agreementUrl": {
            "game": "https://user.hypergryph.com/protocol/plain/ak/index",
            "unbind": "https://user.hypergryph.com/protocol/plain/ak/cancellation",
            "account": "https://user.hypergryph.com/protocol/plain/index",
            "privacy": "https://user.hypergryph.com/protocol/plain/privacy",
            "register": "https://user.hypergryph.com/protocol/plain/registration",
            "updateOverview": "https://user.hypergryph.com/protocol/plain/overview_of_changes",
            "childrenPrivacy": "https://user.hypergryph.com/protocol/plain/children_privacy"
        },
        "app": {
            "enablePayment": True,
            "enableAutoLogin": False,
            "enableAuthenticate": True,
            "enableAntiAddiction": True,
            "wechatAppId": "",
            "alipayAppId": "",
            "oneLoginAppId": "",
            "enablePaidApp": False,
            "appName": "明日方舟",
            "appAmount": 600
        }
    }
}



def general_v1_server_time():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "serverTime": int(time.time()),
            "isHoliday": False
        }
    }
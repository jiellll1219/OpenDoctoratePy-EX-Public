import json

import requests
from flask import request
from random import random

from constants import USER_JSON_PATH, SYNC_DATA_TEMPLATE_PATH
from utils import read_json, write_json, run_after_response

import time


def CheckIn():
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf-8")
    user_data = read_json(USER_JSON_PATH, encoding="utf-8")
    checkin_data = sync_data["user"]["checkIn"]
    checkin_data["canCheckIn"] = 0
    checkin_data["showCount"] += 1
    checkin_data["checkInHistory"].append(0)
    sync_data["user"]["checkIn"] = checkin_data
    user_data["user"]["checkIn"] = checkin_data
    result = {
        "result": 0,
        "playerDataDelta": {
            "modified": {
                "checkIn": {
                    "canCheckIn": 0,
                    "showCount": checkin_data["showCount"],
                    "checkInHistory": checkin_data["checkInHistory"],
                }
            },
            "deleted": {}
        }
    }

    run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)
    run_after_response(write_json, user_data, USER_JSON_PATH)
    return result


def ChangeSecretary():
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


def Login():

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


def OAuth2V1Grant():
    
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


def V1NeedCloudAuth():

    data = request.data
    data = {
        "msg": "OK",
        "status": 0
    }
    
    return data


def V1getToken():

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


def Auth():

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


def ChangeAvatar():

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


def YostarCreatelogin():

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

def Agreement():

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

def auth_v2_token_by_phone_code():
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
        "customerServiceUrl": "https://chat.hypergryph.com/chat/h5/v2/index.html?sysnum=889ee281e3564ddf883942fe85764d44&channelid=2",
        "cancelDeactivateUrl": "https://user.hypergryph.com/cancellation",
        "agreementUrl": {
            "game": "https://user.hypergryph.com/protocol/plain/ak/index",
            "unbind": "https://user.hypergryph.com/protocol/plain/ak/cancellation",
            "gameService": "https://user.hypergryph.com/protocol/plain/ak/service",
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
            "enableUnbindGrant": True,
            "wechatAppId": "wx0ae7fb63d830f7c1",
            "alipayAppId": "2018091261385264",
            "oneLoginAppId": "7af226e84f13f17bd256eca8e1e61b5a",
            "enablePaidApp": False,
            "appName": "明日方舟",
            "appAmount": 600,
            "needShowName": False,
            "customerServiceUrl": "https://customer-service.hypergryph.com/ak?hg_token={hg_token}&source_from=sdk",
            "needAntiAddictionAlert": True,
            "enableScanLogin": False,
            "deviceCheckMode": 2,
            "enableGiftCode": True
        },
        "scanUrl": {
            "login": "hypergryph://scan_login"
        },
        "userCenterUrl": "https://user.hypergryph.com/pcSdk/userInfo"
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

def userSend_phone_code():
    return {
        "msg": "OK",
        "status": 0,
        "type": "A"
    }

def exchangeDiamondShard():
    json_body = json.loads(request.data)
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    #debug code
    print(request.data)

    use_count = json_body["count"]
    user_androidDiamond = user_sync_data["user"]["status"]["androidDiamond"]

    if user_androidDiamond < use_count:
        return {
            "result": 1,
            "errMsg": "剩余源石无法兑换合成玉"
        }
    else:
        user_sync_data["user"]["status"]["androidDiamond"] -= use_count
        user_sync_data["user"]["status"]["diamondShard"] += use_count * 180
        user_sync_data["user"]["status"]["iosDiamond"] = user_sync_data["user"]["status"]["androidDiamond"]
        
    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)
    
    result = {
        "playerDataDelta": {
            "modified": {
                "androidDiamond": user_sync_data["user"]["status"]["androidDiamond"],
                "iosDiamond": user_sync_data["user"]["status"]["iosDiamond"],
                "diamondShard":user_sync_data["user"]["status"]["diamondShard"]
            },
            "deleted": {}
        }
    }

    return result

def bindNickName():
    json_body = json.loads(request.data)
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    nickName = json_body["nickName"]

    if len(nickName) > 8 :
        return {
            "result": 1
        }
    elif '/' in nickName:
        return {
            "result": 2
        }
    else:
        #nickNumber = f"{len(user_sql.query_nick_name(nick_name)) + 1:04d}"  #在sql中使用
        nickNumber = "0001"  #在单人服务器中使用
        user_sync_data = (user_sync_data["user"]["status"]["nickNumber"], nickNumber)
        user_sync_data = (user_sync_data["user"]["status"]["nickName"], nickName)

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    result = {
        "deleted": {},
        "modified": {
            "status": {
                "nickName": nickName
            }
        }
    }

    return result
    
def rebindNickName():
    json_body = json.loads(request.data)
    user_sync_data = SYNC_DATA_TEMPLATE_PATH

    nick_name = json_body['nickName']

    user_sync_data["user"]["status"]["nickName"] = nick_name
    user_sync_data["user"]["inventory"]["renamingCard"] -= 1

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)
    write_json(user_sync_data, USER_JSON_PATH)

    return {
        "playerDataDelta": {
        "deleted": {},
        "modified": {
            "status": {"nickName": nick_name},
            "inventory": {"renamingCard": user_sync_data["inventory"]["renamingCard"]}
            }
        }
    }
    
def BuyAP():
    user_sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

    now_time = time()

    add_ap = (now_time - user_sync_data["user"]["status"]["lastApAddTime"]) // 360

    if user_sync_data["user"]["status"]["ap"] < user_sync_data["user"]["status"]["maxAp"]:
        if user_sync_data["user"]["status"]["ap"] + add_ap >= user_sync_data["user"]["status"]["maxAp"]:
            user_sync_data["user"]["status"]["ap"] = user_sync_data["user"]["status"]["maxAp"]
            user_sync_data["user"]["status"]["lastApAddTime"] = now_time
        elif add_ap != 0:
            user_sync_data["user"]["status"]["ap"] += add_ap
            user_sync_data["user"]["status"]["lastApAddTime"] = now_time

    user_sync_data["user"]["status"]["androidDiamond"] -= 1
    user_sync_data["user"]["status"]["iosDiamond"] = user_sync_data["user"]["status"]["androidDiamond"]
    user_sync_data["user"]["status"]["ap"] += user_sync_data["user"]["status"]["maxAp"]
    user_sync_data["user"]["status"]["lastApAddTime"] = now_time
    user_sync_data["user"]["status"]["buyApRemainTimes"] = user_sync_data["user"]["status"]["buyApRemainTimes"]

    write_json(user_sync_data, SYNC_DATA_TEMPLATE_PATH)

    return {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "status": {
                    "androidDiamond": user_sync_data["user"]["status"]["androidDiamond"],
                    "iosDiamond": user_sync_data["user"]["status"]["iosDiamond"],
                    "ap": user_sync_data["user"]["status"]["ap"],
                    "lastApAddTime": user_sync_data["user"]["status"]["lastApAddTime"],
                    "buyApRemainTimes": user_sync_data["user"]["status"]["buyApRemainTimes"]
                }
            }
        }
    }

def changeResume():
    return {
        "playerDataDelta": {
            "modified": {"status": {"resume": request.get_json()["resume"]}},
            "deleted": {},
        }
    }

def getOtherPlayerNameCard():

    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH, encoding="utf-8")

    assist_list = [user_data["troop"]["chars"].keys()]
    assist_char_id = assist_list[random.randint(0, len(assist_list) - 1)]
    assist_char_num_id = int(assist_char_id.split("_")[1])

    assist_char_obj = user_data["troop"]["chars"][str(assist_char_num_id)].copy()
    nickNumber = int(random.randint(1, 9999))

    result = {
        "nameCard": {
            "nickName": "ABCDEFG",
            "nickNumber": f"{nickNumber:04d}",
            "uid": json_body["uid"],
            "registerTs": 1700000000,
            "mainStageProgress": None,
            "charCnt": 0,
            "skinCnt": 0,
            "secretary": "char_002_amiya",
            "secretarySkinId": "char_002_amiya#1",
            "resume": "",
            "teamV2": {},
            "level": 200,  
            "avatarId": "0",
            "avatar": {
                "type": "ICON",
                "id": "avatar_def_01"
            },
            "assistCharList": [
                assist_char_obj,
                None,
                None
            ],
            "medalBoard": {
                "type": "EMPTY",
                "custom": None,
                "template": None
            },
            "nameCardStyle": {
                "componentOrder": [
                    "module_sign",
                    "module_assist",
                    "module_medal"
                ],
                "skin": {
                    "selected": "nc_rhodes_default",
                    "state": {}
                },
                "misc": {
                    "showDetail": True,
                    "showBirthday": False
                }
            }
        }
    }
    return result

def businessCard_changeNameCardComponent():
    json_body = request.get_json()
    return {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": {"componentOrder": json_body["component"]}
            },
            "deleted": {},
        }
    }


def businessCard_changeNameCardSkin():
    json_body = request.get_json()
    return {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": {"skin": {"selected": json_body["skinId"]}}
            },
            "deleted": {},
        }
    }

def editNameCard():
    json_body = request.get_json()
    sync_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf-8")
    user_data = read_json(USER_JSON_PATH, encoding="utf-8")
    nameCardStyle_data = sync_data["user"]["nameCardStyle"]
    modified_data = json_body["content"]

    if modified_data["skinId"] is not None:
        nameCardStyle_data["skin"]["selected"] = modified_data["skinId"]

    if modified_data["component"] is not None:
        nameCardStyle_data["componentOrder"] = modified_data["component"]

    if modified_data["misc"] is not None:
        nameCardStyle_data["misc"]["showDetail"] = bool(modified_data["misc"]["showDetail"])
        nameCardStyle_data["misc"]["showBirthday"] = bool(modified_data["misc"]["showBirthday"])

    user_data["user"]["nameCardStyle"] = nameCardStyle_data

    result = {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": nameCardStyle_data
            },
            "deleted": {},
        }
    }

    run_after_response(write_json, sync_data, USER_JSON_PATH)
    run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)

    return result

def bindBirthday():

    json_body = request.get_json()

    user_data = read_json(USER_JSON_PATH, encoding="utf-8")
    user_data["user"]["status"]["birthday"] = {
        "month": -1,
        "day": -1
    }
    user_data["user"]["status"]["birthday"]["month"] = int(json_body["month"])
    user_data["user"]["status"]["birthday"]["day"] = int(json_body["day"])

    write_json(USER_JSON_PATH, user_data, encoding="utf-8")

    return {
        "playerDataDelta": {
            "modified": {
                "user": {
                    "status": {
                        "birthday": {
                            "month": json_body["month"],
                            "day": json_body["day"],
                        }
                    }
                }
            }
        }
    }

def agreement_version():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "agreementUrl": {
                "privacy": "https://user.hypergryph.com/protocol/plain/ak/privacy",
                "service": "https://user.hypergryph.com/protocol/plain/ak/service",
                "updateOverview": "https://user.hypergryph.com/protocol/plain/ak/overview_of_changes",
                "childrenPrivacy": "https://user.hypergryph.com/protocol/plain/ak/children_privacy",
            },
            "authorized": True,
            "isLatestUserAgreement": True,
        },
    }
from flask import request
from virtualtime import time
from utils import read_json, write_json
from constants import (
    SYNC_DATA_TEMPLATE_PATH
)
import random

class CheckInReward():
    # 这个类用于处理活动签到奖励
    def __init__(self):
        # 需要用到用户数据时，传参里添加self，使用 self.user_data 获取用户数据
        self.user_data = read_json(SYNC_DATA_TEMPLATE_PATH, encoding="utf-8")
        
    def getCheckInReward(self):
        json_body = request.get_json()
        user_data = self.user_data
        access_id = json_body["activityId"]

        if access_id == "act2access":
            rewardsCnt = user_data["user"]["activity"]["CHECKIN_ACCESS"]["act2access"]["rewardsCount"]
            content = {
                "items": [
                    {
                        "type": "AP_SUPPLY",
                        "id": "ap_supply_lt_80",
                        "count": 1
                    },
                    {
                        "type": "DIAMOND_SHD",
                        "id": "4003",
                        "count": 200
                    }
                ]
            }
            
            modified = {
                "activity": {
                    "CHECKIN_ACCESS": {
                        access_id: {
                            "currentStatus": 0,
                            "lastTs": time(),
                            "rewardsCount": rewardsCnt + 1
                        }
                    }
                }
            }

        result = {
            "playerDataDelta": {
                "modified": modified,
                "deleted": {}
            },
            "content": content
        }

        return result

    def getActivityCheckInReward(self):

        json_body = request.get_json()

        activity_id = json_body["activityId"]
        target_index = json_body["index"]
        user_data = self.user_data
        activity_data = user_data["user"]["activity"]["CHECKIN_ONLY"][activity_id]

        activity_data["history"][target_index] = 0

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "CHECKIN_ONLY": {
                            activity_id: activity_data
                        }
                    }
                },
                "deleted": {}
            }
        }

        return result
    
    def getReward(self):
        # 签到墙奖励
        json_body = request.get_json()
        # {'prayArray': [0, 1], 'activityId': 'act11pray'}
        user_data = self.user_data
        activity_id = json_body["activityId"]
        activity_data = user_data["user"]["activity"]["PRAY_ONLY"][activity_id]

        activity_data["lastTs"] = time()
        activity_data["praying"] = True

        count_list = [200, 300, 400, 500, 600, 700, 800]
        random.shuffle(count_list)
        count_1 = random.choice(count_list)
        random.shuffle(count_list)
        count_2 = random.choice(count_list)
        if count_1 >= count_2:
            activity_data["prayMaxIndex"] = json_body["prayArray"][0]
        else:
            activity_data["prayMaxIndex"] = json_body["prayArray"][1]

        activity_data["prayArray"] = [
            {
                "index": json_body["prayArray"][0],
                "count": count_1
            },
            {
                "index": json_body["prayArray"][1],
                "count": count_2
            }
        ]

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "PRAY_ONLY": {
                            activity_id: activity_data
                        }
                    }
                },
                "deleted": {}
            }
        }

        return result


class enemyDuel():
    def singleBattleStart():

        return{
            "pushMessage": [],
            "result": 0,
            "battleId": "abcdefgh-1234-5678-a1b2c3d4e5f6",
        }

    def singleBattleFinish():

        json_body = request.get_json()

        rankList = json_body["settle"]["rankList"]

        result = {
            "result": 0,
            "apFailReturn": 0,
            "itemReturn": [],
            "rewards": [],
            "unusualRewards": [],
            "overrideRewards": [],
            "additionalRewards": [],
            "diamondMaterialRewards": [],
            "furnitureRewards": [],
            "goldScale": 0.0,
            "expScale": 0.0,
            "firstRewards": [],
            "unlockStages": None,
            "pryResult": [],
            "alert": [],
            "suggestFriend": False,
            "extra": None,
            "choiceCnt": {
                "skip": 0,
                "normal": 5,
                "allIn": 1
            },
            "commentId": "Comment_Operation_7",
            "isHighScore": False,
            "rankList": rankList,
            "dailyMission": {
                "add": 0,
                "reward": 0
            },
            "bp": 0
        }

        return result
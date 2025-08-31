from flask import request
from virtualtime import time
from utils import read_json, write_json, run_after_response
from constants import (
    SYNC_DATA_TEMPLATE_PATH
)
import random

class CheckInReward():
    # 这个类用于处理活动签到奖励
    def __init__(self):
        # 需要用到用户数据时，传参里添加self，使用 self.user_data 获取用户数据
        self.user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        
    def getCheckInReward(self):
        json_body = request.get_json()
        user_data = self.user_data
        access_id = json_body["activityId"]

        if access_id == "act2access":
            rewardsCnt = user_data["user"]["activity"]["CHECKIN_ACCESS"]["act2access"]["rewardsCount"]
            items = [
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
            "items": items
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

    def sign(self):
        json_body = request.get_json()
        user_data = self.user_data
        act_id = json_body["actId"]
        act_data = user_data["user"]["activity"]["CHECKIN_VS"][act_id]

        act_data["signedCnt"] += 1
        act_data["canVote"] = 0
        if json_body["tasteChoice"] == 1:
            act_data["sweetVote"] += 1
        else:
            act_data["saltyVote"] += 1
        act_data["voteRewardState"] = 0

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "CHECKIN_VS": {
                            act_id: act_data
                        }
                    }
                },
                "deleted": {}
            },
            "items": [
                {
                "type": "AP_SUPPLY",
                "id": "ap_supply_lt_120",
                "count": 1
                },
                {
                "type": "GOLD",
                "id": "4001",
                "count": 30000
                }
            ]
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
    
class act35side():

    def __init__(self):
        # 回合数据
        self.round_data_map = {
            "challenge_1_r1": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_1_r2": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_3_r1": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_3_r2": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_3_r3": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_3_r4": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_3_r5": {
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_4_r1": {
                "material_fire_1": 0,
                "material_leaf_1": 100,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_4_r2": {
                "material_fire_1": 0,
                "material_leaf_1": 100,
                "material_clst_1": 0,
                "material_sand": 0
            },
            "challenge_4_r3": {
                "material_fire_1": 18,
                "material_leaf_1": 50,
                "material_clst_1": 13,
                "material_sand": 19
            },
            "challenge_4_r4": {
                "material_fire_1": 14,
                "material_leaf_1": 50,
                "material_clst_1": 21,
                "material_sand": 15
            },
            "challenge_4_r5": {
                "material_fire_1": 20,
                "material_leaf_1": 50,
                "material_clst_1": 17,
                "material_sand": 13
            },
            "challenge_5_r1": {
                "material_fire_1": 0,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 100
            },
            "challenge_5_r2": {
                "material_fire_1": 0,
                "material_leaf_1": 50,
                "material_clst_1": 0,
                "material_sand": 50
            },
            "challenge_5_r3": {
                "material_fire_1": 18,
                "material_leaf_1": 13,
                "material_clst_1": 19,
                "material_sand": 50
            },
            "challenge_5_r4": {
                "material_fire_1": 14,
                "material_leaf_1": 21,
                "material_clst_1": 15,
                "material_sand": 50
            },
            "challenge_5_r5": {
                "material_fire_1": 20,
                "material_leaf_1": 17,
                "material_clst_1": 13,
                "material_sand": 50
            },
            "challenge_6_r1": {
                "material_fire_1": 0,
                "material_leaf_1": 0,
                "material_clst_1": 50,
                "material_sand": 50
            },
            "challenge_6_r2": {
                "material_fire_1": 0,
                "material_leaf_1": 70,
                "material_clst_1": 30,
                "material_sand": 0
            },
            "challenge_6_r3": {
                "material_fire_1": 18,
                "material_leaf_1": 13,
                "material_clst_1": 50,
                "material_sand": 19
            },
            "challenge_6_r4": {
                "material_fire_1": 14,
                "material_leaf_1": 21,
                "material_clst_1": 50,
                "material_sand": 15
            },
            "challenge_6_r5": {
                "material_fire_1": 20,
                "material_leaf_1": 17,
                "material_clst_1": 50,
                "material_sand": 13
            },
            "challenge_7_r1": None,
            "challenge_7_r2": None,
            "challenge_7_r3": None,
            "challenge_7_r4": None,
            "challenge_7_r5": None,
            "challenge_7_r6": None,
            "challenge_7_r7": None,
            "challenge_7_r8": None,
            "challenge_7_r9": None,
            "challenge_7_r10": None,
            "challenge_7_r11": None,
            "challenge_7_r12": None,
            "challenge_7_r13": None,
            "challenge_7_r14": None,
            "challenge_7_r15": {
                "material_fire_1": 70,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_7_r16": None,
            "challenge_7_r17": None,
            "challenge_7_r18": None,
            "challenge_7_r19": {
                "material_fire_1": 10,
                "material_leaf_1": 70,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_7_r20": None,
            "challenge_7_r21": None,
            "challenge_7_r22": None,
            "challenge_7_r23": {
                "material_fire_1": 10,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 70
            },
            "challenge_7_r24": None,
            "challenge_7_r25": None,
            "challenge_7_r26": None,
            "challenge_7_r27": {
                "material_fire_1": 70,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_7_r28": None,
            "challenge_7_r29": None,
            "challenge_7_r30": None,
            "challenge_7_r31": {
                "material_fire_1": 10,
                "material_leaf_1": 70,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_7_r32": None,
            "challenge_7_r33": None,
            "challenge_7_r34": None,
            "challenge_7_r35": {
                "material_fire_1": 10,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 70
            },
            "challenge_7_r36": None,
            "challenge_7_r37": None,
            "challenge_7_r38": None,
            "challenge_7_r39": None,
            "challenge_7_r40": None,
            "challenge_8_r1": None,
            "challenge_8_r2": None,
            "challenge_8_r3": {
                "material_fire_1": 70,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_8_r4": None,
            "challenge_8_r5": None,
            "challenge_8_r6": {
                "material_fire_1": 10,
                "material_leaf_1": 70,
                "material_clst_1": 10,
                "material_sand": 10
            },
            "challenge_8_r7": None,
            "challenge_8_r8": None,
            "challenge_8_r9": {
                "material_fire_1": 10,
                "material_leaf_1": 10,
                "material_clst_1": 10,
                "material_sand": 70
            },
            "challenge_8_r10": None,
            "challenge_8_r11": None,
            "challenge_8_r12": {
                "material_fire_1": 10,
                "material_leaf_1": 10,
                "material_clst_1": 70,
                "material_sand": 10
            },
            "challenge_8_r13": None,
            "challenge_8_r14": None,
            "challenge_8_r15": None,
            "challenge_8_r16": None,
            "challenge_8_r17": None,
            "challenge_8_r18": None,
            "challenge_8_r19": None,
            "challenge_8_r20": None,
            "challenge_8_r21": None,
            "challenge_8_r22": None,
            "challenge_8_r23": None,
            "challenge_8_r24": None,
            "challenge_8_r25": None,
            "challenge_8_r26": None,
            "challenge_8_r27": None,
            "challenge_8_r28": None,
            "challenge_8_r29": None,
            "challenge_8_r30": None,
            "challenge_8_r31": None,
            "challenge_8_r32": None,
            "challenge_8_r33": None,
            "challenge_8_r34": None,
            "challenge_8_r35": None,
            "challenge_8_r36": None,
            "challenge_8_r37": None,
            "challenge_8_r38": None,
            "challenge_8_r39": None,
            "challenge_8_r40": None,
            "challenge_9_r1": {
                "material_fire_1": 50,
                "material_leaf_1": 17,
                "material_clst_1": 13,
                "material_sand": 20
            },
            "challenge_9_r2": {
                "material_fire_1": 50,
                "material_leaf_1": 20,
                "material_clst_1": 13,
                "material_sand": 17
            },
            "challenge_9_r3": {
                "material_fire_1": 30,
                "material_leaf_1": 40,
                "material_clst_1": 20,
                "material_sand": 10
            },
            "challenge_9_r4": {
                "material_fire_1": 30,
                "material_leaf_1": 15,
                "material_clst_1": 40,
                "material_sand": 15
            },
            "challenge_9_r5": {
                "material_fire_1": 30,
                "material_leaf_1": 10,
                "material_clst_1": 20,
                "material_sand": 40
            },
            "challenge_10_r1": {
                "material_fire_1": 25,
                "material_leaf_1": 25,
                "material_clst_1": 25,
                "material_sand": 25
            },
            "challenge_10_r2": None,
            "challenge_10_r3": None,
            "challenge_10_r4": {
                "material_fire_1": 50,
                "material_leaf_1": 20,
                "material_clst_1": 10,
                "material_sand": 20
            },
            "challenge_10_r5": None,
            "challenge_10_r6": None,
            "challenge_10_r7": {
                "material_fire_1": 20,
                "material_leaf_1": 50,
                "material_clst_1": 10,
                "material_sand": 20
            },
            "challenge_10_r8": None,
            "challenge_10_r9": None,
            "challenge_10_r10": {
                "material_fire_1": 20,
                "material_leaf_1": 20,
                "material_clst_1": 10,
                "material_sand": 50
            },
            "challenge_10_r11": None,
            "challenge_10_r12": None,
            "challenge_10_r13": None,
            "challenge_10_r14": None,
            "challenge_10_r15": None,
            "challenge_10_r16": None,
            "challenge_10_r17": None,
            "challenge_10_r18": None,
            "challenge_10_r19": None,
            "challenge_10_r20": None,
            "challenge_10_r21": None,
            "challenge_10_r22": None,
            "challenge_10_r23": None,
            "challenge_10_r24": None,
            "challenge_10_r25": None,
            "challenge_10_r26": None,
            "challenge_10_r27": None,
            "challenge_10_r28": None,
            "challenge_10_r29": None,
            "challenge_10_r30": None,
            "challenge_10_r31": None,
            "challenge_10_r32": None,
            "challenge_10_r33": None,
            "challenge_10_r34": None,
            "challenge_10_r35": None,
            "challenge_10_r36": None,
            "challenge_10_r37": None,
            "challenge_10_r38": None,
            "challenge_10_r39": None,
            "challenge_10_r40": None
        }
        # 初始卡片
        self.Initial_card = {
            "challenge_1": ["card_fire_2"],
            "challenge_3": ["card_fire_1", "card_fire_2"],
            "challenge_4": ["card_leaf_1", "card_leaf_2"],
            "challenge_5": ["card_clst_1", "card_clst_2"],
            "challenge_6": ["card_sand_1", "card_sand_1"],
            "challenge_7": None,
            "challenge_8": None,
            "challenge_9": None,
            "challenge_10": None,
        }
        # 卡片数据
        self.prepared_card_data = {
            "card_fire_1": {
                "1": {
                    "inputs": {
                        "material_fire_1": 1
                    },
                    "outputs": {
                        "material_fire_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_fire_1": 1
                    },
                    "outputs": {
                        "material_fire_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": True
                },
                "3": {
                    "inputs": {
                        "material_fire_1": 1
                    },
                    "outputs": {
                        "material_fire_2": 1
                    },
                    "multiplier": 2.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": True
                }
            },
            "card_fire_2": {
                "1": {
                    "inputs": {
                        "material_fire_2": 1
                    },
                    "outputs": {
                        "material_fire_3": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_fire_2": 1
                    },
                    "outputs": {
                        "material_fire_3": 1
                    },
                    "multiplier": 2.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_fire_2": 1
                    },
                    "outputs": {
                        "material_fire_3": 1
                    },
                    "multiplier": 2.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": True
                }
            },
            "card_fire_3": {
                "1": {
                    "inputs": {
                        "material_fire_3": 1
                    },
                    "outputs": {
                        "material_fire_4": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_fire_3": 1
                    },
                    "outputs": {
                        "material_fire_4": 1
                    },
                    "multiplier": 2.4,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_fire_3": 1
                    },
                    "outputs": {
                        "material_fire_4": 1
                    },
                    "multiplier": 2.4,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": True
                }
            },
            "card_fire_4": {
                "1": {
                    "inputs": {
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_fire_5": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_fire_5": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 1500,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_fire_5": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 5000,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_leaf_1": {
                "1": {
                    "inputs": {
                        "material_leaf_1": 10
                    },
                    "outputs": {
                        "material_leaf_2": 5,
                        "material_sand": 5
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_leaf_1": 10
                    },
                    "outputs": {
                        "material_leaf_2": 8,
                        "material_sand": 2
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_leaf_1": 1
                    },
                    "outputs": {
                        "material_leaf_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {
                        "material_sand": 1
                    },
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_leaf_2": {
                "1": {
                    "inputs": {
                        "material_leaf_2": 10
                    },
                    "outputs": {
                        "material_leaf_3": 4,
                        "material_sand": 6
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_leaf_2": 10
                    },
                    "outputs": {
                        "material_leaf_3": 6,
                        "material_sand": 4
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_leaf_2": 10
                    },
                    "outputs": {
                        "material_leaf_3": 8,
                        "material_sand": 2
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {
                        "material_sand": 1
                    },
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_leaf_3": {
                "1": {
                    "inputs": {
                        "material_leaf_3": 10
                    },
                    "outputs": {
                        "material_leaf_4": 3,
                        "material_sand": 7
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_leaf_3": 10
                    },
                    "outputs": {
                        "material_leaf_4": 5,
                        "material_sand": 5
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_leaf_3": 10
                    },
                    "outputs": {
                        "material_leaf_4": 7,
                        "material_sand": 3
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {
                        "material_sand": 1
                    },
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_clst_1": {
                "1": {
                    "inputs": {
                        "material_clst_1": 1,
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_clst_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_clst_1": 1,
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_clst_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_clst_1": 1,
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_clst_2": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {
                        "<color=#fce0ba>[<天空伊纳>": 5
                    },
                    "pre_exec": False
                }
            },
            "card_clst_2": {
                "1": {
                    "inputs": {
                        "material_clst_2": 1,
                        "material_leaf_2": 1
                    },
                    "outputs": {
                        "material_clst_3": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_clst_2": 1,
                        "material_leaf_2": 1
                    },
                    "outputs": {
                        "material_clst_3": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {
                        "<color=#fce0ba>[<天空伊纳>": 15
                    },
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_clst_2": 1,
                        "material_leaf_2": 1
                    },
                    "outputs": {
                        "material_clst_3": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {
                        "<color=#fce0ba>[<天空伊纳>": 15
                    },
                    "pre_exec": False
                }
            },
            "card_clst_3": {
                "1": {
                    "inputs": {
                        "material_clst_3": 1,
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_clst_4": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_clst_3": 1,
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_clst_4": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_clst_3": 1,
                        "material_fire_4": 1
                    },
                    "outputs": {
                        "material_clst_4": 1
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_sand_1": {
                "1": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 2
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 3
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 5
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_sand_2": {
                "1": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 3
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 5
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 8
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            },
            "card_sand_3": {
                "1": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 5
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "2": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 9
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                },
                "3": {
                    "inputs": {
                        "material_sand": 1
                    },
                    "outputs": {
                        "material_sand": 9
                    },
                    "multiplier": 1.0,
                    "extra_outputs": {},
                    "flat_score": 0,
                    "series_bonus": {},
                    "pre_exec": False
                }
            }
        }
        # 材料分数
        self.material_price = {
            "material_fire_1": 1,
            "material_fire_2": 2,
            "material_fire_3": 10,
            "material_fire_4": 35,
            "material_fire_5": 85,
            "material_clst_1": 1,
            "material_clst_2": 3,
            "material_clst_3": 22,
            "material_clst_4": 105,
            "material_leaf_1": 1,
            "material_leaf_2": 5,
            "material_leaf_3": 50,
            "material_leaf_4": 500,
            "material_sand": 1
        }
        # 初始材料
        self.material_list = {
            "challenge_1": [{
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            }],
            "challenge_3": [{
                "material_fire_1": 100,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 0
            }],
            "challenge_4": [{
                "material_fire_1": 0,
                "material_leaf_1": 100,
                "material_clst_1": 0,
                "material_sand": 0
            }],
            "challenge_5": [{
                "material_fire_1": 0,
                "material_leaf_1": 0,
                "material_clst_1": 0,
                "material_sand": 100
            }],
            "challenge_6": [{
                "material_fire_1": 0,
                "material_leaf_1": 0,
                "material_clst_1": 50,
                "material_sand": 50
            }],
            "challenge_7": [{
                
            }]
        }
        # 商店花费数据
        # 设计思路：刷新和购买独立一个self变量，刷新与购买时修改对应变量，nextround触发时清零，变量作为偏移从这个列表获取价格，超出最大范围取最后一位作为价格
        self.shop_data = {
            "fresh": [1,1,2,2,2,3,3,3,3,3,6,6,6,6,6,6,6,10],
            "buy": [2,3,4,4,4,5,5,5,5,10,10,10,10,10,16],
            "slot": [8,18,28,40]
        }
        # 加钱数据
        self.coin_data = {
            "challenge_1": [10,10],
            "challenge_3": [10,10,10,10,10],
            "challenge_4": [10,10,10,10,10],
            "challenge_5": [10,10,10,10,10],
            "challenge_6": [10,10,10,10,10],
            "challenge_7": [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10],
            "challenge_8": [10,10,10,10,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
            "challenge_9": [30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
            "challenge_10": [30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
        }
        # 卡牌组数据
        self.card_data = {
            "fire": ["card_fire_1","card_fire_2","card_fire_3","card_fire_4","card_fire_5"],
            "leaf": ["card_leaf_1","card_leaf_2","card_leaf_3","card_leaf_4"],
            "clst": ["card_clst_1","card_clst_2","card_clst_3","card_clst_4"],
            "sand": ["card_sand_1","card_sand_2","card_sand_3","card_sand_4"]
        }

    def _random_card(self, carving_data):
        max_lv_card = []
        # 获取满级卡信息
        card_info = carving_data["card"]
        for card, lv in card_info.items():
            if card_info[card] == 3:
                max_lv_card.append(card)

        # 随机选卡
        def pick_random(max_lv_card1, pool_name=None, count=3):
            if pool_name is None:
                return [None] * count
            if pool_name == "all":
                card_data = (
                    self.card_data["fire"] +
                    self.card_data["leaf"] +
                    self.card_data["clst"] +
                    self.card_data["sand"]
                )
            else:
                card_data = self.card_data[pool_name]
            random_list = list(set(card_data) - set(max_lv_card1))
            random.shuffle(random_list)
            return random_list[:count]

        # 映射表：关卡ID -> 池子名
        challenge_map = {
            "challenge_3": "fire",
            "challenge_4": "leaf",
            "challenge_5": "clst",
            "challenge_6": "sand",
            "challenge_7": "all",
            "challenge_9": "all",
            "challenge_10": "all",
            "challenge_8": None,
        }

        cid = carving_data["id"]

        if cid == "challenge_1":
            good = [{"id": "card_fire_3", "price": 0}, None, None]
        elif cid in challenge_map:
            good = pick_random(max_lv_card, challenge_map[cid])
        else:
            good = [None, None, None]

        return good

    def act35sideCreate(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        challenge_id = json_body["challengeId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]
        activity_data["carving"] = {}

        material = {
            "material_fire_1": 0,
            "material_leaf_1": 0,
            "material_clst_1": 0,
            "material_sand": 0
        }
        if self.round_data_map[challenge_id + "_r1"] is None:
            keys = list(material.keys())
            n = len(keys)

            total = 100
            max_diff = 25
            
            # 计算每个值的最小和最大可能范围
            # 平均值
            avg = total / n
            
            # 确定每个值的范围，确保差值不超过max_diff
            min_val = max(0, avg - max_diff/2)
            max_val = min(total, avg + max_diff/2)
            
            # 生成第一个随机值
            values = [random.randint(int(min_val), int(max_val))]
            
            # 生成后续值，考虑已分配的值和剩余的总和
            remaining = total - values[0]
            for i in range(1, n-1):
                # 计算当前值可能的范围
                remaining_avg = remaining / (n - i)
                current_min = max(0, remaining_avg - max_diff/2, remaining - max_val*(n-i-1))
                current_max = min(remaining, remaining_avg + max_diff/2, remaining - min_val*(n-i-1))
                
                # 确保范围有效
                current_min = max(min_val, current_min)
                current_max = min(max_val, current_max)
                
                # 生成随机值
                if current_min <= current_max:
                    value = random.randint(int(current_min), int(current_max))
                else:
                    value = int(remaining_avg)  # 如果范围无效，使用平均值
                
                values.append(value)
                remaining -= value
            
            # 添加最后一个值
            values.append(remaining)
            
            # 打乱顺序
            random.shuffle(values)
            
            # 分配值到材料
            for i, key in enumerate(keys):
                material[key] = values[i]

        else:
            material = self.round_data_map[challenge_id + "_r1"]


        # 特殊关卡卡牌处理
        match challenge_id:
            case "challenge_1":
                card = {
                    "card_fire_1": 1
                }
                free_cnt = 1
            case "challenge_8":
                card = {
                    "card_fire_1": 3,
                    "card_fire_2": 3,
                    "card_fire_3": 3,
                    "card_fire_4": 3,
                    "card_leaf_1": 3,
                    "card_leaf_2": 3,
                    "card_leaf_3": 3,
                    "card_clst_1": 3,
                    "card_clst_2": 3,
                    "card_clst_3": 3,
                    "card_sand_1": 3,
                    "card_sand_2": 3,
                    "card_sand_3": 3
                }
                free_cnt = 0
            case _:
                card = {}
                free_cnt = 2
        
        good = []
        if self.Initial_card[challenge_id] is not None:
            for card_id in self.Initial_card[challenge_id]:
                good.append({
                    "id": card_id,
                    "price": 0
                })
            if len(good) < 3:
                good += [None] * (3 - len(good))
        else:
            good = [None, None, None]
        shop = {
            "coin": 0,
            "good": good,
            "freeCardCnt": free_cnt,
            "refreshPrice":99,
            "slotPrice": 8
        }

        carving_data = {
            "id": challenge_id,
            "round": 1,
            "roundCoinAdd": -1,
            "score": 0,
            "state": 5,
            "material": material,
            "card": card,
            "slotCnt": 2,
            "shop": shop,
            "mission": None
        }
        activity_data["carving"] = carving_data

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": carving_data
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result

    def act35sidesettle(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]

        challenge_id = carving_data["id"]
        score = carving_data["score"]
        round_num = carving_data["round"]
        # 清空数据
        user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"] = None

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": None
                            }
                        }
                    }
                }
            },
            "challengeId": challenge_id,
            "score": score,
            "oldRound": 0,
            "newRound": round_num,
            "pointStage": 0,
            "pointRound": 0,
            "pointBefore": 0,
            "pointAfter": 0
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    def act35sideToBuy(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]
        
        # 商店卡牌刷新
        good_list = self._random_card(carving_data)
        good = []
        if carving_data["shop"]["freeCardCnt"] > 0:
            for card_id in good_list:
                if card_id is None:
                    good.append(None)
                else:
                    good.append({
                        "id": card_id,
                        "price": 0
                    })
            if len(good) < 3:
                good += [None] * (3 - len(good))
        else:
            for card_id in good_list:
                if card_id is None:
                    good.append(None)
                else:
                    good.append({
                        "id": card_id,
                        "price": 2
                    })
            if len(good) < 3:
                good += [None] * (3 - len(good))

        carving_data["shop"]["good"] = good
        carving_data["shop"]["coin"] = 0


        # 操作台槽位
        if carving_data["slotCnt"] < 8:
            carving_data["shop"]["slotPrice"] = self.shop_data["slot"][carving_data["slotCnt"] - 2]


        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "shop": carving_data["shop"],
                                    "state": 1
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    def act35siderefreshShop(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]
        good_list = self._random_card(carving_data)
        good = []
        if carving_data["shop"]["freeCardCnt"] > 0:
            for card_id in good_list:
                good.append({
                    "id": card_id,
                    "price": 0
                })
            if len(good) < 3:
                good += [None] * (3 - len(good))
        else:
            for card_id in good_list:
                good.append({
                    "id": card_id,
                    "price": 2
                })
            if len(good) < 3:
                good += [None] * (3 - len(good))
        
        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            "carving": {
                                "shop": carving_data["shop"],
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        return result
    
    def act35sidebuySlot(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]

        carving_data["slotCnt"] += 1
        carving_data["shop"]["coin"] -= 8
        carving_data["shop"]["slotPrice"] = -1

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "shop": carving_data["shop"],
                                    "slotCnt": carving_data["slotCnt"]
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result

    def act35sidebuyCard(self):
        json_body = request.get_json()
        # {'activityId': 'act35sre', 'slot': 0}
        activity_id = json_body["activityId"]
        slot = json_body["slot"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]

        # 获取要购买的卡片ID
        card_id = carving_data["shop"]["good"][slot]["id"]
        
        # 更新卡片数量
        if card_id in carving_data["card"]:
            carving_data["card"][card_id] += 1
        else:
            carving_data["card"][card_id] = 1
        
        # 更新商店状态
        if carving_data["shop"]["freeCardCnt"] > 0:
            carving_data["shop"]["freeCardCnt"] -= 1  # 减少免费卡次数
        carving_data["shop"]["coin"] -= carving_data["shop"]["good"][slot]["price"]
        carving_data["shop"]["good"][slot] = None
        # 免费次数为0时，开始收费
        if carving_data["shop"]["freeCardCnt"] <= 0:
            for good in carving_data["shop"]["good"]:
                if good is not None:
                    if good["price"] == 0:
                        # 初始价格
                        good["price"] = 3
                    else:
                        good["price"] += 1

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "shop": {
                                        "coin": 10,
                                        "freeCardCnt": carving_data["shop"]["freeCardCnt"],
                                        "good": carving_data["shop"]["good"]
                                    },
                                    "card": carving_data["card"]
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "pushMessage": []
        }
        
        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    def act35sidetoProcess(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]
        carving_data["state"] = 2

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "state": carving_data["state"]
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result

    def act35sideprocess(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        cards = json_body["cards"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]

        card_info = carving_data["card"]
        materials = carving_data["material"]
        slot_cnt = carving_data["slotCnt"]
        empty_slots = slot_cnt - len(cards)

        card_data_map = self.prepared_card_data
        material_data_map = self.material_price

        frames = []

        # 上一回合总分
        base_score = carving_data["score"]
        total_score = base_score

        # 非工艺区生效卡处理
        pre_exec_cards = []
        for card, lv in card_info.items():
            lv = str(lv)
            if card in card_data_map and card_data_map[card][lv]["pre_exec"]:
                if card not in cards:
                    pre_exec_cards.append(card)

        ordered_cards = pre_exec_cards + cards

        # 遍历卡列表
        for card in ordered_cards:
            lv = str(card_info[card])
            card_cfg = card_data_map[card][lv]
            if not card_cfg:
                continue

            inputs = card_cfg["inputs"]
            outputs = card_cfg["outputs"]
            multiplier = card_cfg["multiplier"]
            extra_outputs = card_cfg["extra_outputs"]
            flat_score = card_cfg["flat_score"]
            series_bonus = card_cfg["series_bonus"]

            product = {}
            # 如果材料足够，则循环合成
            while all(materials.get(mat, 0) >= need for mat, need in inputs.items()):
                # 扣输入
                for mat, need in inputs.items():
                    materials[mat] -= need

                # 正常产出
                for mat, out in outputs.items():
                    amount = int(out * multiplier)
                    materials[mat] = materials.get(mat, 0) + amount
                    product[mat] = product.get(mat, 0) + amount

                # 额外产出
                for mat, out in extra_outputs.items():
                    materials[mat] = materials.get(mat, 0) + out
                    product[mat] = product.get(mat, 0) + out

            # 计算当前库存的估值
            step_score = 0
            for mat, num in materials.items():
                base_val = material_data_map.get(mat, 0)
                for prefix, bonus in series_bonus.items():
                    if mat.startswith(prefix):
                        base_val += bonus
                        break
                step_score += base_val * num

            # 空槽位加分
            step_score += empty_slots * flat_score

            # 基础分 + 当前估值
            total_score = base_score + step_score

            frames.append({
                "card": card,
                "product": product,
                "score": total_score,  
                "type": 0
            })

        # 更新 carving_data 的 总分
        carving_data["score"] = total_score

        # 加钱
        coin = self.coin_data[carving_data["id"]][carving_data["round"] - 1]
        carving_data["shop"]["coin"] += coin
        carving_data["roundCoinAdd"] += coin

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "score": frames[-1]["score"],
                                    "shop": carving_data["shop"],
                                    "roundCoinAdd": carving_data["roundCoinAdd"],
                                    "state": 3
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "frames": frames
        }
        print(frames)
        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    def act35nextRound(self):
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = dict(user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"])
        challenge_id = carving_data["id"]
        
        # 回合计数
        carving_data["round"] += 1

        # 下回合初始材料
        material = {
            "material_fire_1": 0,
            "material_leaf_1": 0,
            "material_clst_1": 0,
            "material_sand": 0
        }
        if self.round_data_map[challenge_id + "_r" + str(carving_data["round"])] is None:
            keys = list(material.keys())
            n = len(keys)

            total = 100
            max_diff = 25
            
            # 计算每个值的最小和最大可能范围
            # 平均值
            avg = total / n
            
            # 确定每个值的范围，确保差值不超过max_diff
            min_val = max(0, avg - max_diff/2)
            max_val = min(total, avg + max_diff/2)
            
            # 生成第一个随机值
            values = [random.randint(int(min_val), int(max_val))]
            
            # 生成后续值，考虑已分配的值和剩余的总和
            remaining = total - values[0]
            for i in range(1, n-1):
                # 计算当前值可能的范围
                remaining_avg = remaining / (n - i)
                current_min = max(0, remaining_avg - max_diff/2, remaining - max_val*(n-i-1))
                current_max = min(remaining, remaining_avg + max_diff/2, remaining - min_val*(n-i-1))
                
                # 确保范围有效
                current_min = max(min_val, current_min)
                current_max = min(max_val, current_max)
                
                # 生成随机值
                if current_min <= current_max:
                    value = random.randint(int(current_min), int(current_max))
                else:
                    value = int(remaining_avg)  # 如果范围无效，使用平均值
                
                values.append(value)
                remaining -= value
            
            # 添加最后一个值
            values.append(remaining)
            
            # 打乱顺序
            random.shuffle(values)
            
            # 分配值到材料
            for i, key in enumerate(keys):
                material[key] = values[i]
        else:
            material = self.round_data_map[challenge_id + "_r" + str(carving_data["round"])]

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "TYPE_ACT35SIDE": {
                            activity_id: {
                                "carving": {
                                    "round": carving_data["round"],
                                    "state": 1,
                                    "material": material,
                                    "shop": carving_data["shop"]
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
 
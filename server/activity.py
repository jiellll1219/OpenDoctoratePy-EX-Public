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
        self.round_data_map = {}
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

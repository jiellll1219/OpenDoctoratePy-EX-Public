from flask import request, jsonify
from virtualtime import time
from utils import read_json, write_json, run_after_response
from constants import (
    SYNC_DATA_TEMPLATE_PATH
)
import random

class CheckInReward():
    # 这个类用于处理签到奖励

    def getCheckInReward():
        json_body = request.get_json()
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        access_id = json_body["activityId"]

        items = []
        modified = {}

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

    def getActivityCheckInReward():

        json_body = request.get_json()
        
        items = []

        activity_id = json_body["activityId"]
        target_index = json_body["index"]
        dyn_opt = json_body["dynOpt"]
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_data = user_data["user"]["activity"]["CHECKIN_ONLY"][activity_id]

        activity_data["history"][target_index] = 0
        activity_data["dynOpt"].append(dyn_opt)

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
            },
            "items": items
        }

        run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)

        return result
    
    def _act53sign():
        pass
    
    def getReward():

        json_body = request.get_json()

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_id = json_body["activityId"]
        items = []

        match activity_id:
            case activity_id if activity_id.endswith("pray"):
                activity_type = "PRAY_ONLY"
                activity_data = user_data["user"]["activity"][activity_type][activity_id]

                activity_data["lastTs"] = time()
                activity_data["praying"] = True

                count_list = [200,300, 400, 500, 600, 700, 800]
                random.shuffle(count_list)
                count_1 = random.choice(count_list)
                random.shuffle(count_list)
                count_2 = random.choice(count_list)
                if count_1 >= count_2:
                    activity_data["prayMaxIndex"] = json_body["prayArray"][0]
                    count = count_1
                else:
                    activity_data["prayMaxIndex"] = json_body["prayArray"][1]
                    count = count_2

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
                items.append({
                    "type": "DIAMOND_SHD",
                    "id": "4003",
                    "count": count
                })

            case activity_id if activity_id.endswith("login"):
                activity_type = "LOGIN_ONLY"
                activity_data = user_data["user"]["activity"][activity_type][activity_id]
                activity_data["reward"] = 0

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        activity_type: {
                            activity_id: activity_data
                        }
                    }
                },
                "deleted": {}
            },
            "items": items
        }
        print(result)
        return result

    def sign():
        json_body = request.get_json()
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        # {'actId': 'act3signvs', 'tasteChoice': 2} 咸粽子
        # {'actId': 'act3signvs', 'tasteChoice': 1} 甜粽子
        # "act3signvs": {
        #             "sweetVote": 0,
        #             "saltyVote": 0,
        #             "canVote": 1,
        #             "todayVoteState": 0,
        #             "voteRewardState": 0,
        #             "signedCnt": 0,
        #             "availSignCnt": 1,
        #             "socialState": 2,
        #             "actDay": 1
        #         }
        act_id = json_body["actId"]
        act_data = user_data["user"]["activity"]["CHECKIN_VS"][act_id]

        act_data["signedCnt"] += 1
        act_data["canVote"] = 0
        if json_body["tasteChoice"] == 1:
            act_data["sweetVote"] += 1
        else:
            act_data["saltyVote"] += 1

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

    from data.act_data import round_data_map, Initial_card, prepared_card_data, material_price, material_list, shop_data, coin_data, card_data

    def _build_prepared_card_data() -> dict:

        data = {}

        def make_simple(inp: str, out: str, mults: list[float]) -> dict:
            """单输入单输出卡牌"""
            return {
                str(i + 1): {"inputs": {inp: 1}, "outputs": {out: 1}, "multiplier": mult}
                for i, mult in enumerate(mults)
            }

        def make_simple2(inputs: dict, outputs: dict) -> dict:
            """多输入多输出卡牌（所有等级相同）"""
            return {
                str(i): {"inputs": dict(inputs), "outputs": dict(outputs), "multiplier": 1.0}
                for i in range(1, 4)
            }
        data.update({
            "card_fire_1": make_simple("material_fire_1", "material_fire_2", [1.0, 1.0, 2.0]),
            "card_fire_2": make_simple("material_fire_2", "material_fire_3", [1.0, 2.0, 2.0]),
            "card_fire_3": make_simple("material_fire_3", "material_fire_4", [1.0, 2.4, 2.4]),
            "card_fire_4": make_simple("material_fire_4", "material_fire_5", [1.0, 1.0, 1.0]),
        })

        data["card_leaf_1"] = {
            "1": {"inputs": {"material_leaf_1": 10}, "outputs": {"material_leaf_2": 5, "material_sand": 5}, "multiplier": 1.0},
            "2": {"inputs": {"material_leaf_1": 10}, "outputs": {"material_leaf_2": 8, "material_sand": 2}, "multiplier": 1.0},
            "3": {"inputs": {"material_leaf_1": 1},  "outputs": {"material_leaf_2": 1}, "multiplier": 1.0},
        }

        leaf_rules = {
            "card_leaf_2": [(4, 6), (6, 4), (8, 2)],
            "card_leaf_3": [(3, 7), (5, 5), (7, 3)],
        }

        for card_name, ratios in leaf_rules.items():
            n = int(card_name.split("_")[-1])
            data[card_name] = {
                str(i + 1): {
                    "inputs": {f"material_leaf_{n}": 10},
                    "outputs": {f"material_leaf_{n+1}": a, "material_sand": b},
                    "multiplier": 1.0,
                }
                for i, (a, b) in enumerate(ratios)
            }

        data.update({
            "card_clst_1": make_simple2({"material_clst_1": 1, "material_sand": 1}, {"material_clst_2": 1}),
            "card_clst_2": make_simple2({"material_clst_2": 1, "material_leaf_2": 1}, {"material_clst_3": 1}),
            "card_clst_3": make_simple2({"material_clst_3": 1, "material_fire_4": 1}, {"material_clst_4": 1}),
        })

        data.update({
            "card_sand_1": make_simple("material_sand", "material_sand", [2, 3, 5]),
            "card_sand_2": make_simple("material_sand", "material_sand", [3, 5, 8]),
            "card_sand_3": make_simple("material_sand", "material_sand", [5, 9, 9]),
        })

        return data
    
    def _random_card(carving_data):
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
                    act35side.card_data["fire"] +
                    act35side.card_data["leaf"] +
                    act35side.card_data["clst"] +
                    act35side.card_data["sand"]
                )
            else:
                card_data = act35side.card_data[pool_name]
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

    def act35sideCreate():
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
        if act35side.round_data_map[challenge_id + "_r1"] is None:
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
            material = act35side.round_data_map[challenge_id + "_r1"]


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
        if act35side.Initial_card[challenge_id] is not None:
            for card_id in act35side.Initial_card[challenge_id]:
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

    def act35sidesettle():
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
    
    def act35sideToBuy():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]
        
        # 商店卡牌刷新
        good_list = act35side._random_card(carving_data)
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

        result = {
            
        }
        carving_data["shop"]["good"] = good

        # 操作台槽位
        if carving_data["slotCnt"] < 8:
            carving_data["shop"]["slotPrice"] = act35side.shop_data["slot"][carving_data["slotCnt"] - 2]


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
    
    def act35siderefreshShop():
        json_body = request.get_json()
        activity_id = json_body["activityId"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]
        good_list = act35side._random_card(carving_data)
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
    
    def act35sidebuySlot():
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

    def act35sidebuyCard():
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
    
    def act35sidetoProcess():
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

    def act35sideprocess_old():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        cards = json_body["cards"]

        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"]

        card_info = carving_data["card"]
        materials = carving_data["material"]
        slot_cnt = carving_data["slotCnt"]
        empty_slots = slot_cnt - len(cards)

        card_data_map = act35side.prepared_card_data
        material_data_map = act35side.material_price

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
        coin = act35side.coin_data[carving_data["id"]][carving_data["round"] - 1]
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

        # run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result
    
    def act35sideprocess():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        cards:list[str] = json_body["cards"]

        # 读取数据
        card_data_map = act35side.prepared_card_data
        material_data_map = act35side.material_price
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        carving_data = dict(user_data["user"]["activity"]["TYPE_ACT35SIDE"][activity_id]["carving"])

        card_info:dict[str, int] = carving_data["card"]
        materials:dict[str, int] = carving_data["material"]
        slot_cnt:int = carving_data["slotCnt"]
        empty_slots = slot_cnt - len(cards)# 空槽位数量

        frames = []# 帧记录列表
        base_score = carving_data["score"]# 当前分数
        total_score = base_score

        # 用于宝石合成的闭包函数
        def score_calculation(card: str):
            card_lv = str(card_info[card])  # 卡牌等级
            card_cfg = card_data_map[card][card_lv]  # 卡牌信息
            inputs: dict[str, int] = card_cfg["inputs"]  # 输入材料
            outputs: dict[str, int] = card_cfg["outputs"]  # 输出材料
            multiplier: float = card_cfg["multiplier"]  # 合成倍率

            syn_times: int = float('inf')  # 初始化为无穷大，找出所有输入能支持的最小合成次数
            for mat, need in inputs.items():
                count: int = materials.get(mat, 0)
                if need <= 0:
                    continue
                syn_times = min(syn_times, count // need)

            # syn_times转整数
            if syn_times == float('inf'):
                syn_times = 0
            else:
                syn_times = int(syn_times)

            # 消耗材料
            for mat, need in inputs.items():
                count: int = materials.get(mat, 0)
                materials[mat] = count - need * syn_times

            product: dict[str, int] = {}

            # 产出材料
            for mat, out in outputs.items():
                gain = int(out * multiplier * syn_times)
                materials[mat] = materials.get(mat, 0) + gain
                product[mat] = gain

            result = {
                "syn_times": syn_times,
                "product": product
            }

            return result

        # —— 淬雕I/II/III 合成
        fire_card = {"card_fire_1", "card_fire_2", "card_fire_3"}
        syn_card = {}
        for card in fire_card:
            # 卡牌等级检查
            card_lv:int = card_info.get(card, 0)
            if card_lv <= 1:
                continue
            # 合成
            product = score_calculation(card)
            # 算分
            step_score = 0
            for mat, num in materials.items():
                base_val = material_data_map[mat]
                step_score += base_val * num
            total_score += step_score

            frames.append({
                "card": card,
                "product": product,
                "score": total_score,  
                "type": 0
            })

            syn_card.add(card)

        cards = [item for item in cards if item not in syn_card]

        # —— 常规合成
        for card in cards:# 遍历cards列表，根据卡牌顺序进行合成
            card_lv: int = card_info[card]

            # 交糅I/II/III 均分材料
            if card.startswith("card_clst"):
                match card:
                    case "card_clst_1":
                        if card_lv > 1:
                            sum_cnt = materials.get("material_sand", 0) + materials.get("material_clst_1", 0)
                            count_half = int(sum_cnt / 2)
                            materials["material_sand"] = count_half
                            materials["material_clst_1"] = count_half
                    case "card_clst_2":
                        if card_lv == 3:
                            sum_cnt = materials.get("material_leaf_2", 0) + materials.get("material_clst_2", 0)
                            count_half = int(sum_cnt / 2)
                            materials["material_leaf_2"] = count_half
                            materials["material_clst_2"] = count_half
                    case "card_clst_3":
                        if card_lv > 1:
                            sum_cnt = materials.get("material_fire_4", 0) + materials.get("material_clst_3", 0)
                            count_half = int(sum_cnt / 2)
                            materials["material_fire_4"] = count_half
                            materials["material_clst_3"] = count_half

            # 合成
            syn_info = score_calculation(card)
            syn_times:int = syn_info["syn_times"]
            product:dict[str, int] = syn_info["product"]

            # —— 算分
            step_score:int = 0
            extra_score:int = 0
            # 卡牌等级效果处理
            match card:
                # —— 淬雕 IV 空槽位加分
                case "card_fire_4":
                    if card_lv > 1:
                        step_score += empty_slots * (1500 if card_lv == 2 else 5000)

                # —— 滤纯I/II/III 三级额外产出沙伊纳
                case "card_leaf_1" | "card_leaf_2" | "card_leaf_3":
                    if card_lv == 3:
                        count:int = syn_times
                        product["material_sand"] = count

                # —— 交糅I/II/III 三级额外加分
                case "card_clst_1" | "card_clst_2" | "card_clst_3":
                    match card:
                        case "card_clst_1":
                            if card_lv == 3:
                                extra_score += 5
                        case "card_clst_2":
                            if card_lv > 1:
                                extra_score += 15
                        case "card_clst_3":
                            if card_lv == 3:
                                step_score += syn_times * 100

                case _:
                    pass
                
            # 当前全部材料的总分
            for mat, num in materials.items():
                base_val = material_data_map.get(mat, 0)
                # 天空伊纳系列宝石额外加分
                if mat.startswith("card_clst"):
                    base_val += extra_score
                step_score += base_val * num
            total_score += step_score

            frames.append({
                "card": card,
                "product": product,
                "score": total_score,  
                "type": 0
            })

        # 更新 carving_data 的 总分
        carving_data["score"] = total_score

        # 加钱
        coin = act35side.coin_data[carving_data["id"]][carving_data["round"] - 1]
        carving_data["shop"]["coin"] += coin
        carving_data["roundCoinAdd"] += coin

        carving_data["state"] = 3

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
            },
            "frames": frames
        }

        # run_after_response(write_json, user_data, SYNC_DATA_TEMPLATE_PATH)
        return result


    def act35nextRound():
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
        if act35side.round_data_map[challenge_id + "_r" + str(carving_data["round"])] is None:
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
            material = act35side.round_data_map[challenge_id + "_r" + str(carving_data["round"])]

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


class vhalfidle:
    from data.level import evolve_0, evolve_1, evolve_2
    from data.act_data import spec_char, vhalfidle_pools

    def refreshProduct():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        production = act_info["production"]

        now_ts = time()
        last_ts = production["harvestTs"]
        diff_mult = (now_ts - last_ts) / 3600
        production["refreshTs"] = now_ts

        for key, value in production["rate"].items():
            cnt = int(value * diff_mult)
            production["product"].update({key: cnt})

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "production": production
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def harvest():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        production = act_info["production"]

        keys_to_remove = []
        items = []
        milestoneAdd = 0

        for key, value in production["product"].items():
            if key == "act1vhalfidle_token_point":
                milestoneAdd = production["product"][key]
                items.append({
                    "itemId": key,
                    "count": production["product"][key]
                })
            cnt = int(value + act_info["inventory"].get(key, 0))
            act_info["inventory"].update({key: cnt})
            items.append({
                "itemId": key,
                "count": production["product"][key]
            })
            keys_to_remove.append(key)

        production["product"] = {}

        production["harvestTs"] = time()
        production["refreshTs"] = time()

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "inventory": act_info["inventory"],
                                "production": production
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "milestoneAdd": milestoneAdd,
            "items": items
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def unlockTech():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        # {'activityId': 'act1vhalfidle', 'techId': 'node_1_2'}
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        tech_list = act_info["tech"]["unlock"]

        tech_list.append(json_body["techId"])

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "tech": {
                                    "unlock": tech_list
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result


    def recruitNormal():
        json_body = request.get_json()
        activity_id = json_body["activityId"]
        pool_id = json_body["poolId"]
        count = json_body["count"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        troop_chars = sync_data["user"]["troop"]["chars"]
        act_chars = act_info["troop"]["char"]
        poolTimes = act_info["recruit"]["poolTimes"]

        vhalfidle_pools = vhalfidle.vhalfidle_pools
        spec_char = vhalfidle.spec_char

        # 资源检查
        if act_info["inventory"]["gacha_normal"] >= count * 20:
            act_info["inventory"]["gacha_normal"] -= count * 20
        else:
            return jsonify({"result": 1, "errMsg": "封装矿核不足"}), 404

        # 初始数据定义
        newChar = []
        oldChar = []
        have_chars = set()

        # 获取已有角色ID集合
        for key, value in act_chars.items():
            have_chars.add(act_chars[key]["charId"])

        # 卡池逻辑
        if pool_id in [f"gachaPac{i}" for i in range(1, 7)]:
            # 定向卡池：一次性获取该卡池的所有角色
            pool_set = vhalfidle_pools.get(pool_id, set()).copy()

            for char_id in pool_set:
                if char_id not in have_chars:
                    newChar.append(char_id)
                    vhalfidle._add_char_to_activity(act_info, sync_data, char_id)
                    have_chars.add(char_id)
                else:
                    oldChar.append(char_id)

        elif pool_id == "normalGachaPool":
            # 普通卡池：随机抽取
            # 获取可选角色id
            char_id_list = set()
            for key, value in troop_chars.items():
                char_id_list.add(troop_chars[key]["charId"])
            # 使用差集运算删除特殊干员，再转list
            filtered_char_list = [key for key in char_id_list if key not in spec_char]

            # 随机选择指定数量的角色id
            random_char = random.choices(filtered_char_list, k=count)

            # 添加角色
            for char_id in random_char:
                if char_id not in have_chars:
                    newChar.append(char_id)
                    vhalfidle._add_char_to_activity(act_info, sync_data, char_id)
                    have_chars.add(char_id)
                else:
                    oldChar.append(char_id)

            poolTimes["normalGachaPool"] += json_body["count"]

        elif pool_id == "newPlayerGachaPool":
            # 专项任命卡池：随机抽取
            pool_set = vhalfidle_pools.get(pool_id, set())
            char_data = list(pool_set) if pool_set else []

            for _ in range(count):
                if char_data:
                    selected_char = random.choice(char_data)
                    if selected_char not in have_chars:
                        newChar.append(selected_char)
                        vhalfidle._add_char_to_activity(act_info, sync_data, selected_char)
                        have_chars.add(selected_char)
                    else:
                        oldChar.append(selected_char)
                else:
                    return jsonify({"result": 1, "errMsg": "专项任命卡池为空"}), 404

            poolTimes["newPlayerGachaPool"] = poolTimes.get("newPlayerGachaPool", 0) + count

        ticketCount = len(oldChar)

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": {
                                    "char": act_chars
                                },
                                "recruit": {
                                    "poolTimes": poolTimes
                                },
                                "inventory": act_info["inventory"]
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "pushMessage": [],
            "newChar": newChar,
            "oldChar": oldChar,
            "ticketCount": ticketCount
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def recruitDirect():
        json_body = request.get_json()

        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_id = json_body["activityId"]
        char_id = json_body["charId"]

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        act_chars = act_info["troop"]["char"]
        poolTimes = act_info["recruit"]["poolTimes"]

        if act_info["inventory"]["gacha_direct"] >= 100:
            act_info["inventory"]["gacha_direct"] -= 100
        else:
            return jsonify({"result": 1, "errMsg": "特约邀请函不足"}), 404

        newChar = []
        newChar.append(char_id)


        vhalfidle._add_char_to_activity(act_info, sync_data, char_id)

        poolTimes["directionGachaPool"] += 1

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": {
                                    "char": act_chars
                                },
                                "recruit": {
                                    "poolTimes": poolTimes
                                },
                                "inventory": act_info["inventory"]
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "charId": char_id
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def vhalfidlebattleStart():
        json_body = request.get_json()

        global stage_id
        stage_id = json_body["stageId"]

        result = {
            "apFailReturn": 0,
            "battleId": "abcdefgh-1234-5678-a1b2c3d4e5f6",
            "inApProtectPeriod": False,
            "isApProtect": 0,
            "notifyPowerScoreNotEnoughIfFailed": False,
            "playerDataDelta": {"modified": {}, "deleted": {}},
            "result": 0,
        }

        return result

    def vhalfidlebattleFinish():
        json_body = request.get_json()

        activity_id = json_body["activityId"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]

        global stage_id

        halfidle_data = json_body.get("halfidleData", {})
        bossState = halfidle_data["bossState"]
        battleProcess = halfidle_data["battleProcess"]
        resourceNumDict = halfidle_data["resourceNumDict"]
        global settle_info
        # 构造 settleInfo 数据
        settle_info = {
            "stageId": stage_id,
            "rate": resourceNumDict,
            "bossState": bossState,
            "progress": battleProcess
        }
        act_info["settleInfo"] = settle_info

        if act_info["stage"][stage_id]["rate"] is None:
            act_info["stage"][stage_id]["rate"] = {}
            for key, value in json_body["halfidleData"]["resourceNumDict"].items():
                if value > 0:
                    act_info["stage"][stage_id]["rate"].update({key: value})

        # 更新BOSS击杀状态
        bossState = max(json_body["halfidleData"]["bossState"], act_info["stage"][stage_id]["bossState"])
        act_info["stage"][stage_id]["bossState"] = bossState

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "stage": {
                                    stage_id: act_info["stage"][stage_id]
                                },
                                "settleInfo": settle_info
                            }
                        }
                    }
                },
                "deleted": {}
            },
            "pushMessage": [],
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
            "unlockStages": [],
            "pryResult": [],
            "alert": [],
            "suggestFriend": False,
            "extra": {},
            "charLvUp": [],
            "bossState": bossState,
            "progress": 2,
            "milestoneAdd": 0,
            "items": []
        }
        # 将 settle_info 也存入 session

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def upgradeChar():
        json_body = request.get_json()
        cahr_id = json_body["charId"]
        dest_level = json_body["destLvl"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_id = json_body["activityId"]

        cost = 0

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        act_chars = act_info["troop"]["char"]

        for key, value in act_chars.items():
            if value["charId"] == cahr_id:
                char_info = value
                cahr_str_id = key
                break

        level_list_map = {
            0: vhalfidle.evolve_0,
            1: vhalfidle.evolve_1,
            2: vhalfidle.evolve_2
        }

        level_list = level_list_map[char_info["evolvePhase"]]
        discount = char_info["evolvePhase"] < 2

        # 计算升级所需总成本
        now_level = char_info["level"]
        cost = sum(level_list[lv] for lv in range(now_level + 1, dest_level))

        # 应用折扣并扣除经验
        char_info["level"] = dest_level
        discount_rate = 0.9 if discount else 1.0
        act_info["inventory"]["level_exp"] -= int(cost * discount_rate)

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": {
                                    "char": {
                                        cahr_str_id: char_info
                                    }
                                },
                                "inventory": {
                                    "level_exp": act_info["inventory"]["level_exp"]
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def upgradeSkill():
        json_body = request.get_json()
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        activity_id = json_body["activityId"]

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        act_chars = act_info["troop"]["char"]

        for key, value in act_chars.items():
            if value["charId"] == json_body["charId"]:
                value["skillLvl"] = json_body["destLvl"]
                act_chars[key] = value
                cahr_str_id = key
                break

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": {
                                    "char": {
                                        cahr_str_id: act_chars[key]
                                    }
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def evolveChar():
        json_body = request.get_json()

        activity_id = json_body["activityId"]
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        act_info = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id]
        act_chars = act_info["troop"]["char"]

        for key, value in act_chars.items():
            if value["charId"] == json_body["charId"]:
                value["evolvePhase"] = json_body["destEvolvePhase"]
                value["level"] = 1
                act_chars[key] = value
                cahr_str_id = key
                break

        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": {
                                    "char": {
                                        cahr_str_id: act_chars[key]
                                    }
                                }
                            }
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result

    def replaceRate():
        """数据替换"""
        # 获取请求数据
        json_body = request.get_json()

        activity_id = json_body.get("activityId", "")
        stage_id = json_body.get("stageId", "")
        replace = json_body.get("replace", 0)

        global settle_info

        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        # 获取活动数据
        activity_data = sync_data["user"]["activity"]["HALFIDLE_VERIFY1"].get(activity_id, {})

        # 如果replace为1或settleInfo为null，则更新settleInfo
        if replace == 1:
            # 更新sync_data
            stage = activity_data["stage"][stage_id]
            stage["rate"] = settle_info["rate"]
            stage["bossState"] = settle_info["bossState"]
            activity_data["settleInfo"] = None
        else:
            # 如果replace为0且settleInfo已存在，则不覆盖
            activity_data["settleInfo"] = None
            return {
                "playerDataDelta": {
                    "modified": {},
                    "deleted": {}
                }
            }

        data = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: activity_data
                        }
                    }
                },
                "deleted": {}
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return data

    def _add_char_to_activity(activity_data, user_data, char_id):
        """
        角色添加逻辑
        将角色添加到活动数据中，如果角色已存在则不添加
        """
        # 确保 troop/char 结构存在
        troop = activity_data.get("troop", {})
        troop.get("char", {})

        # ① 检查是否已有相同角色（防止重复添加）
        for char_info in troop["char"].values():
            if char_info.get("charId") == char_id:
                return  # 已存在则直接跳过

        # ② 从用户主数据中查找对应角色
        chars_from_sync = user_data.get("user", {}).get("troop", {}).get("chars", {})
        target_char_info = next(
            (info for info in chars_from_sync.values() if info.get("charId") == char_id),
            None
        )
        if not target_char_info:
            return  # 找不到对应角色则跳过

        inst_id = str(target_char_info["instId"])

        # ③ 构建活动角色信息
        new_char_info = {
            "instId": target_char_info["instId"],
            "charId": target_char_info["charId"],
            "level": target_char_info.get("level", 1),
            "evolvePhase": target_char_info.get("evolvePhase", 0),
            "skillLvl": 10 if target_char_info.get("evolvePhase", 0) == 2 else 7,
            "isAssist": False,
            "defaultSkillId": "",
            "defaultEquipId": "",
        }

        # ④ 处理默认技能
        default_skill_index = target_char_info.get("defaultSkillIndex", -1)
        if default_skill_index != -1 and "skills" in target_char_info:
            skills = target_char_info["skills"]
            if len(skills) > default_skill_index:
                new_char_info["defaultSkillId"] = skills[default_skill_index].get("skillId", "")

        # ⑤ 处理默认模组
        if target_char_info.get("currentEquip"):
            new_char_info["defaultEquipId"] = target_char_info["currentEquip"]

        # ⑥ 添加到活动数据
        troop["char"][inst_id] = new_char_info

    def setAssistChar():
        """助战逻辑"""
        json_body = request.get_json()
        sync_data = read_json(SYNC_DATA_TEMPLATE_PATH)

        # 获取请求参数
        activity_id = json_body.get("activityId", "")
        index = json_body.get("index", 0)  # 助战位索引(0-3)
        assist_friend = json_body.get("assistFriend", None)

        # 确保 activity_id 存在
        activity_map = sync_data["user"]["activity"].get("HALFIDLE_VERIFY1", {})
        activity_data = activity_map.get(activity_id, {})

        # 确保 troop 结构存在
        troop = activity_data.get("troop", {})
        troop.get("assist", [None, None, None, None])
        troop.get("char", {})

        # 跟踪被删除的角色实例ID
        deleted_char_inst_ids = []

        # ========== 情况 1：清除助战位 ==========
        if assist_friend is None:
            old_assist_char = troop["assist"][index] if index < len(troop["assist"]) else None

            if old_assist_char is not None:
                old_char_id = old_assist_char.get("charId", "")
                # 删除 troop.char 中的 isAssist 角色
                for inst_id, char_info in list(troop["char"].items()):
                    if (
                            char_info.get("charId") == old_char_id
                            and char_info.get("isAssist", False)
                    ):
                        deleted_char_inst_ids.append(inst_id)
                        troop["char"].pop(inst_id, None)
                        break

            # 清除助战位
            if index < len(troop["assist"]):
                troop["assist"][index] = None

        # ========== 情况 2：设置新的助战角色 ==========
        else:
            assist_char = assist_friend.get("assistChar", {})
            char_id = assist_char.get("charId", "")

            # 确保 assist 数组长度为4
            while len(troop["assist"]) < 4:
                troop["assist"].append(None)

            # 若该角色已在其他助战位上，清除旧槽（换位情况）
            for i in range(len(troop["assist"])):
                if i != index and troop["assist"][i] is not None:
                    if troop["assist"][i].get("charId") == char_id:
                        troop["assist"][i] = None
                        break

            # 清理当前槽原有的助战角色
            old_assist_char = troop["assist"][index]
            if old_assist_char is not None:
                old_char_id = old_assist_char.get("charId", "")
                for inst_id, char_info in list(troop["char"].items()):
                    if (
                            char_info.get("charId") == old_char_id
                            and char_info.get("isAssist", False)
                    ):
                        deleted_char_inst_ids.append(inst_id)
                        troop["char"].pop(inst_id, None)
                        break

            # 设置新的助战角色
            troop["assist"][index] = assist_char

            # 添加该角色（函数内部已自动去重）
            vhalfidle._add_char_to_activity(activity_data, sync_data, char_id)

            # 将添加的角色标记为 isAssist = True
            for char_info in troop["char"].values():
                if char_info.get("charId") == char_id:
                    char_info["isAssist"] = True
                    break

        # 保存更新
        sync_data["user"]["activity"]["HALFIDLE_VERIFY1"][activity_id] = activity_data

        deleted = {
            "activity": {
                "HALFIDLE_VERIFY1": {
                    activity_id: {
                        "troop": {
                            "char": deleted_char_inst_ids
                        }
                    }
                }
            }
        } if deleted_char_inst_ids else {}

        # 构造返回数据
        result = {
            "playerDataDelta": {
                "modified": {
                    "activity": {
                        "HALFIDLE_VERIFY1": {
                            activity_id: {
                                "troop": troop
                            }
                        }
                    },
                },
                "deleted": deleted
            }
        }

        run_after_response(write_json, sync_data, SYNC_DATA_TEMPLATE_PATH)

        return result
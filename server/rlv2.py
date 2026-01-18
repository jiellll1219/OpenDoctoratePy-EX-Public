from flask import request
from copy import deepcopy
from collections import deque
from virtualtime import time
import random
import os
import re
import hashlib

from constants import (
    SYNC_DATA_TEMPLATE_PATH,
    RLV2_JSON_PATH,
    RLV2_USER_SETTINGS_PATH,
    CONFIG_PATH,
    RLV2_SETTINGS_PATH,
    SERVER_DATA_PATH
)

from utils import read_json, write_json, decrypt_battle_data, writeLog, get_memory, run_after_response
import data.rlv2_data


def rlv2GiveUpGame():
    server_data = read_json(SERVER_DATA_PATH)
    seed = server_data["rlv2_seed"]
    deque_seed = deque(server_data["seed_list"])
    deque_seed.appendleft(seed)
    server_data["seed_list"] = list(deque_seed)
    server_data["rlv2_seed"] = None

    run_after_response(write_json, server_data, SERVER_DATA_PATH)
    return {
        "result": "ok",
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": {
                        "player": None,
                        "record": None,
                        "map": None,
                        "troop": None,
                        "inventory": None,
                        "game": None,
                        "buff": None,
                        "module": None,
                    }
                }
            },
            "deleted": {},
        },
    }


def rlv2CreateGame():
    request_data = request.get_json()

    theme = request_data["theme"]
    mode = request_data["mode"]
    if mode == "MONTH_TEAM" or mode == "CHALLENGE":
        mode = "NORMAL"
    mode_grade = request_data["modeGrade"]

    ro_int = int(theme.split("_")[1])
    band_length = [None, 11, 23, 14, 23, 21]
    bands = []
    ending = ""

    if ro_int < len(band_length):
        for band in range(1, band_length[ro_int]):
            bands.append(f"rogue_{ro_int}_band_{band}")
        # ending = random.choice([f"ro{ro_int}_ending_{i}" for i in range(1, 4)])
        ending = f"ro{ro_int}_ending_1"

    rlv2 = {
        "player": {
            "state": "INIT",
            "property": {
                "exp": 0,
                "level": 10,
                "maxLevel": 10,
                "hp": {"current": 10000, "max": 10000},
                "gold": 450,
                "shield": 10000,
                "capacity": 10000,
                "population": {"cost": 0, "max": 6},
                "conPerfectBattle": 0,
            },
            "cursor": {"zone": 0, "position": None},
            "trace": [],
            "pending": [
                {
                    "index": "e_0",
                    "type": "GAME_INIT_RELIC",
                    "content": {
                        "initRelic": {
                            "step": [1, 3],
                            "items": {
                                str(i): {"id": band, "count": 1}
                                for i, band in enumerate(bands)
                            },
                        }
                    },
                },
                {
                    "index": "e_1",
                    "type": "GAME_INIT_RECRUIT_SET",
                    "content": {
                        "initRecruitSet": {
                            "step": [2, 3],
                            "option": ["recruit_group_1"],
                        }
                    },
                },
                {
                    "index": "e_2",
                    "type": "GAME_INIT_RECRUIT",
                    "content": {
                        "initRecruit": {
                            "step": [3, 3],
                            "tickets": [],
                            "showChar": [],
                            "team": None,
                        }
                    },
                },
            ],
            "status": {"bankPut": 0},
            "toEnding": ending,
            "chgEnding": False,
        },
        "record": {"brief": None},
        "map": {"zones": {}},
        "troop": {
            "chars": {},
            "expedition": [],
            "expeditionReturn": None,
            "hasExpeditionReturn": False,
        },
        "inventory": {
            "relic": {},
            "recruit": {},
            "trap": None,
            "consumable": {},
            "exploreTool": {},
        },
        "game": {
            "mode": mode,
            "predefined": None,
            "theme": theme,
            "outer": {"support": False},
            "start": time(),
            "eGrade": mode_grade,
            "equivalentGrade": mode_grade,
        },
        "buff": {"tmpHP": 0, "capsule": None, "squadBuff": []},
        "module": {
            "san": None,
            "dice": None,
            "totem": None,
            "vision": None,
            "chaos": None,
            "fragment": None,
            "disaster": None,
            "nodeUpgrade": None,
            "copper": None,
            "wrath": None,
            "sky": None
        }
    }

    match theme:
        case "rogue_1":
            pass
        case "rogue_2":
            rlv2["module"]["san"] = {"sanity": 100}
            rlv2["module"]["dice"] = {"id": "", "count": 1}
        case "rogue_3":
            rlv2["module"]["totem"] = {"totemPiece": [], "predictTotemId": "rogue_3_totem_B_E2"}
            rlv2["module"]["vision"] = {"value": 3, "isMax": False}
            rlv2["module"]["chaos"] = {
                "value": 0,
                "level": 0,
                "curMaxValue": 4,
                "chaosList": [],
                "predict": "",
                "deltaChaos": {
                    "dValue": 0,
                    "preLevel": 0,
                    "afterLevel": 0,
                    "dChaos": []
                },
                "lastBattleGain": 0
            }
        case "rogue_4":
            rlv2["module"]["fragment"] = {
                "totalWeight": 0,
                "limitWeight": 3,
                "overWeight": 4,
                "fragments": {},
                "troopWeights": {}, # 转到 _rlv2.ro4_troopWeights_calculate() 处理
                "troopCarry": [],
                "sellCount": 0,
                "currInspiration": None
            }
            rlv2["module"]["disaster"] = {
                "curDisasterId": None,
                "disperseStep": 0
            }
            rlv2["module"]["nodeUpgrade"] = {
                "nodeTypeInfoMap": {
                    "REST": {
                        "tempUpgrade": "temp_update_3",
                        "upgradeList": []
                    },
                    "BATTLE_SHOP": {
                        "tempUpgrade": "temp_update_4",
                        "upgradeList": []
                    },
                    "ALCHEMY": {
                        "tempUpgrade": "temp_update_8",
                        "upgradeList": []
                    }
                }
            }
        case "rogue_5":
            rlv2["module"]["copper"] = None # 转到 _rlv2.ro5_drawCopper() 处理
            rlv2["module"]["wrath"] = {
                "wraths": [],
                "newWrath": -1
            }
            rlv2["module"]["sky"] = {"zones": {}}
        case _:
            pass

    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    config = read_json(CONFIG_PATH)
    if config["rlv2Config"]["allChars"]:
        match theme:
            case "rogue_1":
                ticket = "rogue_1_recruit_ticket_all"
            case "rogue_2":
                ticket = "rogue_2_recruit_ticket_all"
            case "rogue_3":
                ticket = "rogue_3_recruit_ticket_all"
            case "rogue_4":
                ticket = "rogue_4_recruit_ticket_all"
            case "rogue_5":
                ticket = "rogue_5_recruit_ticket_all"
            case _:
                ticket = ""
        chars = _rlv2.getChars(use_user_defaults=True)
        for i, char in enumerate(chars):
            ticket_id = f"t_{i}"
            char_id = str(i + 1)
            char["instId"] = char_id
            # rlv2["inventory"]["recruit"][ticket_id] = {
            #     "index": f"t_{i}",
            #     "id": ticket,
            #     "state": 2,
            #     "list": [],
            #     "result": char,
            #     "ts": time() - 300,
            #     "from": "initial",
            #     "mustExtra": 0,
            #     "needAssist": True,
            # }
            rlv2["troop"]["chars"][char_id] = char

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2ChooseInitialRelic():
    request_data = request.get_json()
    select = request_data["select"]

    rlv2 = read_json(RLV2_JSON_PATH)
    band = rlv2["player"]["pending"][0]["content"]["initRelic"]["items"][select]["id"]
    rlv2["player"]["pending"].pop(0)
    rlv2["inventory"]["relic"]["r_0"] = {
        "index": "r_0",
        "id": band,
        "count": 1,
        "ts": time(),
    }
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2SelectChoice():
    rlv2 = read_json(RLV2_JSON_PATH)

    # run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2ChooseInitialRecruitSet():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)

    config = read_json(CONFIG_PATH)
    if not config["rlv2Config"]["allChars"]:
        for i in range(3):
            ticket_id = _rlv2.getNextTicketIndex(rlv2)
            _rlv2.addTicket(rlv2, ticket_id)
            rlv2["player"]["pending"][0]["content"]["initRecruit"]["tickets"].append(
                ticket_id
            )

    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data



def rlv2ActiveRecruitTicket():
    request_data = request.get_json()
    ticket_id = request_data["id"]

    rlv2 = read_json(RLV2_JSON_PATH)
    _rlv2.activateTicket(rlv2, ticket_id)
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def getNextCharId(rlv2):
    config = read_json(CONFIG_PATH)
    if not config["rlv2Config"]["allChars"]:
        i = 1
    else:
        i = 10000
    while str(i) in rlv2["troop"]["chars"]:
        i += 1
    return str(i)


def rlv2RecruitChar():
    request_data = request.get_json()
    ticket_id = request_data["ticketIndex"]
    option_id = int(request_data["optionId"])

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)
    char_id = getNextCharId(rlv2)
    char = rlv2["inventory"]["recruit"][ticket_id]["list"][option_id]
    char["instId"] = char_id
    rlv2["inventory"]["recruit"][ticket_id]["state"] = 2
    rlv2["inventory"]["recruit"][ticket_id]["list"] = []
    rlv2["inventory"]["recruit"][ticket_id]["result"] = char
    rlv2["troop"]["chars"][char_id] = char
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "chars": [char],
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        },
    }

    return data


def rlv2CloseRecruitTicket():
    request_data = request.get_json()
    ticket_id = request_data["id"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["pending"].pop(0)
    rlv2["inventory"]["recruit"][ticket_id]["state"] = 2
    rlv2["inventory"]["recruit"][ticket_id]["list"] = []
    rlv2["inventory"]["recruit"][ticket_id]["result"] = None
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2FinishEvent():
    server_data = read_json(SERVER_DATA_PATH)
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["cursor"]["zone"] = 1
    rlv2["player"]["pending"] = []
    theme = rlv2["game"]["theme"]

    # 可用节点类型测试用
    if theme == "rogue_0":
        zone = theme.split("_")[1]
        rlv2["map"]["zones"] = data.rlv2_data.test_data(zone)
    else:
        # too large, do not send it every time
        # rlv2["map"]["zones"] = _rlv2.getMap(theme)
        rlv2["map"]["zones"], seed = _rlv2.getMap_new(theme, server_data["rlv2_seed"], rlv2["player"]["cursor"]["zone"])
        server_data["rlv2_seed"] = seed
        
        match theme:
            case "rogue_4":
                troopWeights = _rlv2.ro4_troopWeights_calculate(rlv2)
                rlv2["module"]["fragment"]["troopWeights"] = troopWeights
            case "rogue_5":
                coppper_bag, drawn_list = _rlv2.ro5_drawCopper(seed)
                rlv2["player"]["state"] = "PENDING"
                rlv2["module"]["copper"] = {}
                rlv2["module"]["copper"]["bag"] = {}
                rlv2["module"]["copper"]["bag"] = coppper_bag
                rlv2["module"]["copper"]["redrawCost"] = 0
                rlv2["player"]["pending"].insert(
                    0,
                    {
                        "type": "DRAW_COPPER",
                        "content": {
                            "drawCopper": {
                                "copper": drawn_list,
                                "divineEventId": "rogue_5_levelEVE_2"
                            }, 
                            "done": False
                        }
                    }
                )

            case _:
                pass

    run_after_response(write_json, server_data, SERVER_DATA_PATH)
    run_after_response(write_json, rlv2, RLV2_JSON_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return result


def rlv2MoveAndBattleStart():
    request_data = request.get_json()
    stage_id = request_data["stageId"]
    x = request_data["to"]["x"]
    y = request_data["to"]["y"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "PENDING"
    rlv2["player"]["cursor"]["position"] = {"x": x, "y": y}
    rlv2["player"]["trace"].append(rlv2["player"]["cursor"])
    pending_index = _rlv2.getNextPendingIndex(rlv2)
    buffs = _rlv2.getBuffs(rlv2, stage_id)
    theme = rlv2["game"]["theme"]
    match theme:
        case "rogue_1":
            box_info = {}
        case "rogue_2":
            box_info = {
                random.choice(
                    ["trap_065_normbox", "trap_066_rarebox", "trap_068_badbox"]
                ): 100
            }
        case "rogue_3":
            box_info = {
                random.choice(
                    ["trap_108_smbox", "trap_109_smrbox", "trap_110_smbbox"]
                ): 100
            }
        case "rogue_4":
            box_info = {
                random.choice(
                    ["trap_757_skzbox", "trap_758_skzmbx", "trap_759_skzwyx"]
                ): 100
            },
        case "rogue_5":
            box_info = {
                random.choice(
                    ["rogue_5_stash_recruit", "pool_recruit_1"]
                ): 100
            }
        case _:
            box_info = {}
    dice_roll = []
    if theme == "rogue_2":
        dice_upgrade_count = 0
        band = rlv2["inventory"]["relic"]["r_0"]["id"]
        if (
            band == "rogue_2_band_16"
            or band == "rogue_2_band_17"
            or band == "rogue_2_band_18"
        ):
            dice_upgrade_count += 1
        for i in rlv2["inventory"]["relic"]:
            if rlv2["inventory"]["relic"][i]["id"] == "rogue_2_relic_grace_63":
                dice_upgrade_count += 1
        if dice_upgrade_count == 0:
            dice_face_count = 6
            dice_id = "trap_067_dice"
        elif dice_upgrade_count == 1:
            dice_face_count = 8
            dice_id = "trap_088_dice2"
        else:
            dice_face_count = 12
            dice_id = "trap_089_dice3"
        dice_roll = [random.randint(1, dice_face_count) for i in range(100)]
        buffs.append(
            {
                "key": "misc_insert_token_card",
                "blackboard": [
                    {"key": "token_key", "value": 0, "valueStr": dice_id},
                    {"key": "level", "value": 1, "valueStr": None},
                    {"key": "skill", "value": 0, "valueStr": None},
                    {"key": "cnt", "value": 100, "valueStr": None},
                ],
            }
        )
    rlv2["player"]["pending"].insert(
        0,
        {
            "index": pending_index,
            "type": "BATTLE",
            "content": {
                "battle": {
                    "state": 1,
                    "chestCnt": 100,
                    "goldTrapCnt": 100,
                    "diceRoll": dice_roll,
                    "boxInfo": box_info,
                    "tmpChar": [],
                    "sanity": 0,
                    "unKeepBuff": buffs,
                }
            },
        },
    )
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2BattleFinish():
    request_data = request.get_json()
    battle_data = decrypt_battle_data(request_data["data"])

    rlv2 = read_json(RLV2_JSON_PATH)
    if battle_data["completeState"] != 1:
        rlv2["player"]["pending"].pop(0)
        theme = rlv2["game"]["theme"]
        ticket = f"{theme}_recruit_ticket_all"
        pending_index = _rlv2.getNextPendingIndex(rlv2)
        rlv2["player"]["pending"].insert(
            0,
            {
                "index": pending_index,
                "type": "BATTLE_REWARD",
                "content": {
                    "battleReward": {
                        "earn": {
                            "damage": 0,
                            "hp": 0,
                            "shield": 0,
                            "exp": 0,
                            "populationMax": 0,
                            "squadCapacity": 0,
                            "maxHpUp": 0,
                        },
                        "rewards": [
                            {
                                "index": 0,
                                "items": [{"sub": 0, "id": ticket, "count": 1}],
                                "done": 0,
                            }
                        ],
                        "show": "1",
                    }
                },
            },
        )
    else:
        rlv2["player"]["state"] = "WAIT_MOVE"
        rlv2["player"]["pending"] = []
        rlv2["player"]["cursor"]["position"]["x"] = 0
        rlv2["player"]["cursor"]["position"]["y"] = 0
        rlv2["player"]["trace"].pop()

    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2FinishBattleReward():
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["pending"] = []
    rlv2["player"]["cursor"]["position"]["x"] = 0
    rlv2["player"]["cursor"]["position"]["y"] = 0
    rlv2["player"]["trace"].pop()
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2MoveTo():
    request_data = request.get_json()
    x = request_data["to"]["x"]
    y = request_data["to"]["y"]

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "PENDING"
    rlv2["player"]["cursor"]["position"] = {"x": x, "y": y}
    theme = rlv2["game"]["theme"]
    goods = _rlv2.getGoods(theme)
    rlv2["player"]["trace"].append(rlv2["player"]["cursor"])
    pending_index = _rlv2.getNextPendingIndex(rlv2)
    rlv2["player"]["pending"].insert(
        0,
        {
            "index": pending_index,
            "type": "SHOP",
            "content": {
                "shop": {
                    "bank": {
                        "open": False,
                        "canPut": False,
                        "canWithdraw": False,
                        "withdraw": 0,
                        "cost": 1,
                    },
                    "id": "just_a_shop",
                    "goods": goods,
                    "_done": False,
                }
            },
        },
    )
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2LeaveShop():
    server_data = read_json(SERVER_DATA_PATH)
    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["pending"] = []
    if rlv2["player"]["cursor"]["position"]["x"] > 1:
        rlv2["player"]["cursor"]["zone"] += 1
        rlv2["player"]["cursor"]["position"] = None
        theme = rlv2["game"]["theme"]
        rlv2["map"]["zones"], seed = _rlv2.getMap_new(theme, server_data["rlv2_seed"], rlv2["player"]["cursor"]["zone"])
    elif rlv2["player"]["cursor"]["position"]["x"] == 1:
        rlv2["player"]["cursor"]["position"]["x"] = 0
        rlv2["player"]["cursor"]["position"]["y"] = 0
        rlv2["player"]["trace"].pop()
    
    run_after_response(write_json, rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data

def rlv2BuyGoods(select: int=None):
    if select is None:
        request_data = request.get_json()
        select = int(request_data["select"][0])

    rlv2 = read_json(RLV2_JSON_PATH)
    item_id = rlv2["player"]["pending"][0]["content"]["shop"]["goods"][select]["itemId"]
    if item_id.find("_recruit_ticket_") != -1:
        ticket_id = _rlv2.getNextTicketIndex(rlv2)
        _rlv2.addTicket(rlv2, ticket_id)
        _rlv2.activateTicket(rlv2, ticket_id)
    elif item_id.find("_relic_") != -1:
        relic_id = _rlv2.getNextRelicIndex(rlv2)
        rlv2["inventory"]["relic"][relic_id] = {
            "index": relic_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    elif item_id.find("_active_tool_") != -1:
        rlv2["inventory"]["trap"] = {
            "index": item_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    elif item_id.find("_explore_tool_") != -1:
        explore_tool_id = rlv2.getNextExploreToolIndex(rlv2)
        rlv2["inventory"]["exploreTool"][explore_tool_id] = {
            "index": explore_tool_id,
            "id": item_id,
            "count": 1,
            "ts": 1695000000,
        }
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2shopAction():

    json_body = request.get_json()

    try:
        select = int (json_body["buy"][0])
        return rlv2BuyGoods(select)
    except (KeyError, IndexError):
        return rlv2LeaveShop()

    rlv2 = read_json(RLV2_JSON_PATH)
    rlv2["player"]["state"] = "WAIT_MOVE"
    rlv2["player"]["pending"] = []
    if rlv2["player"]["cursor"]["position"]["x"] > 1:
        rlv2["player"]["cursor"]["zone"] += 1
        rlv2["player"]["cursor"]["position"] = None
    elif rlv2["player"]["cursor"]["position"]["x"] == 1:
        rlv2["player"]["cursor"]["position"]["x"] = 0
        rlv2["player"]["cursor"]["position"]["y"] = 0
        rlv2["player"]["trace"].pop()
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2ChooseBattleReward():
    request_data = request.get_json()
    index = request_data["index"]

    rlv2 = read_json(RLV2_JSON_PATH)
    if index == 0:
        ticket_id = _rlv2.getNextTicketIndex(rlv2)
        _rlv2.addTicket(rlv2, ticket_id)
        _rlv2.activateTicket(rlv2, ticket_id)
    run_after_response(write_json ,rlv2, RLV2_JSON_PATH)

    data = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": rlv2,
                }
            },
            "deleted": {},
        }
    }

    return data


def rlv2CopperConfirmDraw():
    rlv2 = read_json(RLV2_JSON_PATH)
    
    rlv2["player"]["pending"].pop(0)
    rlv2["player"]["state"] = "WAIT_MOVE"

    run_after_response(write_json, rlv2, RLV2_JSON_PATH)

    result = {
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current":{
                        "player": rlv2["player"]
                    }
                }
            },
            "deleted": {}
        }
    }

    return result 


def rlv2CopperRedraw():

    rlv2_data = read_json(RLV2_JSON_PATH)

    bag = rlv2_data["module"]["copper"]["bag"]
    for key, value in bag.items():
        value["isDrawn"] = False

    # a1 = random.sample(0, len(bag.keys()))
    copper = []
    L1 = random.sample(range(0, len(bag.keys())), 3)
    for key in L1:
        key = "c_" + str(key)
        copper.append(key)
        bag[key]["isDrawn"] = True

    run_after_response(write_json ,rlv2_data, RLV2_JSON_PATH)

    data = {
        "copper": copper,
        "divineEventId": "rogue_5_levelEVE_2",
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": {
                        "module": {
                            "copper": {
                                "bag": bag,
                            }
                        }
                    }
                }
            },
            "deleted": {},
        }
    }

    return data

def rlv2SetTroopCarry():
    result = {}

    return result


def rlv2getReward():
    result = {}

    return result


class _rlv2:
    def getNextRelicIndex(rlv2):
        d = set()
        for e in rlv2["inventory"]["relic"]:
            d.add(int(e[2:]))
        i = 0
        while i in d:
            i += 1
        return f"r_{i}"

    def getNextExploreToolIndex(rlv2):
        d = set()
        for e in rlv2["inventory"]["exploreTool"]:
            d.add(int(e[2:]))
        i = 0
        while i in d:
            i += 1
        return f"e_{i}"
    
    def getChars(use_user_defaults=False):
        user_data = read_json(SYNC_DATA_TEMPLATE_PATH)
        chars = [
            user_data["user"]["troop"]["chars"][i]
            for i in user_data["user"]["troop"]["chars"]
        ]
        if use_user_defaults:
            rlv2_user_settings = read_json(RLV2_USER_SETTINGS_PATH)
            initialChars = set(rlv2_user_settings["initialChars"])
            chars_tmp = []
            for char in chars:
                if char["charId"] in initialChars:
                    chars_tmp.append(char)
            chars = chars_tmp
        for i in range(len(chars)):
            char = chars[i]
            if char["evolvePhase"] == 2:
                char_alt = deepcopy(char)
                char_alt["evolvePhase"] = 1
                char_alt["level"] -= 10
                if len(char_alt["skills"]) == 3:
                    char_alt["defaultSkillIndex"] = 1
                    char_alt["skills"][-1]["unlock"] = 0
                for skill in char_alt["skills"]:
                    skill["specializeLevel"] = 0
                char_alt["currentEquip"] = None
                chars.append(char_alt)
                if char["charId"] == "char_002_amiya":
                    tmpls = list(char_alt["tmpl"].keys())
                    for j in tmpls:
                        if len(char_alt["tmpl"][j]["skills"]) == 3:
                            char_alt["tmpl"][j]["defaultSkillIndex"] = 1
                            char_alt["tmpl"][j]["skills"][-1]["unlock"] = 0
                        for skill in char_alt["tmpl"][j]["skills"]:
                            skill["specializeLevel"] = 0
                        char_alt["tmpl"][j]["currentEquip"] = None
                    char["currentTmpl"] = tmpls[0]
                    char_alt["currentTmpl"] = tmpls[0]
                    for j in range(1, len(tmpls)):
                        for k in [char, char_alt]:
                            char_alt_alt = deepcopy(k)
                            char_alt_alt["currentTmpl"] = tmpls[j]
                            chars.append(char_alt_alt)
        for i, char in enumerate(chars):
            char.update(
                {
                    "instId": str(i),
                    "type": "NORMAL",
                    "upgradeLimited": False,
                    "upgradePhase": 1,
                    "isUpgrade": False,
                    "isCure": False,
                    "population": 0,
                    "charBuff": [],
                    "troopInstId": "0",
                }
            )
            if char["evolvePhase"] < 2:
                char["upgradeLimited"] = True
                char["upgradePhase"] = 0
        return chars

    def addTicket(rlv2_data, ticket_id):
        theme = rlv2_data["game"]["theme"]
        match theme:
            case "rogue_1":
                ticket = "rogue_1_recruit_ticket_all"
            case "rogue_2":
                ticket = "rogue_2_recruit_ticket_all"
            case "rogue_3":
                ticket = "rogue_3_recruit_ticket_all"
            case "rogue_4":
                ticket = "rogue_4_recruit_ticket_all"
            case "rogue_5":
                ticket = "rogue_5_recruit_ticket_all"
            case _:
                ticket = ""
        rlv2_data["inventory"]["recruit"][ticket_id] = {
            "index": ticket_id,
            "id": ticket,
            "state": 0,
            "list": [],
            "result": None,
            "ts": time(),
            "from": "initial",
            "mustExtra": 0,
            "needAssist": True,
        }


    def getGoods(theme):
        match theme:
            case "rogue_1":
                ticket = "rogue_1_recruit_ticket_all"
                price_id = "rogue_1_gold"
            case "rogue_2":
                ticket = "rogue_2_recruit_ticket_all"
                price_id = "rogue_2_gold"
            case "rogue_3":
                ticket = "rogue_3_recruit_ticket_all"
                price_id = "rogue_3_gold"
            case "rogue_4":
                ticket = "rogue_4_recruit_ticket_all"
                price_id = "rogue_4_gold"
            case "rogue_5":
                ticket = "rogue_5_recruit_ticket_all"
                price_id = "rogue_5_gold"
            case _:
                ticket = ""
                price_id = ""
        goods = [
            {
                "index": "0",
                "itemId": ticket,
                "count": 1,
                "priceId": price_id,
                "priceCount": 0,
                "origCost": 0,
                "displayPriceChg": False,
                "_retainDiscount": 1,
            }
        ]
        i = 1
        rlv2_table = get_memory("roguelike_topic_table")
        for j in rlv2_table["details"][theme]["archiveComp"]["relic"]["relic"]:
            goods.append(
                {
                    "index": str(i),
                    "itemId": j,
                    "count": 1,
                    "priceId": price_id,
                    "priceCount": 0,
                    "origCost": 0,
                    "displayPriceChg": False,
                    "_retainDiscount": 1,
                }
            )
            i += 1
        for j in rlv2_table["details"][theme]["difficultyUpgradeRelicGroups"]:
            for k in rlv2_table["details"][theme]["difficultyUpgradeRelicGroups"][j][
                "relicData"
            ]:
                goods.append(
                    {
                        "index": str(i),
                        "itemId": k["relicId"],
                        "count": 1,
                        "priceId": price_id,
                        "priceCount": 0,
                        "origCost": 0,
                        "displayPriceChg": False,
                        "_retainDiscount": 1,
                    }
                )
                i += 1
        for j in rlv2_table["details"][theme]["archiveComp"]["trap"]["trap"]:
            goods.append(
                {
                    "index": str(i),
                    "itemId": j,
                    "count": 1,
                    "priceId": price_id,
                    "priceCount": 0,
                    "origCost": 0,
                    "displayPriceChg": False,
                    "_retainDiscount": 1,
                }
            )
            i += 1
        return goods

    def getMap(theme):
        rlv2_table = get_memory("roguelike_topic_table")
        stages = [i for i in rlv2_table["details"][theme]["stages"]]

        # 商店类型
        if theme != "rogue_1":
            shop = 4096
        else:
            shop = 8

        map = {}
        zone = 1
        j = 0
        while j < len(stages):
            zone_map = {"id": f"zone_{zone}", "index": zone, "nodes": {}, "variation": []}
            nodes_list = [
                {
                    "index": "0",
                    "pos": {"x": 0, "y": 0},
                    "next": [{"x": 1, "y": 0}],
                    "type": shop,
                },
                {"index": "100", "pos": {"x": 1, "y": 0}, "next": [], "type": shop},
            ]
            x_max = 9
            y_max = 3
            x = 1
            y = 1
            while j < len(stages):
                stage = stages[j]
                if y > y_max:
                    if x + 1 == x_max:
                        break
                    x += 1
                    y = 0
                node_type = 1
                if rlv2_table["details"][theme]["stages"][stage]["isElite"]:
                    node_type = 2
                elif rlv2_table["details"][theme]["stages"][stage]["isBoss"]:
                    node_type = 4
                nodes_list.append(
                    {
                        "index": f"{x}0{y}",
                        "pos": {"x": x, "y": y},
                        "next": [],
                        "type": node_type,
                        "stage": stage,
                    }
                )
                nodes_list[0]["next"].append({"x": x, "y": y})
                y += 1
                j += 1
            x += 1
            nodes_list[0]["next"].append({"x": x, "y": 0})
            nodes_list.append(
                {
                    "index": f"{x}00",
                    "pos": {"x": x, "y": 0},
                    "next": [],
                    "type": shop,
                    "zone_end": True,
                }
            )

            for node in nodes_list:
                zone_map["nodes"][node["index"]] = node
            map[str(zone)] = zone_map
            zone += 1
        return map
        
    def getMap_new(theme: str, seed: str = None, zone: int = 1):
        rlv2_table = get_memory("roguelike_topic_table")
        stages_list: list[str] = rlv2_table["details"][theme]["stages"].keys()

        # 随机种子
        if seed is None:
            randomseed = os.urandom(16).hex()
            writeLog(f"本次种子：{randomseed}")
        else:
            randomseed = seed

        random.seed(f"{randomseed}_{zone}")

        # 商店类型
        shop = 4096 if theme != "rogue_1" else 8
        wish = 512 if theme != "rogue_1" else 64

        zone_map = {
            str(zone): {
                "id": f"zone_{zone}",
                "index": zone,
                "nodes": {},
                "variation": []
            }
        }

        nodetemp = {
            "index": "",
            "pos": {"x": 0, "y": 0},
            "next": [],
            "type": 0,
            "refresh": {"usedCount": 0, "count": 99, "cost": 1}
        }

        # 节点类型权重
        type_weight: dict[int, int] = {}
        type_weight.update({1:55, 2:15, 32:30, wish:20})

        if zone > 1:
            type_weight.setdefault(16, 20)
            match theme:
                case "rogue_1":
                    type_weight.update({
                        4: 10, 8: 10, 64: 10, 128: 10, 256: 10
                    })
                case "rogue_2":
                    type_weight.update({
                        4: 10, 1024: 10, 2048: 10, 4096: 10, 8192: 10, 16384: 10
                    })
                case "rogue_3":
                    type_weight.update({
                        4: 10, 1024: 10, 2048: 10, 4096: 10, 8192: 10, 65536: 10
                    })
                case "rogue_4":
                    type_weight.update({
                        4: 10, 128: 10, 256: 10, 1024: 10, 2048: 10, 
                        4096: 10, 8192: 10, 131072: 10, 262144: 10
                    })
                case "rogue_5":
                    type_weight.update({
                        4: 10, 1024: 10, 2048: 10, 4096: 10, 8192: 10, 
                        262144: 10, 524288: 10
                    })
                case _:
                    pass

        items = sorted(type_weight.items())
        type_list = [k for k, _ in items]
        type_weight = [v for _, v in items]


        # 坐标最大值
        x_max = [None, 2, 4, 4, 5] 
        y_max = [None, 2, 3, 4, 4]

        ro_num = theme.split("_")[1]
        normal_list = [s for s in stages_list if s.startswith(f"ro{ro_num}_n_{zone}_")]
        elite_list  = [s for s in stages_list if s.startswith(f"ro{ro_num}_e_{zone}_")]
        boss_list   = [
            s for s in stages_list
            if re.fullmatch(rf"ro{ro_num}_b_[1-9]", s)
        ]

        # 路径数据
        nodes_by_x: dict[int, list[int]] = {}
        can_add_shop = True
        zone_1 = True if zone == 1 else False

        # 可复现非random随机
        def rand_by_key(seed: str, *keys, mod: int) -> int:
            h = hashlib.md5(f"{seed}_{'_'.join(map(str, keys))}".encode()).hexdigest()
            return int(h, 16) % mod

        # 随机节点生成
        for x in range(0, x_max[zone]):
            nodes_by_x[x] = []
            is_end_col = (not zone_1 and x == x_max[zone] - 1)

            # end_node 单独生成
            if is_end_col:
                match zone:
                    case 2:
                        end_type = 512
                        end_count = 2
                    case 3:
                        end_type = 4
                        end_count = 1
                    case _:
                        end_type = 0
                        end_count = 1

                for y in range(end_count):
                    node = deepcopy(nodetemp)
                    node_index = x * 100 + y

                    node["pos"]["x"] = x
                    node["pos"]["y"] = y
                    node["index"] = str(node_index)
                    node["type"] = end_type
                    node["zone_end"] = True

                    if end_type == 4:
                        node["stage"] = random.choice(boss_list)

                    zone_map[str(zone)]["nodes"][node["index"]] = node
                    nodes_by_x[x].append(y)

                continue

            #普通列，正常 y_size 随机
            y_size = rand_by_key(randomseed, zone, x, mod=y_max[zone]) + 1

            if can_add_shop and x > 0:
                type_list.append(shop)
                type_weight.append(10)
                can_add_shop = False

            for y in range(y_size):
                node = deepcopy(nodetemp)
                node_index = x * 100 + y

                node_type = random.choices(type_list, weights=type_weight, k=1)[0]

                node["pos"]["x"] = x
                node["pos"]["y"] = y
                node["index"] = str(node_index)
                node["type"] = node_type

                match node_type:
                    case 1:
                        node["stage"] = random.choice(normal_list)
                    case 2:
                        node["stage"] = random.choice(elite_list)

                zone_map[str(zone)]["nodes"][node["index"]] = node
                nodes_by_x[x].append(y)

        # 第一层固定节点
        if zone_1:
            end_type = 1048576 if ro_num == 5 else shop
            z1_node = shop if ro_num == 5 else 32
            zone1_nodes = {
                "200": {
                    "index": "200",
                    "pos": {"x": 2, "y": 0},
                    "next": [{"x": 3, "y": 0}],
                    "type": z1_node,
                    "refresh": {"usedCount": 0, "count": 99, "cost": 1}
                },
                "201": {
                    "index": "201",
                    "pos": {"x": 2, "y": 1},
                    "next": [{"x": 3, "y": 0}],
                    "type": z1_node,
                    "refresh": {"usedCount": 0, "count": 99, "cost": 1}
                },
                "300": {
                    "index": "300",
                    "pos": {"x": 3, "y": 0},
                    "next": [],
                    "type": end_type,
                    "zone_end": True
                }
            }

            zone_map[str(zone)]["nodes"].update(zone1_nodes)
            nodes_by_x[2] = [0, 1]
            nodes_by_x[3] = [0]

        # 路径分配
        for idx, node in zone_map[str(zone)]["nodes"].items():
            x:int = node["pos"]["x"]
            y:int = node["pos"]["y"]

            # zone1 固定节点，跳过
            if zone == 1 and x >= 2:
                continue

            node["next"] = []

            # 横向
            if x + 1 in nodes_by_x:
                candidates = []
                for ny in (y - 1, y, y + 1):
                    if ny in nodes_by_x[x + 1]:
                        candidates.append({"x": x + 1, "y": ny})

                if candidates:
                    k = random.randint(1, min(2, len(candidates)))
                    node["next"].extend(random.sample(candidates, k))

            # 纵向
            if x != 0:
                for ny in (y - 1, y + 1):
                    if ny in nodes_by_x.get(x, []):
                        if random.random() < 0.6:
                            edge = {"x": x, "y": ny}
                            if random.random() < 0.5:
                                edge["key"] = True
                            node["next"].append(edge)

        # 路径检查
        for x in sorted(nodes_by_x.keys()):
            if x == 0:
                continue

            # 收集本列已被指向的 y
            has_incoming = set()
            for node in zone_map[str(zone)]["nodes"].values():
                if node["pos"]["x"] == x - 1:
                    for e in node.get("next", []):
                        if e["x"] == x:
                            has_incoming.add(e["y"])

            # 检查本列所有节点
            for y in nodes_by_x[x]:
                if y in has_incoming:
                    continue

                # 补一条来自 x-1 的连接
                prev_candidates = []
                for py in nodes_by_x[x - 1]:
                    if abs(py - y) <= 1:
                        prev_candidates.append(py)

                if not prev_candidates:
                    continue

                py = random.choice(prev_candidates)
                prev_idx = str((x - 1) * 100 + py)

                zone_map[str(zone)]["nodes"][prev_idx]["next"].append({
                    "x": x,
                    "y": y
                })

        # 节点排序
        for node in zone_map[str(zone)]["nodes"].values():
            if "next" in node and node["next"]:
                node["next"].sort(key=lambda e: (e["x"], e["y"]))

        return zone_map, randomseed

    def getNextPendingIndex(rlv2):
        d = set()
        for e in rlv2["player"]["pending"]:
            d.add(int(e["index"][2:]))
        i = 0
        while i in d:
            i += 1
        return f"e_{i}"

    def activateTicket(rlv2, ticket_id):
        pending_index = _rlv2.getNextPendingIndex(rlv2)
        rlv2["player"]["pending"].insert(
            0,
            {
                "index": pending_index,
                "type": "RECRUIT",
                "content": {"recruit": {"ticket": ticket_id}},
            },
        )
        chars = _rlv2.getChars()
        rlv2["inventory"]["recruit"][ticket_id]["state"] = 1
        rlv2["inventory"]["recruit"][ticket_id]["list"] = chars

    def getNextTicketIndex(rlv2):
        d = set()
        for e in rlv2["inventory"]["recruit"]:
            d.add(int(e[2:]))
        config = read_json(CONFIG_PATH)
        if not config["rlv2Config"]["allChars"]:
            i = 0
        else:
            i = 10000 - 1
        while i in d:
            i += 1
        return f"t_{i}"

    def getBuffs(rlv2:dict, stage_id:str):
        rlv2_table:dict = get_memory("roguelike_topic_table")
        theme:str = rlv2["game"]["theme"]
        buffs = []

        if rlv2["inventory"]["trap"] is not None:
            item_id = rlv2["inventory"]["trap"]["id"]
            if item_id in rlv2_table["details"][theme]["relics"]:
                buffs += rlv2_table["details"][theme]["relics"][item_id]["buffs"]
        for i in rlv2["inventory"]["exploreTool"]:
            item_id = rlv2["inventory"]["exploreTool"][i]["id"]
            if item_id in rlv2_table["details"][theme]["relics"]:
                buffs += rlv2_table["details"][theme]["relics"][item_id]["buffs"]

        for i in rlv2["buff"]["squadBuff"]:
            if i in rlv2_table["details"][theme]["squadBuffData"]:
                buffs += rlv2_table["details"][theme]["squadBuffData"][i]["buffs"]

        mode_grade:int = rlv2["game"]["eGrade"]
        theme_buffs = data.rlv2_data.rogue_buffs.get(theme, [])
        
        if theme_buffs is None:
            pass
        else:
            for i in range(len(theme_buffs)):
                if mode_grade < i:
                    break
                for j in theme_buffs[i][1]:
                    theme_buffs[j] = ([], [])
            for i in range(len(theme_buffs)):
                if mode_grade < i:
                    break
                buffs += theme_buffs[i][0]

        def getZone():
            rlv2_settings = read_json(RLV2_SETTINGS_PATH)
            if stage_id in rlv2_settings["stageZone"]:
                return rlv2_settings["stageZone"][stage_id]
            if stage_id.find("_n_") != -1 or stage_id.find("_e_") != -1:
                try:
                    return int(stage_id.split("_")[2])
                except Exception:
                    pass
            return -1

        zone = getZone()
        match theme:
            case "rogue_2":
                if zone == -1:
                    pass
                elif 16 > mode_grade > 0:
                    value = 1 + 0.01 * mode_grade
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": value},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": value},
                                ],
                            },
                        ]
                elif mode_grade == 15:
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": 1.2},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": 1.2},
                                ],
                            },
                        ]
                elif mode_grade > 16:
                    value = 1 + 0.01 * (5 * mode_grade - 60)
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": 1.2},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": value},
                                ],
                            },
                        ]
            case "rogue_3":
                if zone == -1:
                    pass
                if mode_grade > 4:
                    value = 1 + 0.16 * (mode_grade - 4) / 11 #(15 - 4)
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": value},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": value},
                                ],
                            },
                        ]
            case "rogue_4":
                if zone == -1:
                    pass
                if mode_grade > 4:
                    if mode_grade < 8:
                        value = mode_grade - 4
                    elif 7 < mode_grade < 12:
                        value = mode_grade - 3
                    elif 11 < mode_grade < 15:
                        value = 3 * mode_grade - 26 #10 + (mode_grade - 12) * 3
                    else:
                        value = mode_grade + 5
                    value = 1 + value * 0.01
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": value},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": value},
                                ],
                            },
                        ]
            case "rogue_5":
                if zone == -1:
                    pass
                if mode_grade > 3:
                    if mode_grade < 11:
                        value = mode_grade - 3
                    elif 10 < mode_grade < 15:
                        value = mode_grade - 1
                    else:
                        value = mode_grade
                    value = 1 + value * 0.01
                    for i in range(zone):
                        buffs += [
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_atk_down"},
                                    {"key": "atk", "value": value},
                                ],
                            },
                            {
                                "key": "global_buff_normal",
                                "blackboard": [
                                    {"key": "key", "valueStr": "enemy_max_hp_down"},
                                    {"key": "max_hp", "value": value},
                                ],
                            },
                        ]
            case _:
                pass

        return buffs

    def ro5_drawCopper(randomseed:str):
        coppper_bag = {}

        random.seed(randomseed)
        rlv2_table = get_memory("roguelike_topic_table")
        all_copper = [i for i in rlv2_table["details"]["rogue_5"]["items"].keys() 
                      if rlv2_table["details"]["rogue_5"]["items"][i]["type"] == "COPPER"]

        # 随机选择7个copperid
        copper_list = random.sample(all_copper, 7)

        for i in range(7):
            copper_data = {
                "id": copper_list[i],
                "isDrawn": False,
                "layer": -1,
                "countDown": -1,
                "ts": time()
                }
                
            coppper_bag[f"c_{i}"] = copper_data
        
        drawn_list = random.sample(list(coppper_bag.keys()), 3)

        for copper in drawn_list:
            coppper_bag[copper]["isDrawn"] = True

        return coppper_bag, drawn_list
    
    def ro4_troopWeights_calculate(rlv2:dict):
        character_table = get_memory("character_table")
        character_star = get_memory("character_star")
        troopWeights = {}
        char_load_data = {"6": 6, "5": 5, "4": 4, "3": 2, "2": 2, "1": 2}

        for key, value in rlv2["troop"]["chars"].items():
            if value["charId"] == "char_4151_tinman":
                troopWeights[key] = 10
            else:
                char_id = value["charId"]
                char_star = str(character_star[char_id])
                cahr_load = char_load_data[char_star]
                troopWeights[key] = cahr_load

        return troopWeights
